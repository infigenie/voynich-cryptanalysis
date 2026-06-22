#!/usr/bin/env python3
"""Reproducible cryptanalysis of the Voynich (Takahashi/EVA) corpus.
Comparators: Latin (Gutenberg) and English (Gutenberg). Honest, no decipherment claimed."""
import re, math, collections, random
random.seed(42)

# ---------------------------------------------------------------- load VMS
lines = open('LSI_ivtff_0d.txt', encoding='latin-1').read().split('\n')
loc_re = re.compile(r'^<(f[0-9]+[rv][0-9]*)\.([0-9]+),([^;]*);H>\s+(.*?)\s*$')
hdr_re = re.compile(r'^<(f[0-9]+[rv][0-9]*)>\s*<!(.*)>')
page_lang = {}
for ln in lines:
    m = hdr_re.match(ln)
    if m:
        lm = re.search(r'\$L=([A-Z])', m.group(2)); page_lang[m.group(1)] = lm.group(1) if lm else '?'

def clean(t):
    t = re.sub(r'<[^>]*>', '', t)
    return t.replace('!', '').replace('%', '').replace(',', '.')

# group tokens by structure: per-line lists, by locus type, by language
lines_by_type = collections.defaultdict(list)   # type letter -> list of token-lists (one per line)
all_lines = []                                   # (lang, type, [tokens])
for ln in lines:
    m = loc_re.match(ln)
    if not m: continue
    page, lineno, locus, text = m.groups()
    typ = locus[1] if len(locus) > 1 else '?'    # 2nd char = P/L/C/R
    toks = [w for w in clean(text).split('.') if w and not any(c in w for c in '?*@')]
    if not toks: continue
    lines_by_type[typ].append(toks)
    all_lines.append((page_lang.get(page, '?'), typ, toks))

para_lines = [toks for lang, t, toks in all_lines if t == 'P']
para_tokens = [w for toks in para_lines for w in toks]
label_tokens = [w for toks in lines_by_type.get('L', []) for w in toks]
all_tokens = [w for lang, t, toks in all_lines for w in toks]

# ---------------------------------------------------------------- comparators
def load_gutenberg(path):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    # strip Gutenberg header/footer
    s = raw
    a = re.search(r'\*\*\* START.*?\*\*\*', s);  b = re.search(r'\*\*\* END.*?\*\*\*', s)
    if a: s = s[a.end():]
    if b: s = s[:b.start()]
    s = s.lower()
    words = re.findall(r'[a-z]+', s)
    return [w for w in words if 2 <= len(w) <= 20]

latin = load_gutenberg('latin_raw.txt')
english = load_gutenberg('english_raw.txt')

# ---------------------------------------------------------------- entropy helpers
def char_entropies(tokens, sample=None):
    if sample and len(tokens) > sample:
        tokens = random.sample(tokens, sample)
    seq = []
    for w in tokens:
        seq.append('#'); seq.extend(w)
    seq.append('#')
    uni = collections.Counter(seq); M = sum(uni.values())
    h1 = -sum((c/M)*math.log2(c/M) for c in uni.values())
    bi = collections.Counter(zip(seq, seq[1:]))
    fc = collections.Counter()
    for (a, b), c in bi.items(): fc[a] += c
    B = sum(bi.values()); h2 = 0.0
    for (a, b), c in bi.items():
        h2 -= (c/B)*math.log2(c/fc[a])
    alpha = len([k for k in uni if k != '#'])
    return alpha, h1, h2

def word_entropy(tokens):
    c = collections.Counter(tokens); N = sum(c.values())
    return -sum((v/N)*math.log2(v/N) for v in c.values())

def word_cond_entropy(tokens):
    # H(next | current)
    bi = collections.Counter(zip(tokens, tokens[1:]))
    fc = collections.Counter()
    for (a, b), c in bi.items(): fc[a] += c
    B = sum(bi.values()); h = 0.0
    for (a, b), c in bi.items():
        h -= (c/B)*math.log2(c/fc[a])
    return h

