"""Commercial QA audit for the generated SIE question bank."""
from collections import Counter,defaultdict
from finra_style_engine import build_pool
from question_metadata import quality_flags
from curriculum import SECTION_CHAPTERS


def audit_bank():
    pool=build_pool(list(range(1,21)),28)
    unique={q.get("item_id",q.get("q")):q for q in pool}
    flags=Counter();by_ch=Counter();by_style=Counter();by_difficulty=Counter();terms=defaultdict(set)
    for q in unique.values():
        by_ch[q.get("chapter")]+=1;by_style[q.get("style","unknown")]+=1;by_difficulty[q.get("difficulty",1)]+=1
        terms[q.get("chapter")].add(q.get("term"))
        for flag in quality_flags(q):flags[flag]+=1
    section_counts={sec:sum(by_ch[ch] for ch in chs) for sec,chs in SECTION_CHAPTERS.items()}
    return {"total_generated":len(pool),"unique_items":len(unique),"by_chapter":dict(by_ch),"by_style":dict(by_style),"by_difficulty":dict(by_difficulty),"unique_terms_by_chapter":{ch:len(v) for ch,v in terms.items()},"section_inventory":section_counts,"flags":dict(flags)}


def commercial_gate(report):
    blockers=[]
    if report["unique_items"]<300:blockers.append("Expand to at least 300 genuinely unique reviewed items before paid launch.")
    if report["by_style"].get("recall",0)>report["unique_items"]*.30:blockers.append("Reduce recall items below 30% of the reviewed bank.")
    serious=sum(v for k,v in report["flags"].items() if k not in ("recall_item",))
    if serious:blockers.append(f"Resolve {serious} structural/rationale QA flags.")
    for ch in range(1,21):
        if report["by_chapter"].get(ch,0)<8:blockers.append(f"Chapter {ch} has fewer than 8 unique items.")
    return blockers
