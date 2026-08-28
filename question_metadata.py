"""Commercial question-bank metadata and QA helpers.
Adds objective IDs, difficulty, provenance/version fields and answer-choice rationales.
No item is represented as a live FINRA question. FINRA public outline informs objective mapping only.
"""
from datetime import date
from curriculum import CHAPTERS

BANK_VERSION="2026.08.28"
SOURCE_BASIS="Uploaded STC SIE manual + FINRA public SIE content outline/practice-style calibration"

def objective_id(q):
    return f"SIE-CH{int(q.get('chapter',0)):02d}-{str(q.get('term','concept')).upper().replace(' ','-').replace('/','-')[:48]}"

def infer_difficulty(q):
    text=(q.get('q','')+' '+q.get('why','')).lower()
    if any(x in text for x in ['calculate','approximately','breakeven','current yield','conversion ratio','most appropriate','best explains','except','not true','not accurate']):
        return 3
    if q.get('style') in ('application','scenario'):
        return 2
    return 1

def _term_definition(ch,choice):
    for term,definition in CHAPTERS.get(ch,{}).get('cards',[]):
        if choice.strip().lower()==term.strip().lower():return definition
    return None

def option_rationales(q):
    """Return rationale per option.
    Exact term distractors get their real definition; phrase distractors receive a concise
    contrast explanation that is explicitly marked as an instructional rationale.
    """
    out={}
    answer=q.get('a')
    why=q.get('why','')
    ch=q.get('chapter')
    for choice in q.get('c',[]):
        if choice==answer:
            out[choice]=why or 'This choice best matches the facts and rule tested.'
            continue
        d=_term_definition(ch,choice)
        if d:
            out[choice]=f"Not best here. {choice} means: {d} The stem is testing {q.get('term','a different concept')}."
        else:
            out[choice]=f"Not best here. This choice does not match the controlling fact or distinction in the stem; compare it with the rule for {q.get('term','the tested concept')}."
    return out

def enrich(q,review_status="draft-reviewed"):
    item=dict(q)
    item.setdefault('objective_id',objective_id(item))
    item.setdefault('difficulty',infer_difficulty(item))
    item.setdefault('source_basis',SOURCE_BASIS)
    item.setdefault('bank_version',BANK_VERSION)
    item.setdefault('last_reviewed',str(date.today()))
    item.setdefault('review_status',review_status)
    item.setdefault('copyright_note','Original training item; not copied from or represented as a live FINRA exam question.')
    item.setdefault('option_rationales',option_rationales(item))
    return item

def quality_flags(q):
    flags=[]
    if len(q.get('c',[]))!=4:flags.append('choice_count')
    if q.get('a') not in q.get('c',[]):flags.append('answer_missing')
    if len(set(q.get('c',[])))!=len(q.get('c',[])):flags.append('duplicate_choices')
    if not q.get('why'):flags.append('missing_rationale')
    if not q.get('objective_id'):flags.append('missing_objective')
    if not q.get('option_rationales'):flags.append('missing_option_rationales')
    if q.get('style')=='recall':flags.append('recall_item')
    return flags
