#!/usr/bin/env python3
"""Reverse-engineer the Voynich SCRIPT (not its meaning): learn an interpretable
finite-state grammar over glyph-group 'atoms', then validate by generating a synthetic
corpus and checking it is statistically indistinguishable from the real manuscript."""
import re, math, collections, random, json
random.seed(17)

# ---- load real corpus ----
L = open('LSI_ivtff_0d.txt', encoding='latin-1').read().split('\n')
loc = re.compile(r'^<f[0-9]+[rv][0-9]*\.[0-9]+,[^;]*;H>\s+(.*?)\s*$')
clean = lambda t: re.sub(r'<[^>]*>', '', t).replace('!','').replace('%','').replace(',','.')
real = [w for ln in L if (m:=loc.match(ln)) for w in clean(m.group(1)).split('.') if w and not any(c in w for c in '?*@')]
real_types = collections.Counter(real)
N = len(real)

# ---- atom tokenizer: greedy longest-match over the known Voynich multigraph inventory ----
ATOMS = ['cfhaiin','ckhaiin','cthaiin','cphaiin','cthar','ckhar','cthy','ckhy',
         'cth','ckh','cph','cfh','qok','qot','qop','qof','sh','ch',
         'aiin','aiir','aiii','aii','ain','ai','iin','iir','iii','ii',
         'eee','ee','dy','dai','dal','dar','dam','dan',
         'ok','ot','op','of','qo','ol','or','al','ar','am','an','od','os','ot',
         'q','o','y','d','l','r','s','n','m','k','t','p','f','e','a','i','g','x']
ATOMS = sorted(set(ATOMS), key=len, reverse=True)
def tok(w):
    out=[]; i=0
    while i < len(w):
        for a in ATOMS:
            if w.startswith(a, i):
                out.append(a); i += len(a); break
        else:
            out.append(w[i]); i += 1
    return out

# ---- learn the grammar: order-2 Markov over atoms (state = previous TWO atoms) ----
# This IS a probabilistic finite-state automaton. States/transitions = the "rules".
def build(order):
    model = collections.defaultdict(collections.Counter)
    for w in real:
        seq = ['^']*order + tok(w) + ['$']
        for i in range(order, len(seq)):
            ctx = tuple(seq[i-order:i]); model[ctx][seq[i]] += 1
    return model
def generate(model, order, n):
    out=[]
    for _ in range(n):
        seq=['^']*order
        for _ in range(40):
            ctx=tuple(seq[-order:]); dist=model.get(ctx)
            if not dist: break
            atoms,wts=zip(*dist.items()); nxt=random.choices(atoms,wts)[0]
            if nxt=='$': break
            seq.append(nxt)
        out.append(''.join(seq[order:]))
    return [w for w in out if w]

def h2(tokens):
    seq=[]
    for w in tokens: seq.append('#'); seq+=w
    seq.append('#')
    bi=collections.Counter(zip(seq,seq[1:])); fc=collections.Counter()
    for (a,b),c in bi.items(): fc[a]+=c
    B=sum(bi.values()); h=0
    for (a,b),c in bi.items(): h-=(c/B)*math.log2(c/fc[a])
    return h
def zipf_slope(counter):
    rb=counter.most_common(); import statistics
    xs=[math.log(r) for r in range(1,min(500,len(rb))+1)]; ys=[math.log(c) for _,c in rb[:500]]
    mx=statistics.mean(xs);my=statistics.mean(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)

print("="*66)
print("REVERSE-ENGINEERING THE VOYNICH SCRIPT (generative grammar)")
print("="*66)
print(f"Real corpus: {N:,} tokens, {len(real_types):,} types")
mean_atoms = sum(len(tok(w)) for w in real)/N
print(f"Mean atoms/word under learned tokenizer: {mean_atoms:.2f}  (vs {sum(len(w) for w in real)/N:.2f} raw glyphs)")

results={'real':{},'gen':{}}
for order in (2, 3):
    model = build(order)
    gen = generate(model, order, N)
    gtypes = collections.Counter(gen)
    prec = 100*sum(1 for w in gen if w in real_types)/len(gen)        # generated words that ARE real
    # recall: real token-mass whose word-form the model produced in this sample
    recall = 100*sum(c for w,c in real_types.items() if w in gtypes)/N
    print(f"\n--- ORDER-{order} finite-state grammar ({len(model)} states) ---")
    print(f"  generated {len(gen):,} words")
    print(f"  PRECISION  (generated words that are real Voynich words): {prec:4.1f}%")
    print(f"  RECALL     (real token-mass the grammar reproduced)     : {recall:4.1f}%")
    print(f"  h2:        real {h2(real):.2f}  vs  synthetic {h2(gen):.2f}")
    print(f"  Zipf slope: real {zipf_slope(real_types):.2f}  vs  synthetic {zipf_slope(gtypes):.2f}")
    print(f"  mean len:   real {sum(len(w) for w in real)/N:.2f}  vs  synthetic {sum(len(w) for w in gen)/len(gen):.2f}")
    rt=[w for w,_ in real_types.most_common(15)]; gt=[w for w,_ in gtypes.most_common(15)]
    print(f"  top-15 real : {' '.join(rt)}")
    print(f"  top-15 synth: {' '.join(gt)}")
    print(f"  top-15 overlap: {len(set(rt)&set(gt))}/15")
    if order==3:
        results['gen']={'lengths':{str(k):sum(1 for w in gen if len(w)==k)/len(gen) for k in range(1,16)},
                        'zipf':zipf_slope(gtypes),'h2':h2(gen),'prec':prec,'recall':recall,
                        'top':[w for w,_ in gtypes.most_common(20)]}
        results['real']={'lengths':{str(k):sum(1 for w in real if len(w)==k)/N for k in range(1,16)},
                         'zipf':zipf_slope(real_types),'h2':h2(real),
                         'top':[w for w,_ in real_types.most_common(20)]}

# ---- distil the human-readable GRAMMAR (dominant transitions of the order-1 machine) ----
print("\n" + "="*66)
print("THE DISTILLED GRAMMAR (most probable transitions, order-1 view)")
print("="*66)
m1 = build(1)
def show(ctx, label):
    d=m1.get((ctx,))
    if d:
        tot=sum(d.values())
        top=", ".join(f"{a}:{100*c/tot:.0f}%" for a,c in d.most_common(6))
        print(f"  {label:16s} -> {top}")
show('^','WORD START')
for a in ['qo','ch','sh','o','ot','ok']: show(a, f"after '{a}'")
print("  (e.g. words begin overwhelmingly with qo/ch/sh/o; gallows k/t follow qo/o;")
print("   benches feed into e/ee then d/aiin; words end on y/n/l/r/m. This positional")
print("   pipeline is the slot grammar, recovered as an automaton.)")

json.dump(results, open('regen.json','w'), indent=1)
print("\nsaved regen.json. DONE.")
