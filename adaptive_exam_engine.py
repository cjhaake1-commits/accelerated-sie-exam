"""Balanced SIE sampler with stable item identity and application-first selection.
Quality rule: never manufacture test length by repeating the same underlying concept with a cosmetic rewrite.
"""
import random
import hashlib
from finra_style_engine import build_pool


def _identity(q):
    """Prefer a stable item id. Fall back to a content fingerprint for legacy items."""
    if q.get("item_id"):
        return q["item_id"]
    raw="|".join(str(q.get(k,"")) for k in ("chapter","term","q","a"))
    return "legacy-"+hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _concept(q):
    """Concept identity suppresses cosmetic variants while allowing genuinely different applications."""
    return (q.get("chapter"),q.get("term"),q.get("concept_id") or q.get("why"))


def unique_pool(chapters,variants=20):
    raw=build_pool(chapters,variants)
    groups={}
    for q in raw:
        groups.setdefault(_concept(q),[]).append(q)
    items=[]
    for group in groups.values():
        premium=[q for q in group if q.get("premium")]
        application=[q for q in group if q.get("style") in ("application","scenario")]
        items.append(random.choice(premium or application or group))
    random.shuffle(items)
    return items


def balanced_sample(chapters,n,history=None):
    """Return up to n distinct concepts, spread across chapters.
    Premium/application items win ties. Recently seen items are deferred until unseen inventory is exhausted.
    """
    history=set(history or [])
    pool=unique_pool(chapters,28)
    fresh=[q for q in pool if _identity(q) not in history]
    stale=[q for q in pool if _identity(q) in history]

    def rank(q):
        return (2 if q.get("premium") else 1 if q.get("style") in ("application","scenario") else 0,q.get("difficulty",1),random.random())

    def round_robin(source,target,seen_concepts):
        by_ch={ch:[] for ch in chapters}
        for q in source:by_ch.setdefault(q.get("chapter"),[]).append(q)
        for qs in by_ch.values():qs.sort(key=rank,reverse=True)
        while len(target)<n and any(by_ch.values()):
            progressed=False
            for ch in chapters:
                if len(target)>=n:break
                bucket=by_ch.get(ch,[])
                while bucket:
                    q=bucket.pop(0);concept=_concept(q)
                    if concept not in seen_concepts:
                        target.append(q);seen_concepts.add(concept);progressed=True;break
            if not progressed:break
        return target,seen_concepts

    chosen=[];seen=set()
    chosen,seen=round_robin(fresh,chosen,seen)
    if len(chosen)<n:chosen,seen=round_robin(stale,chosen,seen)
    random.shuffle(chosen)
    return chosen[:n]


def identities(items):return [_identity(q) for q in items]
