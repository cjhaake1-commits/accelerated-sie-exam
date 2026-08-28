"""Exam-session helpers for realistic SIE simulation.
The official SIE appointment provides 1 hour 45 minutes for the exam. This module keeps
practice timing separate from content scoring so timing never changes whether an answer is correct.
"""
from datetime import datetime, timezone

EXAM_MINUTES=105
SCORED_QUESTIONS=75
SECONDS_PER_SCORED_QUESTION=(EXAM_MINUTES*60)/SCORED_QUESTIONS


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def elapsed_seconds(started_at):
    if not started_at:return 0
    try:
        start=datetime.fromisoformat(started_at)
        return max(0,int((datetime.now(timezone.utc)-start).total_seconds()))
    except Exception:return 0


def remaining_seconds(started_at,limit_minutes=EXAM_MINUTES):
    return max(0,limit_minutes*60-elapsed_seconds(started_at))


def clock_text(seconds):
    minutes,secs=divmod(max(0,int(seconds)),60)
    return f"{minutes:02d}:{secs:02d}"


def pacing_status(answered,total,started_at):
    elapsed=elapsed_seconds(started_at)
    expected=elapsed/SECONDS_PER_SCORED_QUESTION if elapsed else 0
    delta=answered-expected
    if elapsed<120:return "SETTLING IN"
    if delta>=3:return "AHEAD OF PACE"
    if delta<=-3:return "BEHIND PACE"
    return "ON PACE"


def exam_summary(items,answers,started_at):
    elapsed=elapsed_seconds(started_at)
    answered=sum(1 for i in range(len(items)) if answers.get(i) is not None)
    return {
        "answered":answered,
        "unanswered":len(items)-answered,
        "elapsed_seconds":elapsed,
        "avg_seconds_per_answer":round(elapsed/max(1,answered),1),
        "pace":pacing_status(answered,len(items),started_at),
    }
