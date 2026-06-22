#!/usr/bin/env python3
"""(a) verbose-cipher mapping search  (b) per-section tests  (c) multilingual baselines.
Honest: reports whether an optimised mapping yields REAL words, not just n-gram mimicry."""
import re, math, collections, random, time
random.seed(7)

# ===================== load VMS with page->section (=$I) and locus type ============
lines = open('LSI_ivtff_0d.txt', encoding='latin-1').read().split('\n')
hdr_re = re.compile(r'^<(f[0-9]+[rv][0-9]*)>\s*<!(.*)>')
loc_re = re.compile(r'^<(f[0-9]+[rv][0-9]*)\.([0-9]+),([^;]*);H>\s+(.*?)\s*$')
page_sec = {}
for ln in lines:
    m = hdr_re.match(ln)
    if m:
        im = re.search(r'\$I=([A-Z])', m.group(2)); page_sec[m.group(1)] = im.group(1) if im else '?'
def clean(t): return re.sub(r'<[^>]*>', '', t).replace('!', '').replace('%', '').replace(',', '.')

# per (section, locus-type) line lists
sec_lines = collections.defaultdict(list)     # section -> list of token-lists (paragraph P only)
sec_labels = collections.defaultdict(list)    # section -> label tokens
para_lines = []
vms_tokens = []
for ln in lines:
    m = loc_re.match(ln)
    if not m: continue
    page, _, locus, text = m.groups()
    typ = locus[1] if len(locus) > 1 else '?'
    sec = page_sec.get(page, '?')
    toks = [w for w in clean(text).split('.') if w and not any(c in w for c in '?*@')]
    if not toks: continue
    if typ == 'P':
        sec_lines[sec].append(toks); para_lines.append(toks); vms_tokens += toks
    elif typ == 'L':
        sec_labels[sec] += toks

# ===================== comparators (c) ===========================================
def load(path, alpha=r'[a-z]'):
    s = open(path, encoding='utf-8', errors='ignore').read()
    a = re.search(r'\*\*\* START.*?\*\*\*', s); b = re.search(r'\*\*\* END.*?\*\*\*', s)
    if a: s = s[a.end():]
    if b: s = s[:b.start()]
    return [w for w in re.findall(alpha + '+', s.lower()) if 2 <= len(w) <= 20]
latin  = load('latin_raw.txt')                       # Caesar (no PG markers -> whole file)
latin  = [w for w in re.findall(r'[a-z]+', open('latin_raw.txt',encoding='utf-8',errors='ignore').read().lower()) if 2<=len(w)<=20]
english= load('english_raw.txt')
german = load('german_raw.txt', r'[a-zäöüß]')
italian= load('italian_raw.txt', r'[a-zàèéìòù]')
print("Corpus sizes:", {k: len(v) for k,v in [('VMS',vms_tokens),('Latin',latin),('English',english),('German',german),('Italian',italian)]})

def cond_h2(tokens, sample=30000):
    if sample and len(tokens) > sample: tokens = random.sample(tokens, sample)
    seq=[]
    for w in tokens: seq.append('#'); seq+=w
    seq.append('#')
    bi=collections.Counter(zip(seq,seq[1:])); fc=collections.Counter()
    for (a,b),c in bi.items(): fc[a]+=c
    B=sum(bi.values()); h=0
    for (a,b),c in bi.items(): h-=(c/B)*math.log2(c/fc[a])
    return h
def word_order_info(tokens, n=30000):
    t=tokens[:n]
    def ce(seq):
        bi=collections.Counter(zip(seq,seq[1:])); fc=collections.Counter()
        for (a,b),c in bi.items(): fc[a]+=c
        B=sum(bi.values()); h=0
        for (a,b),c in bi.items(): h-=(c/B)*math.log2(c/fc[a]);
        return h
    real=ce(t); sh=t[:]; random.shuffle(sh); return ce(sh)-real

print("\n[C] MULTILINGUAL BASELINES -------------------------------------------")
print(f"{'lang':9s} {'h2(char)':>9s} {'word-order-info(bits)':>22s}")
for name,toks in [('Voynich',vms_tokens),('Latin',latin),('Italian',italian),('German',german),('English',english)]:
    print(f"{name:9s} {cond_h2(toks):9.3f} {word_order_info(toks):22.2f}")

