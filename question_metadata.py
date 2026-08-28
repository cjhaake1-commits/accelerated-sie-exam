"""Commercial question-bank metadata and QA helpers.
Production items must be independently authored from approved public-source objectives/rules.
No item is represented as a live FINRA question.
"""
from datetime import date
import hashlib
import re
from curriculum import CHAPTERS
from source_registry import SOURCE_REGISTRY

BANK_VERSION="2026.08.28-cleanroom.2"
DEFAULT_SOURCE_KEYS=("FINRA_SIE_OUTLINE","FINRA_RULES","SEC_INVESTOR")


def _slug(value):return re.sub(r"[^A-Z0-9]+","-",str(value).upper()).strip("-")
def _digest(value,n=10):return hashlib.sha1(str(value).encode("utf-8")).hexdigest()[:n].upper()
def objective_id(q):return f"SIE-CH{int(q.get('chapter',0)):02d}-{_slug(q.get('term','concept'))[:48]}"
def concept_id(q):
    """Scenario-family identity: cosmetic rewrites collapse; materially different applications survive."""
    family=q.get("scenario_family") or q.get("why") or q.get("term") or q.get("q") or "concept"
    return f"{objective_id(q)}-F{_digest(family,8)}"
def item_id(q):
    raw="|".join(str(q.get(k,"")) for k in ("chapter","term","q","a"))
    return f"{objective_id(q)}-{_digest(raw,10)}"

def infer_difficulty(q):
    if q.get("difficulty") is not None:return int(q["difficulty"])
    text=(q.get('q','')+' '+q.get('why','')).lower()
    if any(x in text for x in ['calculate','approximately','breakeven','current yield','conversion ratio','most appropriate','best explains','except','not true','not accurate']):return 3
    if q.get('style') in ('application','scenario'):return 2
    return 1

def _term_definition(ch,choice):
    for term,definition in CHAPTERS.get(ch,{}).get('cards',[]):
        if choice.strip().lower()==term.strip().lower():return definition
    return None

def option_rationales(q):
    out={};answer=q.get('a');why=q.get('why','');ch=q.get('chapter');supplied=q.get("distractor_rationales",{})
    for choice in q.get('c',[]):
        if choice==answer:out[choice]=why or 'This choice best matches the controlling facts and rule.';continue
        if choice in supplied:out[choice]=supplied[choice];continue
        d=_term_definition(ch,choice)
        if d:out[choice]=f"Not best here. {choice} is a different concept: {d} The controlling facts point instead to {q.get('term','the tested concept')}."
        else:out[choice]=f"Not best here. This choice misses the controlling fact or distinction. Contrast it directly with {q.get('term','the tested concept')}."
    return out

def enrich(q,review_status="cleanroom-draft"):
    item=dict(q);source_keys=tuple(item.get("source_keys") or DEFAULT_SOURCE_KEYS)
    item.setdefault('objective_id',objective_id(item));item.setdefault('concept_id',concept_id(item));item.setdefault('item_id',item_id(item))
    item.setdefault('difficulty',infer_difficulty(item));item['source_keys']=source_keys
    item['source_basis']=" + ".join(SOURCE_REGISTRY[k]['publisher']+": "+SOURCE_REGISTRY[k]['use'] for k in source_keys if k in SOURCE_REGISTRY)
    item.setdefault('bank_version',BANK_VERSION);item.setdefault('created_on',str(date.today()));item.setdefault('review_status',review_status);item.setdefault('reviewed_on',None);item.setdefault('reviewed_by',None)
    item.setdefault('clean_room_attestation','Independently authored training item; production provenance restricted to approved public-source registry.')
    item.setdefault('copyright_note','Original training item; not copied from or represented as a live FINRA exam question.')
    item.setdefault('option_rationales',option_rationales(item))
    return item

def quality_flags(q):
    flags=[];choices=q.get('c',[])
    if len(choices)!=4:flags.append('choice_count')
    if q.get('a') not in choices:flags.append('answer_missing')
    if len(set(choices))!=len(choices):flags.append('duplicate_choices')
    if not q.get('why'):flags.append('missing_rationale')
    if not q.get('objective_id'):flags.append('missing_objective')
    if not q.get('concept_id'):flags.append('missing_concept_id')
    if not q.get('item_id'):flags.append('missing_item_id')
    if not q.get('option_rationales') or len(q.get('option_rationales',{}))!=len(choices):flags.append('missing_option_rationales')
    if not q.get('source_keys'):flags.append('missing_public_provenance')
    if not q.get('clean_room_attestation'):flags.append('missing_clean_room_attestation')
    if q.get('review_status') in ('production-approved','independently-reviewed') and not q.get('reviewed_on'):flags.append('review_date_missing')
    if q.get('style')=='recall':flags.append('recall_item')
    if len(q.get('q','').split())<7:flags.append('very_short_stem')
    return flags
