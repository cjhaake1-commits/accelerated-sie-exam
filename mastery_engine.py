"""Prototype commercial-learning engine for the SIE app.
Tracks concept-level mastery, confidence calibration, spaced-review due items,
blueprint-weighted readiness and a daily study prescription.
State is designed to live in Streamlit session state for now; production should persist to a user DB.
"""
from datetime import datetime, timedelta, timezone
from curriculum import CHAPTERS, SECTION_CHAPTERS

SECTION_WEIGHT_DECIMAL={
    "Capital Markets":0.16,
    "Products & Risks":0.44,
    "Trading, Accounts & Prohibited Activities":0.31,
    "Regulatory Framework":0.09,
}

def objective_id(q):
    return f"ch{q.get('chapter')}::{q.get('term','unknown')}"

def section_for_chapter(ch):
    for section,chapters in SECTION_CHAPTERS.items():
        if ch in chapters:return section
    return "Unknown"

def ensure_mastery(state):
    if "mastery" not in state: state.mastery={}
    if "attempt_log" not in state: state.attempt_log=[]
    if "review_due" not in state: state.review_due={}

def _quality(correct,confidence):
    if not correct:return 0.0
    if confidence=="Know it":return 1.0
    if confidence=="Unsure":return 0.72
    if confidence=="Guessed":return 0.40
    return 0.60

def _next_interval_days(old_score,correct,confidence):
    if not correct:return 0
    if confidence=="Guessed":return 1
    if confidence=="Unsure":return 2 if old_score<0.65 else 4
    if old_score<0.45:return 2
    if old_score<0.70:return 5
    if old_score<0.85:return 9
    return 16

def record_attempt(state,items,answers,confidence,mode="practice"):
    ensure_mastery(state)
    now=datetime.now(timezone.utc)
    for i,q in enumerate(items):
        oid=objective_id(q);correct=answers.get(i)==q.get("a");conf=confidence.get(i,"Not marked")
        old=state.mastery.get(oid,{"score":0.0,"attempts":0,"correct":0,"chapter":q.get("chapter"),"term":q.get("term"),"section":section_for_chapter(q.get("chapter"))})
        quality=_quality(correct,conf)
        # Recency-weighted estimate: new attempts matter, but one lucky answer cannot erase weakness.
        alpha=0.38 if old["attempts"] else 1.0
        new_score=(1-alpha)*old["score"]+alpha*quality
        old.update({"score":round(new_score,4),"attempts":old["attempts"]+1,"correct":old["correct"]+int(correct),"last_confidence":conf,"last_correct":correct,"last_seen":now.isoformat()})
        state.mastery[oid]=old
        interval=_next_interval_days(new_score,correct,conf)
        state.review_due[oid]=(now+timedelta(days=interval)).isoformat()
        state.attempt_log.append({"objective":oid,"chapter":q.get("chapter"),"term":q.get("term"),"section":old["section"],"correct":correct,"confidence":conf,"mode":mode,"at":now.isoformat(),"score":new_score})
    state.attempt_log=state.attempt_log[-1500:]

def due_objectives(state):
    ensure_mastery(state);now=datetime.now(timezone.utc);due=[]
    for oid,when in state.review_due.items():
        try:
            if datetime.fromisoformat(when)<=now:due.append(oid)
        except Exception:due.append(oid)
    return due

def chapter_mastery(state,ch):
    ensure_mastery(state);vals=[v["score"] for v in state.mastery.values() if v.get("chapter")==ch]
    return sum(vals)/len(vals) if vals else 0.0

def section_mastery(state,section):
    ensure_mastery(state);vals=[v["score"] for v in state.mastery.values() if v.get("section")==section]
    return sum(vals)/len(vals) if vals else 0.0

def coverage(state):
    ensure_mastery(state)
    total=sum(len(CHAPTERS[ch]["cards"]) for ch in CHAPTERS)
    seen=len(state.mastery)
    return min(1.0,seen/max(1,total))

def confidence_calibration(state):
    ensure_mastery(state);recent=state.attempt_log[-250:]
    if not recent:return 0.0
    vals=[]
    for x in recent:
        if x["confidence"]=="Know it": vals.append(1.0 if x["correct"] else 0.0)
        elif x["confidence"]=="Unsure": vals.append(0.75 if x["correct"] else 0.25)
        elif x["confidence"]=="Guessed": vals.append(0.45 if x["correct"] else 0.25)
    return sum(vals)/len(vals) if vals else 0.5

def weighted_objective_mastery(state):
    return sum(section_mastery(state,s)*w for s,w in SECTION_WEIGHT_DECIMAL.items())

def readiness_score(state,exam_history):
    recent=exam_history[-3:] if exam_history else []
    recent_exam=(sum(recent)/len(recent)/100.0) if recent else 0.0
    mastery=weighted_objective_mastery(state)
    calibration=confidence_calibration(state)
    cov=coverage(state)
    score=.45*recent_exam+.30*mastery+.15*calibration+.10*cov
    return round(score*100,1),{"recent_exam":recent_exam*100,"mastery":mastery*100,"calibration":calibration*100,"coverage":cov*100}

def daily_plan(state,minutes=30):
    ensure_mastery(state);due=set(due_objectives(state))
    weak=sorted(state.mastery.items(),key=lambda kv:(0 if kv[0] in due else 1,kv[1]["score"]))
    high_weight_order=["Products & Risks","Trading, Accounts & Prohibited Activities","Capital Markets","Regulatory Framework"]
    picks=[]
    for section in high_weight_order:
        for oid,data in weak:
            if data.get("section")==section and oid not in [x[0] for x in picks]:picks.append((oid,data))
            if len(picks)>=8:break
        if len(picks)>=8:break
    if not picks:
        return ["Start with FINRA-Weighted Learning: Products & Risks.","Complete one chapter flashcard deck and its chapter quiz.","Finish with 5 mixed application questions."]
    q_target=8 if minutes<=15 else 15 if minutes<=30 else 25
    terms=", ".join([f"Ch {d['chapter']} {d['term']}" for _,d in picks[:5]])
    return [f"Review these weak/due concepts first: {terms}.",f"Complete about {q_target} interleaved application questions across weak and high-weight topics.","Re-study any miss or guessed-correct item before ending the session."]
