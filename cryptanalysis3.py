#!/usr/bin/env python3
"""Reverse/mirror tests; multilingual sweep (+Finnish, +Sanskrit);
(1) slot-position-dependent cipher search; (2) finite-state generator test.
Dumps results.json for figures. Honest: real-word lexicon is the judge."""
import re, math, collections, random, time, json
random.seed(11)

# ---------- load VMS ----------
L = open('LSI_ivtff_0d.txt', encoding='latin-1').read().split('\n')
loc = re.compile(r'^<f[0-9]+[rv][0-9]*\.[0-9]+,[^;]*;H>\s+(.*?)\s*$')
clean = lambda t: re.sub(r'<[^>]*>', '', t).replace('!', '').replace('%', '').replace(',', '.')
vms_lines = []
for ln in L:
    m = loc.match(ln)
    if m:
        toks = [w for w in clean(m.group(1)).split('.') if w and not any(c in w for c in '?*@')]
        if toks: vms_lines.append(toks)
vms = [w for l in vms_lines for w in l]

# ---------- comparators ----------
def load(path, alpha):
    s = open(path, encoding='utf-8', errors='ignore').read()
    a = re.search(r'\*\*\* START.*?\*\*\*', s); b = re.search(r'\*\*\* END.*?\*\*\*', s)
    if a: s = s[a.end():]
    if b: s = s[:b.start()]
    return [w for w in re.findall(alpha + '+', s.lower()) if 2 <= len(w) <= 22]
