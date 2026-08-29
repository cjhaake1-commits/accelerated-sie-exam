"""Commercial QA audit for the generated SIE question bank.
This gate distinguishes automated structural QA from independent content review.
Passing automated QA alone never means an item is production-approved.
"""
from collections import Counter,defaultdict
from finra_style_engine import build_pool
from question_metadata import quality_flags
from curriculum import SECTION_CHAPTERS
from source_registry import SOURCE_REGISTRY

APPROVED_REVIEW_STATES={"independently-reviewed","production-approved"}


def audit_bank():
    pool=build_pool(list(range(1,21)),28);unique={q.get("item_id",q.get("q")):q for q in pool}
    flags=Counter();by_ch=Counter();by_style=Counter();by_difficulty=Counter();by_review=Counter();terms=defaultdict(set);concepts=set();objectives=set();bad_sources=0
    for q in unique.values():
        by_ch[q.get("chapter")]+=1;by_style[q.get("style","unknown")]+=1;by_difficulty[q.get("difficulty",1)]+=1;by_review[q.get("review_status","missing")]+=1
        terms[q.get("chapter")].add(q.get("term"));concepts.add(q.get("concept_id"));objectives.add(q.get("objective_id"))
        if any(k not in SOURCE_REGISTRY for k in q.get("source_keys",())):bad_sources+=1
        for flag in quality_flags(q):flags[flag]+=1
    section_counts={sec:sum(by_ch[ch] for ch in chs) for sec,chs in SECTION_CHAPTERS.items()}
    reviewed=sum(by_review[s] for s in APPROVED_REVIEW_STATES)
    return {"total_generated":len(pool),"unique_items":len(unique),"unique_concepts":len({x for x in concepts if x}),"unique_objectives":len({x for x in objectives if x}),"by_chapter":dict(by_ch),"by_style":dict(by_style),"by_difficulty":dict(by_difficulty),"by_review_status":dict(by_review),"independently_reviewed":reviewed,"unique_terms_by_chapter":{ch:len(v) for ch,v in terms.items()},"section_inventory":section_counts,"unknown_source_keys":bad_sources,"flags":dict(flags)}


def commercial_gate(report):
    """Return paid-launch blockers. Automated QA clearance is not independent review."""
    blockers=[]
    if report["unique_items"]<300:blockers.append("Expand to at least 300 genuinely unique QA-cleared items before paid launch; market-depth target remains substantially higher.")
    if report.get("unique_concepts",0)<200:blockers.append("Expand materially distinct scenario families; cosmetic stem variants do not count as bank depth.")
    if report["by_style"].get("recall",0)>report["unique_items"]*.30:blockers.append("Reduce recall items below 30% of the QA-cleared bank.")
    serious=sum(v for k,v in report["flags"].items() if k not in ("recall_item",))
    if serious:blockers.append(f"Resolve {serious} structural/rationale/provenance QA flags.")
    if report.get("unknown_source_keys",0):blockers.append("Resolve all unregistered provenance source keys.")
    if report.get("independently_reviewed",0)<report["unique_items"]:blockers.append("Independent content review is incomplete; draft or automated-QA items cannot be marketed as reviewed or production-approved.")
    for ch in range(1,21):
        if report["by_chapter"].get(ch,0)<8:blockers.append(f"Legacy chapter {ch} has fewer than 8 unique items; fill coverage while migrating to the four-function commercial curriculum.")
    return blockers