def levenshtein(a, b):
    if a == b: return 0
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j]+1, cur[j-1]+1, prev[j-1]+(ca != cb)))
        prev = cur
    return prev[-1]

print("="*70)
print("DEEPER CRYPTANALYSIS OF THE VOYNICH CORPUS (Takahashi/EVA)")
print("="*70)
print(f"VMS tokens (paragraph): {len(para_tokens):,} | labels: {len(label_tokens):,} | all: {len(all_tokens):,}")
print(f"Latin comparator: {len(latin):,} words | English: {len(english):,} words")

# ---- TEST 1: character entropy, three corpora, equal sample size
print("\n[1] CHARACTER ENTROPY (within words, equal sample)  --------------")
S = 30000
print(f"{'corpus':10s} {'alpha':>6s} {'h1':>7s} {'h2':>7s} {'h2/h1':>7s}")
for name, toks in [('Voynich', para_tokens), ('Latin', latin), ('English', english)]:
    a, h1, h2 = char_entropies(toks, sample=S)
    print(f"{name:10s} {a:6d} {h1:7.3f} {h2:7.3f} {h2/h1:7.3f}")
print("Interpretation: VMS h2 far below Latin/English -> abnormally predictable.")

# ---- TEST 2: positional slot grammar (entropy by within-word position)
print("\n[2] SLOT GRAMMAR: glyph entropy by position in word ---------------")
def positional_profile(tokens, maxpos=7):
    out = []
    for p in range(maxpos):
        chars = collections.Counter(w[p] for w in tokens if len(w) > p)
        M = sum(chars.values())
        H = -sum((c/M)*math.log2(c/M) for c in chars.values()) if M else 0
        out.append(H)
    return out
print(f"{'pos':>4s} " + " ".join(f"{i+1:>6d}" for i in range(7)))
for name, toks in [('Voynich', para_tokens), ('Latin', latin), ('English', english)]:
    prof = positional_profile(toks)
    print(f"{name:>10s} " + " ".join(f"{h:6.2f}" for h in prof))
print("Low, uneven per-position entropy in VMS => glyphs fill fixed slots,")
print("not the freer positional mixing of Latin/English.")

# ---- TEST 3: word-order information (syntax test) vs shuffled
print("\n[3] WORD-ORDER INFORMATION (is there syntax?) --------------------")
for name, toks in [('Voynich', para_tokens), ('Latin', latin[:len(para_tokens)]), ('English', english[:len(para_tokens)])]:
    H1 = word_entropy(toks)
    H2 = word_cond_entropy(toks)
    sh = toks[:]; random.shuffle(sh)
    H2s = word_cond_entropy(sh)
    print(f"{name:8s}  H(word)={H1:6.2f}  H(next|cur)={H2:6.2f}  shuffled={H2s:6.2f}  "
          f"order-info={H1-H2:5.2f} bits")
print("order-info = how much the previous word constrains the next.")
print("Natural languages: large gap. VMS: compare below.")

# ---- TEST 4: Line-as-a-functional-unit (LAAFU)
print("\n[4] LINE-AS-FUNCTIONAL-UNIT (layout-driven, not sentence-driven) --")
gallows = set('ktpf')
first_glyph = collections.Counter(); other_glyph = collections.Counter()
first_words_len = []; mid_words_len = []; last_words_len = []
lineinit_gallows = 0; lineinit_total = 0; body_gallows_words = 0; body_total = 0
for toks in para_lines:
    if len(toks) < 3: continue
    # line-initial vs rest: does first word start with a gallows more often?
    lineinit_total += 1
    if toks[0] and toks[0][0] in gallows: lineinit_gallows += 1
    for w in toks[1:]:
        body_total += 1
        if w and w[0] in gallows: body_gallows_words += 1
    first_words_len.append(len(toks[0]))
    last_words_len.append(len(toks[-1]))
    for w in toks[1:-1]: mid_words_len.append(len(w))