def load_sanskrit():
    s = open('sanskrit_raw.txt', encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<[^>]+>', ' ', s)
    return [w for w in re.findall(r'[a-zāīūṛṝḷṅñṭḍṇśṣṁṃḥ]+', t.lower()) if 2 <= len(w) <= 22]
latin = [w for w in re.findall(r'[a-z]+', open('latin_raw.txt',encoding='utf-8',errors='ignore').read().lower()) if 2<=len(w)<=22]
english = load('english_raw.txt', r'[a-z]')
german = load('german_raw.txt', r'[a-zäöüß]')
italian = load('italian_raw.txt', r'[a-zàèéìòù]')
finnish = load('finnish_raw.txt', r'[a-zäöå]')
sanskrit = load_sanskrit()
CORP = {'Voynich':vms,'Latin':latin,'Italian':italian,'German':german,'English':english,'Finnish':finnish,'Sanskrit':sanskrit}
print("sizes:", {k:len(v) for k,v in CORP.items()})
results = {'sizes':{k:len(v) for k,v in CORP.items()}}

# ---------- helpers ----------
def cond_h2(tokens, sample=30000):
    if sample and len(tokens)>sample: tokens=random.sample(tokens,sample)
    seq=[]
    for w in tokens: seq.append('#'); seq+=w
    seq.append('#')
    bi=collections.Counter(zip(seq,seq[1:])); fc=collections.Counter()
    for (a,b),c in bi.items(): fc[a]+=c
    B=sum(bi.values()); h=0
    for (a,b),c in bi.items(): h-=(c/B)*math.log2(c/fc[a])
    return h
def order_info(tokens,n=30000):
    t=tokens[:n]
    def ce(seq):
        bi=collections.Counter(zip(seq,seq[1:])); fc=collections.Counter()
        for (a,b),c in bi.items(): fc[a]+=c
        B=sum(bi.values()); h=0
        for (a,b),c in bi.items(): h-=(c/B)*math.log2(c/fc[a])
        return h
    real=ce(t); sh=t[:]; random.shuffle(sh); return ce(sh)-real

# ===== [C] multilingual sweep incl. Finnish + Sanskrit =====
print("\n[C] LANGUAGE SWEEP -------------------------------------------------")
print(f"{'lang':9s} {'h2':>6s} {'order-info':>10s} {'meanLen':>8s}")
sweep={}
for k,v in CORP.items():
    h2=cond_h2(v); oi=order_info(v); ml=sum(len(w) for w in v)/len(v)
    sweep[k]={'h2':h2,'order_info':oi,'mean_len':ml}
    print(f"{k:9s} {h2:6.3f} {oi:10.2f} {ml:8.2f}")
results['sweep']=sweep
# word-length distributions (for figure)
results['lengths']={k:{L:sum(1 for w in v if len(w)==L)/len(v) for L in range(1,16)} for k,v in CORP.items()}

# ===== REVERSE / MIRROR tests =====
print("\n[R] REVERSE / MIRROR ANALYSIS -------------------------------------")
firstg=collections.Counter(w[0] for w in vms)
lastg=collections.Counter(w[-1] for w in vms)
Nf=sum(firstg.values()); Nl=sum(lastg.values())
allg=set(firstg)|set(lastg)
kl=sum((firstg[g]/Nf)*math.log2((firstg[g]/Nf)/(lastg[g]/Nl)) for g in allg if firstg[g] and lastg[g])
print(f"Word-initial top glyphs: {', '.join(f'{g}:{100*c/Nf:.0f}%' for g,c in firstg.most_common(5))}")
print(f"Word-final   top glyphs: {', '.join(f'{g}:{100*c/Nl:.0f}%' for g,c in lastg.most_common(5))}")
print(f"KL(initial || final) = {kl:.2f} bits  -> ends are very different => directional, not symmetric")
results['reverse']={'first':dict(firstg.most_common(6)),'last':dict(lastg.most_common(6)),'kl':kl}

# ===== verbose-cipher mapping machinery (units) =====
def bpe(tokens,K):
    words=[list(w) for w in tokens]; alpha=set(c for w in words for c in w)
    while len(alpha)<K:
        pr=collections.Counter()
        for w in words:
            for a,b in zip(w,w[1:]): pr[(a,b)]+=1
        if not pr: break
        (a,b),_=pr.most_common(1)[0]; mg=a+b
        for w in words:
            i=0
            while i<len(w)-1:
                if w[i]==a and w[i+1]==b: w[i:i+2]=[mg]
                else: i+=1
        alpha=set(c for w in words for c in w)
    return [tuple(w) for w in words], sorted(alpha,key=lambda u:-sum(1 for w in words for x in w if x==u))
def trigram(tokens):
    tri=collections.Counter(); bi=collections.Counter(); V=len(set(''.join(tokens)))+1
    for w in tokens:
        s='##'+w+'#'
        for i in range(len(s)-2): tri[s[i:i+3]]+=1; bi[s[i:i+2]]+=1
    return lambda c3: math.log((tri.get(c3,0)+0.1)/(bi.get(c3[:2],0)+0.1*V))
def score(words,lp):
    tot=0;n=0
    for w in words:
        s='##'+w+'#'
        for i in range(len(s)-2): tot+=lp(s[i:i+3]); n+=1
    return tot/max(n,1)

# ===== (1) SLOT-POSITION-DEPENDENT cipher search =====
print("\n[1] SLOT-POSITION-DEPENDENT CIPHER (context-sensitive variant) -----")
def zone(word_units):
    n=len(word_units); out=[]
    for i,u in enumerate(word_units):
        if n<=2: z=1
        elif i< n/3: z=0
        elif i>=2*n/3: z=2
        else: z=1
        out.append((u,z))
    return out
def run_slot(name, corpus, slotted):
    letters=sorted(set(''.join(corpus[:5000]))); K=len(letters)
    uw,units=bpe(vms,K); units=units[:K]; uset=set(units)
    words=[w for w in uw if all(u in uset for u in w) and sum(len(u) for u in w)>=3]
    random.shuffle(words); search=words[:3000]
    lp=trigram(corpus); wordset=set(w for w in corpus if len(w)>=3)
    nz=3 if slotted else 1
    lf=[l for l,_ in collections.Counter(''.join(corpus)).most_common() if l in letters]
    mp={z:{u:(lf[i] if i<len(lf) else letters[i%K]) for i,u in enumerate(units)} for z in range(nz)}
    def dec(ws):
        out=[]
        for w in ws:
            out.append(''.join(mp[(z if slotted else 0)][u] for u,z in zone(list(w))))
        return out
    cur=score(dec(search),lp); best=cur; bestmp={z:dict(mp[z]) for z in mp}
    t0=time.time(); it=0
    while time.time()-t0<22 and it<6000:
        it+=1; z=random.randrange(nz); a,b=random.sample(units,2)
        mp[z][a],mp[z][b]=mp[z][b],mp[z][a]
        s=score(dec(search),lp)
        if s>=cur or random.random()<math.exp((s-cur)*30):
            cur=s
            if s>best: best=s; bestmp={zz:dict(mp[zz]) for zz in mp}
        else: mp[z][a],mp[z][b]=mp[z][b],mp[z][a]
    mp=bestmp
    decoded=dec(words)
    real=sum(1 for w in decoded if len(w)>=3 and w in wordset)
    den=sum(1 for w in decoded if len(w)>=3)
    return best, 100*real/den
for nm in ['Latin','Sanskrit']:
    b0,r0=run_slot(nm,CORP[nm],False)
    b1,r1=run_slot(nm,CORP[nm],True)
    print(f"  {nm:8s}: single-map fit={b0:.2f} real={r0:4.1f}%   |  3-slot fit={b1:.2f} real={r1:4.1f}%")
    results.setdefault('slot',{})[nm]={'single_fit':b0,'single_real':r0,'slot_fit':b1,'slot_real':r1}

# ===== (2) FINITE-STATE GENERATOR test =====
print("\n[2] FINITE-STATE / TEMPLATIC GENERATION TEST ----------------------")
# (2a) held-out char predictability: order-2 model cross-entropy on held-out word tokens
def heldout_bits(tokens):
    random.shuffle(tokens); k=int(len(tokens)*0.8); tr,te=tokens[:k],tokens[k:]
    tri=collections.Counter(); bi=collections.Counter(); uni=collections.Counter()
    chars=set()
    for w in tr:
        s='##'+w+'#'
        for c in s: uni[c]+=1; chars.add(c)
        for i in range(len(s)-1): bi[s[i:i+2]]+=1
        for i in range(len(s)-2): tri[s[i:i+3]]+=1
    V=len(chars)
    tot=0;n=0;tot0=0
    U=sum(uni.values())
    for w in te:
        s='##'+w+'#'
        for i in range(len(s)-2):
            p=(tri.get(s[i:i+3],0)+0.5)/(bi.get(s[i:i+2],0)+0.5*V)
            tot-=math.log2(p); n+=1
        for c in w+'#':
            tot0-=math.log2((uni.get(c,0)+0.5)/(U+0.5*V))
    return tot/n, tot0/max(1,sum(len(w)+1 for w in te))
print("  Held-out word predictability (order-2 char model):")
print(f"  {'lang':9s} {'order2 bits/char':>16s} {'unigram bits':>13s} {'%uncertainty removed':>20s}")
for k in ['Voynich','Latin','Sanskrit','Finnish','English']:
    h2c,h0c=heldout_bits(CORP[k][:30000])
    print(f"  {k:9s} {h2c:16.3f} {h0c:13.3f} {100*(h0c-h2c)/h0c:19.1f}%")
    results.setdefault('predict',{})[k]={'order2':h2c,'order0':h0c}

# (2b) factored independent-slot generator: can prefix2 x middle x suffix2 (sampled
#      independently) regenerate the real lexicon? fidelity = token mass of real words covered
def factored_fidelity(tokens):
    types=collections.Counter(tokens); N=sum(types.values())
    pre=collections.Counter(); suf=collections.Counter(); mid=collections.Counter()
    for w,c in types.items():
        p=w[:2]; s=w[-2:]; m=w[2:-2]
        pre[p]+=c; suf[s]+=c; mid[m]+=c
    def samp(dist):
        items,wts=zip(*dist.items()); return random.choices(items,wts,k=1)[0]
    gen=collections.Counter()
    for _ in range(40000):
        gen[samp(pre)+samp(mid)+samp(suf)]+=1
    real_types=set(types)
    covered_types=sum(1 for w in gen if w in real_types)
    # token mass of real corpus reproduced by generator's support
    gensupport=set(gen)
    mass=sum(c for w,c in types.items() if w in gensupport)/N
    return 100*covered_types/len(gen), 100*mass
print("\n  Independent-slot generator (prefix2 x middle x suffix2):")
print(f"  {'lang':9s} {'gen words that are real types':>30s} {'real token-mass reproduced':>27s}")
for k in ['Voynich','Latin','Sanskrit','Finnish']:
    ct,mass=factored_fidelity(CORP[k][:30000])
    print(f"  {k:9s} {ct:29.1f}% {mass:26.1f}%")
    results.setdefault('factored',{})[k]={'gen_real':ct,'mass':mass}

json.dump(results, open('results.json','w'), indent=1)
print("\nsaved results.json. DONE.")
