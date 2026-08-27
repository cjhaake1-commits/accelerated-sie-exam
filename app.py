import random
import streamlit as st
from question_bank import QUESTION_FAMILIES, FLASHCARDS, CLIFF_NOTES

st.set_page_config(page_title="Accelerated SIE Exam", page_icon="🎯", layout="wide")

# FINRA's scored outline weighting: 12 / 33 / 23 / 7 = 75 scored questions.
DOMAIN_ORDER = [
    ("Capital Markets", 12),
    ("Products & Risks", 33),
    ("Trading, Accounts & Prohibited Activities", 23),
    ("Regulatory Framework", 7),
]

st.markdown("""
<style>
.block-container{max-width:1200px;padding-top:1.4rem}.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}.pill{display:inline-block;padding:.25rem .6rem;border-radius:999px;background:#eef2ff;margin:.15rem;font-size:.85rem}.big{font-size:2.2rem;font-weight:800}.muted{opacity:.78}.card{border:1px solid rgba(128,128,128,.25);border-radius:14px;padding:1rem;margin:.5rem 0}
</style>
""", unsafe_allow_html=True)

if "attempt" not in st.session_state: st.session_state.attempt = 0
if "exam" not in st.session_state: st.session_state.exam = []
if "answers" not in st.session_state: st.session_state.answers = {}
if "submitted" not in st.session_state: st.session_state.submitted = False
if "history" not in st.session_state: st.session_state.history = []
if "fc" not in st.session_state: st.session_state.fc = 0


def build_exam():
    """Build a 75-question exam matching FINRA scored-domain weights.
    Every new attempt alternates to the other stem in every question family,
    guaranteeing 100% of question stems differ from the immediately prior exam.
    Choices are also reshuffled independently.
    """
    st.session_state.attempt += 1
    stem_key = "q1" if st.session_state.attempt % 2 else "q2"
    exam = []
    for domain, count in DOMAIN_ORDER:
        pool = [x for x in QUESTION_FAMILIES if x["d"] == domain]
        chosen = random.sample(pool, count)
        for item in chosen:
            choices = item["c"].copy()
            random.shuffle(choices)
            exam.append({"q": item[stem_key], "c": choices, "a": item["a"], "d": item["d"], "e": item["e"]})
    random.shuffle(exam)
    st.session_state.exam = exam
    st.session_state.answers = {}
    st.session_state.submitted = False


def grade_exam():
    exam = st.session_state.exam
    correct = sum(st.session_state.answers.get(i) == q["a"] for i, q in enumerate(exam))
    pct = round(correct / len(exam) * 100, 1)
    by_domain = {}
    for domain, _ in DOMAIN_ORDER:
        idxs = [i for i,q in enumerate(exam) if q["d"] == domain]
        hits = sum(st.session_state.answers.get(i) == exam[i]["a"] for i in idxs)
        by_domain[domain] = round(hits / len(idxs) * 100, 1) if idxs else 0
    st.session_state.history.append({"attempt":st.session_state.attempt,"score":pct,**by_domain})
    st.session_state.submitted = True


st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">CliffNotes → Flashcards → Targeted Practice → Full Simulation → Remediation → Pass Readiness</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("SIE Command Center")
    page = st.radio("Study mode", ["Dashboard","CliffNotes","Flashcards","Practice Exam","Rapid Drill","Exam Review"])
    st.divider()
    st.caption("Full simulation: 75 scored-style questions")
    st.caption("Target: 70% to pass; train toward 85%+ for margin.")
    st.caption("Question stems rotate 100% between consecutive full attempts.")

if page == "Dashboard":
    st.subheader("Your fastest path")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Capital Markets","12 / 75")
    c2.metric("Products & Risks","33 / 75")
    c3.metric("Trading / Accounts","23 / 75")
    c4.metric("Regulatory","7 / 75")
    st.info("Priority rule: Products & Risks + Trading/Accounts/Prohibited Activities = 56 of the 75 scored questions. Spend most of your time there, while memorizing high-yield regulatory numbers, Acts, account rules and option/bond relationships.")
    st.markdown("### Recommended cycle")
    st.markdown("**1. CliffNotes (20–30 min)** → **2. Flashcards (15 min)** → **3. Rapid Drill (20 min)** → **4. Full Exam (105 min max)** → **5. Review every miss**")
    if st.session_state.history:
        last=st.session_state.history[-1]
        st.metric("Latest full-exam score", f"{last['score']}%", "READY" if last['score']>=85 else "Keep training")
        st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)

elif page == "CliffNotes":
    st.subheader("SIE CliffNotes — high-yield review")
    st.caption("Condensed around the uploaded STC manual's four SIE content areas and exam weighting.")
    for domain,_ in DOMAIN_ORDER:
        with st.expander(domain, expanded=True):
            for note in CLIFF_NOTES[domain]: st.markdown(f"- {note}")
    st.warning("Buzzword method: when you see a key phrase, immediately connect it to the rule: 1933→new issue; 1934→secondary/SEC; broker→agent; dealer→principal; rates↑→bond prices↓; call→buy; put→sell; GO→taxes; revenue→project revenue; CIP→identity; CTR→cash >$10k; SIPC→broker failure, not market loss.")

