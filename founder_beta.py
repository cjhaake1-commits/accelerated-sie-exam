"""Founder-beta instrumentation.
Designed for the first real test subject without turning a single outcome into a marketing statistic.
"""
from datetime import datetime, timezone

BETA_VERSION="founder-1"

def ensure_beta(state):
    if "founder_beta" not in state:
        state.founder_beta={
            "version":BETA_VERSION,"started_at":datetime.now(timezone.utc).isoformat(),
            "study_sessions":[],"simulations":[],"actual_exam":None,"notes":[]}
    return state.founder_beta

def log_study_session(state,minutes,mode,objectives=None):
    beta=ensure_beta(state)
    beta["study_sessions"].append({"at":datetime.now(timezone.utc).isoformat(),"minutes":int(minutes),"mode":mode,"objectives":list(objectives or [])})

def log_simulation(state,score,question_count,elapsed_seconds,unanswered=0):
    beta=ensure_beta(state)
    beta["simulations"].append({"at":datetime.now(timezone.utc).isoformat(),"score_pct":round(float(score),1),"question_count":int(question_count),"elapsed_seconds":int(elapsed_seconds),"unanswered":int(unanswered)})

def record_actual_exam(state,result,exam_date=None,notes=""):
    beta=ensure_beta(state)
    normalized=str(result).strip().lower()
    if normalized not in {"pass","fail"}:raise ValueError("result must be pass or fail")
    beta["actual_exam"]={"result":normalized,"exam_date":exam_date,"recorded_at":datetime.now(timezone.utc).isoformat(),"notes":notes}

def beta_summary(state):
    beta=ensure_beta(state);sessions=beta["study_sessions"];sims=beta["simulations"]
    minutes=sum(x["minutes"] for x in sessions)
    recent=[x["score_pct"] for x in sims[-3:]]
    return {
      "study_minutes":minutes,"study_hours":round(minutes/60,1),"sessions":len(sessions),"simulations":len(sims),
      "recent_sim_avg":round(sum(recent)/len(recent),1) if recent else None,
      "actual_exam":beta["actual_exam"],
      "marketing_status":"individual founder case study only; not a validated pass-rate claim"
    }
