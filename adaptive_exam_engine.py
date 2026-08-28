"""Balanced SIE sampler that treats cosmetic scenario variants as the SAME item.
Quality rule: never manufacture test length by repeating the same underlying concept with a new prefix.
Application/scenario items are preferred over pure recall when both are available.
"""
import random
from finra_style_engine import build_pool

def _identity(q):
    return (q.get("chapter"), q.get("term"), q.get("why"))

def unique_pool(chapters, variants=20):
    raw=build_pool(chapters, variants)
    groups={}
    for q in raw:
        groups.setdefault(_identity(q), []).append(q)
    items=[]
    for variants_for_concept in groups.values():
        application=[q for q in variants_for_concept if q.get("style") in ("application","scenario")]
        items.append(random.choice(application or variants_for_concept))
    random.shuffle(items)
    return items

def balanced_sample(chapters,n,history=None):
    """Return up to n DISTINCT underlying concepts.
    Spread questions across chapters, suppress recently seen concepts, and prefer application items.
    If the bank does not contain n genuinely distinct concepts, return fewer questions rather than clones.
    """
    history=set(history or [])
    pool=unique_pool(chapters,28)
    fresh=[q for q in pool if _identity(q) not in history]
    stale=[q for q in pool if _identity(q) in history]

    def round_robin(source, target, seen):
        by_ch={ch:[] for ch in chapters}
        for q in source:
            if _identity(q) not in seen:
                by_ch.setdefault(q["chapter"],[]).append(q)
        for qs in by_ch.values(): random.shuffle(qs)
        while len(target)<n and any(by_ch.values()):
            for ch in chapters:
                if len(target)>=n: break
                if by_ch.get(ch):
                    q=by_ch[ch].pop()
                    ident=_identity(q)
                    if ident not in seen:
                        target.append(q);seen.add(ident)
        return target,seen

    chosen=[];seen=set()
    chosen,seen=round_robin(fresh,chosen,seen)
    # Only reuse a previously seen concept after all unseen concepts are exhausted,
    # and still never repeat an underlying concept inside the same sitting.
    if len(chosen)<n:
        chosen,seen=round_robin(stale,chosen,seen)
    random.shuffle(chosen)
    return chosen[:n]

def identities(items): return [_identity(q) for q in items]