# ===================== (b) per-section tests 4-6 =================================
def levenshtein(a,b):
    if a==b: return 0
    if not a or not b: return len(a)+len(b)
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1): cur.append(min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
gallows=set('ktpf')
SEC_NAMES={'H':'Herbal','B':'Biological','P':'Pharma','S':'Stars/recipes','A':'Astro','C':'Cosmo','Z':'Zodiac','T':'Text'}
print("\n[B] PER-SECTION FINGERPRINT (is it one process across the book?) ------")
print(f"{'section':14s} {'nTok':>6s} {'h2':>5s} {'1stGallows%':>11s} {'bodyGall%':>9s} {'1edit%':>7s} {'rnd%':>5s} {'finalY%':>7s}")
for sec in ['H','B','P','S','A','C','Z']:
    lns=sec_lines.get(sec,[])
    toks=[w for l in lns for w in l]
    if len(toks)<400:
        print(f"{SEC_NAMES[sec]:14s} {len(toks):6d}  (too little paragraph text)")
        continue
    h2=cond_h2(toks)
    fi=sum(1 for l in lns if len(l)>=3 and l[0] and l[0][0] in gallows)
    fitot=sum(1 for l in lns if len(l)>=3)
    bg=sum(1 for l in lns if len(l)>=3 for w in l[1:] if w and w[0] in gallows)
    bgt=sum(len(l)-1 for l in lns if len(l)>=3)
    consec=[levenshtein(a,b) for l in lns for a,b in zip(l,l[1:])]
    p1=100*sum(1 for d in consec if d==1)/len(consec) if consec else 0
    rnd=[levenshtein(random.choice(toks),random.choice(toks)) for _ in range(len(consec))]
    p1r=100*sum(1 for d in rnd if d==1)/len(rnd) if rnd else 0
    fy=collections.Counter(l[-1][-1] for l in lns if l and l[-1])
    fyp=100*fy.get('y',0)/sum(fy.values())
    print(f"{SEC_NAMES[sec]:14s} {len(toks):6d} {h2:5.2f} {100*fi/fitot:11.1f} {100*bg/bgt:9.1f} {p1:7.1f} {p1r:5.1f} {fyp:7.1f}")
# labels per section
print("\n   label-vs-body overlap per section:")
allbody=set(vms_tokens)
for sec in ['H','B','P','A','C','Z']:
    labs=sec_labels.get(sec,[])
    if not labs: continue
    st=set(labs); sh=st&allbody
    print(f"   {SEC_NAMES[sec]:12s} {len(labs):4d} label-tokens, {len(st)} types, {100*len(sh)/len(st):3.0f}% also in body")

# ===================== (a) verbose-cipher mapping search =========================
print("\n[A] VERBOSE-CIPHER MAPPING SEARCH (can units->letters yield REAL words?) --")
# 1) BPE-merge VMS into ~N units
def bpe_merge(tokens, target_alpha):
    words=[list(w) for w in tokens]
    alpha=set(c for w in words for c in w)
    while len(alpha)<99:  # do merges until alphabet grows to target
        pairs=collections.Counter()
        for w in words:
            for a,b in zip(w,w[1:]): pairs[(a,b)]+=1
        if not pairs: break
        (a,b),_=pairs.most_common(1)[0]; merged=a+b
        for w in words:
            i=0
            while i<len(w)-1:
                if w[i]==a and w[i+1]==b: w[i:i+2]=[merged]
                else: i+=1
        alpha=set(c for w in words for c in w)
        if len(alpha)>=target_alpha: break
    return [tuple(w) for w in words], sorted(alpha, key=lambda u:-sum(1 for w in words for x in w if x==u))

def trigram_model(tokens):
    tri=collections.Counter(); bi=collections.Counter()
    for w in tokens:
        s='##'+w+'#'
        for i in range(len(s)-2):
            tri[s[i:i+3]]+=1; bi[s[i:i+2]]+=1
    V=len(set(''.join(tokens)))+1
    def logp(c3):
        return math.log((tri.get(c3,0)+0.1)/(bi.get(c3[:2],0)+0.1*V))
    return logp
def score(decoded_words, logp):
    tot=0.0; n=0
    for w in decoded_words:
        s='##'+w+'#'
        for i in range(len(s)-2): tot+=logp(s[i:i+3]); n+=1
    return tot/n   # mean log-prob per char (higher=better, less negative)

# search: map VMS units -> letters of target lang to maximise trigram score; then test real-word rate
def run_target(name, corpus):
    letters=sorted(set(''.join(corpus[:5000])))      # target alphabet
    K=len(letters)
    units_words, units = bpe_merge(vms_tokens, K)
    units=units[:K]
    uset=set(units)
    # keep only words fully in top-K units (drop rare units -> '?')
    sample_words=[w for w in units_words if all(u in uset for u in w)]
    random.shuffle(sample_words); search=sample_words[:4000]
    logp=trigram_model(corpus)
    wordset=set(w for w in corpus if len(w)>=3)
    # init mapping by frequency rank alignment
    lf=[l for l,_ in collections.Counter(''.join(corpus)).most_common() if l in letters]
    mapping={u:(lf[i] if i<len(lf) else letters[i%K]) for i,u in enumerate(units)}
    def decode(words): return [''.join(mapping[u] for u in w) for w in words]
    cur=score(decode(search), logp); best=cur; bestmap=dict(mapping)
    t0=time.time(); it=0
    while time.time()-t0<25 and it<4000:
        it+=1
        a,b=random.sample(units,2); mapping[a],mapping[b]=mapping[b],mapping[a]
        s=score(decode(search), logp)
        if s>=cur or random.random()<math.exp((s-cur)*30):
            cur=s
            if s>best: best=s; bestmap=dict(mapping)
        else:
            mapping[a],mapping[b]=mapping[b],mapping[a]
    mapping=bestmap
    dec_all=decode([w for w in units_words if all(u in uset for u in w)])
    real=sum(1 for w in dec_all if len(w)>=3 and w in wordset)
    denom=sum(1 for w in dec_all if len(w)>=3)
    # baselines: real-word rate of the language vs itself, and random mapping
    self_real=sum(1 for w in random.sample(corpus,min(3000,len(corpus))) if len(w)>=3 and w in wordset)/ \
              max(1,sum(1 for w in random.sample(corpus,min(3000,len(corpus))) if len(w)>=3))
    # self-perplexity of language and of best-decoded
    lang_score=score(random.sample(corpus,3000), logp)
    print(f" {name:8s}: best mean-logp/char decoded={best:6.2f}  (real {name} text={lang_score:6.2f})")
    print(f"           decoded tokens that are REAL {name} words: {100*real/denom:4.1f}%   "
          f"(real {name} self-rate ~{100*self_real:.0f}%)")
    return 100*real/denom

print(" Optimising unit->letter bijection to MAXIMISE trigram fit, then checking lexicon:")
rates={}
for nm,corp in [('Latin',latin),('Italian',italian),('German',german)]:
    rates[nm]=run_target(nm,corp)
print("\n VERDICT: if the verbose-cipher hypothesis were right for one of these")
print(" languages, that column would show a high REAL-word %. Compare to ~self-rate.")
print("DONE.")
