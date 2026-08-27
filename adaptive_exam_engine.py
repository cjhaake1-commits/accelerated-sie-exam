"""Balanced exam sampler that treats scenario variants as the SAME concept.
Prevents cosmetic rewording from appearing as new questions and spreads questions across chapters/terms.
"""
import random
from finra_style_engine import build_pool

def _identity(q):
    # Scenario variants preserve chapter + term + rationale, so they count as one underlying item.
    return (q.get("chapter"), q.get("term"), q.get("why"))

def unique_pool(chapters, variants=16):
    raw=build_pool(chapters, variants)
    groups={}
    for q in raw:
        groups.setdefault(_identity(q), []).append(q)
    # Pick one random presentation of each underlying concept per test.
    items=[random.choice(v) for v in groups.values()]
    random.shuffle(items)
    return items

def balanced_sample(chapters,n,history=None):
    """Spread questions across chapters and avoid prior underlying items when possible."""
    history=set(history or [])
    pool=unique_pool(chapters,24)
    fresh=[q for q in pool if _identity(q) not in history]
    used=[]
    by_ch={ch:[] for ch in chapters}
    for q in fresh: by_ch.setdefault(q["chapter"],[]).append(q)
    # Round-robin forces chapter coverage instead of random clustering.
    while len(used)<n and any(by_ch.values()):
        for ch in chapters:
            if by_ch.get(ch) and len(used)<n:
                q=random.choice(by_ch[ch]); by_ch[ch].remove(q); used.append(q)
    # If history exhausted the bank, reuse least recently excluded unique concepts rather than stem clones.
    if len(used)<n:
        remaining=[q for q in pool if _identity(q) not in {_identity(x) for x in used}]
        random.shuffle(remaining); used.extend(remaining[:n-len(used)])
    # Last-resort fill only if a chapter bank is genuinely too small.
    if len(used)<n:
        raw=build_pool(chapters,32); random.shuffle(raw)
        for q in raw:
            if len(used)>=n: break
            if q["q"] not in {x["q"] for x in used}: used.append(q)
    random.shuffle(used)
    return used[:n]

def identities(items): return [_identity(q) for q in items]