print(f"First word of line starts with gallows: {100*lineinit_gallows/lineinit_total:.1f}%")
print(f"Other words   start with gallows:       {100*body_gallows_words/body_total:.1f}%")
print(f"Mean length  first word={sum(first_words_len)/len(first_words_len):.2f}  "
      f"mid={sum(mid_words_len)/len(mid_words_len):.2f}  "
      f"last={sum(last_words_len)/len(last_words_len):.2f}")
# line-final glyph preference
linefinal = collections.Counter(toks[-1][-1] for toks in para_lines if toks and toks[-1])
print("Most common line-FINAL glyph:", ", ".join(f"{g}:{100*c/sum(linefinal.values()):.0f}%" for g, c in linefinal.most_common(5)))

# ---- TEST 5: labels vs paragraph vocabulary
print("\n[5] LABELS vs BODY TEXT -----------------------------------------")
para_set = set(para_tokens); label_set = set(label_tokens)
shared = label_set & para_set
print(f"Distinct label words: {len(label_set)} | also appear in body text: {len(shared)} ({100*len(shared)/len(label_set):.0f}%)")
lab_mean = sum(len(w) for w in label_tokens)/len(label_tokens)
print(f"Mean label-word length {lab_mean:.2f} vs body {sum(len(w) for w in para_tokens)/len(para_tokens):.2f}")
labc = collections.Counter(label_tokens)
print("Top label words:", ", ".join(f"{w}({c})" for w, c in labc.most_common(8)))

# ---- TEST 6: adjacent-word similarity ("ladder" / autocopying signature)
print("\n[6] ADJACENT-WORD SIMILARITY (the 'one-edit neighbour' anomaly) --")
def adj_stats(lines_lists, tokens):
    consec = []
    for toks in lines_lists:
        for a, b in zip(toks, toks[1:]):
            consec.append(levenshtein(a, b))
    # random baseline: random pairs from same token pool
    rnd = [levenshtein(random.choice(tokens), random.choice(tokens)) for _ in range(len(consec))]
    p1_consec = 100*sum(1 for d in consec if d == 1)/len(consec)
    p1_rnd = 100*sum(1 for d in rnd if d == 1)/len(rnd)
    return sum(consec)/len(consec), sum(rnd)/len(rnd), p1_consec, p1_rnd
for name, lns, toks in [('Voynich', para_lines, para_tokens)]:
    mc, mr, p1c, p1r = adj_stats(lns, toks)
    print(f"{name}: mean edit-dist adjacent={mc:.2f} vs random={mr:.2f}")
    print(f"   adjacent words differing by exactly 1 edit: {p1c:.1f}%  (random baseline {p1r:.1f}%)")
# Latin baseline for the same metric
lat_lines = [latin[i:i+8] for i in range(0, 8000, 8)]
mc, mr, p1c, p1r = adj_stats(lat_lines, latin[:20000])
print(f"Latin (control): adjacent 1-edit {p1c:.1f}% vs random {p1r:.1f}%")

# ---- TEST 7: Currier A vs B character entropy
print("\n[7] CURRIER A vs B (two scribal 'dialects') ----------------------")
for L in ['A', 'B']:
    toks = [w for lang, t, tks in all_lines if lang == L and t == 'P' for w in tks]
    a, h1, h2 = char_entropies(toks)
    print(f"  Currier {L}: {len(toks):6d} tokens  h1={h1:.3f}  h2={h2:.3f}")

# ---- TEST 8: directionality (forward vs reversed h2)
print("\n[8] DIRECTIONALITY (forward vs reversed conditional entropy) -----")
for name, toks in [('Voynich', para_tokens), ('Latin', latin), ('English', english)]:
    _, _, hf = char_entropies(toks, sample=S)
    _, _, hr = char_entropies([w[::-1] for w in toks], sample=S)
    print(f"  {name:8s} forward h2={hf:.3f}  reversed h2={hr:.3f}  diff={abs(hf-hr):.3f}")
print("\nDONE.")