elif page == "Flashcards":
    st.subheader("Flashcards")
    idx=st.session_state.fc % len(FLASHCARDS)
    term,definition=FLASHCARDS[idx]
    st.markdown(f"### {term}")
    if st.toggle("Reveal answer", key=f"reveal_{idx}"):
        st.success(definition)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous", use_container_width=True): st.session_state.fc=(idx-1)%len(FLASHCARDS); st.rerun()
    if b.button("🔀 Random", use_container_width=True): st.session_state.fc=random.randrange(len(FLASHCARDS)); st.rerun()
    if c.button("Next ➡", use_container_width=True): st.session_state.fc=(idx+1)%len(FLASHCARDS); st.rerun()
    st.progress((idx+1)/len(FLASHCARDS), text=f"Card {idx+1} of {len(FLASHCARDS)}")

elif page == "Practice Exam":
    st.subheader("Full SIE Simulation")
    st.caption("75 questions using the official scored-domain proportions. Each consecutive attempt uses the alternate stem for every question family, so 100% of the question wording changes.")
    if not st.session_state.exam:
        if st.button("Start Full Exam", type="primary", use_container_width=True): build_exam(); st.rerun()
    else:
        top1,top2=st.columns([3,1])
        top1.progress(len(st.session_state.answers)/75, text=f"Answered {len(st.session_state.answers)} / 75")
        if top2.button("New 100% Fresh Exam", use_container_width=True): build_exam(); st.rerun()
        for i,q in enumerate(st.session_state.exam):
            st.markdown(f"**{i+1}. {q['q']}**")
            val=st.radio("Choose one", q["c"], index=None, key=f"exam_{st.session_state.attempt}_{i}", label_visibility="collapsed", disabled=st.session_state.submitted)
            if val is not None: st.session_state.answers[i]=val
            if st.session_state.submitted:
                if st.session_state.answers.get(i)==q["a"]: st.success(f"Correct — {q['e']}")
                else: st.error(f"Correct answer: {q['a']} — {q['e']}")
            st.divider()
        if not st.session_state.submitted:
            if st.button("Submit & Grade", type="primary", use_container_width=True): grade_exam(); st.rerun()
        else:
            correct=sum(st.session_state.answers.get(i)==q["a"] for i,q in enumerate(st.session_state.exam))
            pct=correct/75*100
            st.header(f"Score: {correct}/75 — {pct:.1f}%")
            if pct>=85: st.success("Strong readiness margin. Keep rotating fresh exams until this is repeatable.")
            elif pct>=70: st.warning("Passing-range performance, but build more margin. Review misses and retest.")
            else: st.error("Below passing range. Use Exam Review + CliffNotes, then take a fresh exam.")
            if st.button("Generate Next 100% Fresh Exam", type="primary", use_container_width=True): build_exam(); st.rerun()

elif page == "Rapid Drill":
    st.subheader("Rapid Drill")
    domain=st.selectbox("Focus area", [x[0] for x in DOMAIN_ORDER]+["Mixed"])
    n=st.slider("Questions",5,30,10)
    if st.button("Generate Drill", type="primary"):
        pool=QUESTION_FAMILIES if domain=="Mixed" else [x for x in QUESTION_FAMILIES if x["d"]==domain]
        picks=random.sample(pool,min(n,len(pool)))
        st.session_state.drill=[]
        for x in picks:
            stem=random.choice(["q1","q2"]); choices=x["c"].copy(); random.shuffle(choices)
            st.session_state.drill.append({"q":x[stem],"c":choices,"a":x["a"],"e":x["e"],"d":x["d"]})
    for i,q in enumerate(st.session_state.get("drill",[])):
        with st.expander(f"{i+1}. {q['q']}"):
            ans=st.radio("Answer",q["c"],index=None,key=f"dr_{i}_{q['q']}")
            if ans:
                if ans==q["a"]: st.success("Correct. "+q["e"])
                else: st.error(f"Correct: {q['a']}. {q['e']}")

elif page == "Exam Review":
    st.subheader("Remediation")
    if not st.session_state.submitted or not st.session_state.exam:
        st.info("Complete and submit a full Practice Exam first. Your misses will appear here.")
    else:
        misses=[(i,q) for i,q in enumerate(st.session_state.exam) if st.session_state.answers.get(i)!=q["a"]]
        st.metric("Questions to remediate",len(misses))
        domains={}
        for _,q in misses: domains[q["d"]]=domains.get(q["d"],0)+1
        if domains: st.bar_chart(domains)
        for i,q in misses:
            st.markdown(f"**Q{i+1}: {q['q']}**")
            st.write(f"Your answer: {st.session_state.answers.get(i,'Unanswered')}")
            st.success(f"Correct: {q['a']}")
            st.caption(q["e"])
            st.divider()

st.divider()
st.caption("Original study questions for training purposes. Not copied from or represented as live FINRA exam questions. Exam weighting follows the SIE content breakdown used by the uploaded study manual. Readiness scores are study heuristics, not a guarantee of passing.")
