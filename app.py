import random
import streamlit as st
from curriculum import CHAPTERS, BLOCKS, SECTION_CHAPTERS, SECTION_WEIGHTS
from math_cards import MATH_CARDS
from study_lessons import LESSONS
from deep_dive import DEEP_DIVE
from block1_mastery import BLOCK1_MASTERY
from adaptive_exam_engine import balanced_sample, identities
from weighted_learning import WEIGHTED_SECTIONS, STUDY_METHOD
from exam_blueprint import BLOCK_TARGETS
from mastery_engine import record_attempt, readiness_score, daily_plan, chapter_mastery, section_mastery, due_objectives
from audio_review import render_audio_review

st.set_page_config(page_title="Accelerated SIE Exam",page_icon="🎯",layout="wide")
st.markdown("""<style>.block-container{max-width:1200px;padding-top:1.2rem}.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}.big{font-size:2.1rem;font-weight:800}.muted{opacity:.82}.weight{font-size:1.7rem;font-weight:800}</style>""",unsafe_allow_html=True)
DEFAULTS={"study_block":1,"math_idx":0,"chapter_idx":1,"chapter_card_idx":0,"chapter_quiz":[],"chapter_answers":{},"chapter_conf":{},"chapter_submitted":False,"chapter_attempt":0,"active_quiz_chapter":None,"block_exam":[],"block_answers":{},"block_conf":{},"block_submitted":False,"block_attempt":0,"active_test_block":None,"full_exam":[],"full_answers":{},"full_conf":{},"full_submitted":False,"full_attempt":0,"history":[],"question_history":[],"miss_log":[],"mastery":{},"attempt_log":[],"review_due":{}}
for k,v in DEFAULTS.items():
    if k not in st.session_state:st.session_state[k]=v

def fresh_sample(chapters,n):
    q=balanced_sample(chapters,n,st.session_state.question_history);st.session_state.question_history.extend(identities(q));st.session_state.question_history=st.session_state.question_history[-500:];return q

def build_chapter_quiz(ch):
    st.session_state.chapter_attempt+=1;st.session_state.chapter_quiz=fresh_sample([ch],20);st.session_state.chapter_answers={};st.session_state.chapter_conf={};st.session_state.chapter_submitted=False;st.session_state.active_quiz_chapter=ch

def build_block(block):
    n=BLOCK_TARGETS.get(block,35);st.session_state.block_attempt+=1;st.session_state.block_exam=fresh_sample(BLOCKS[block],n);st.session_state.block_answers={};st.session_state.block_conf={};st.session_state.block_submitted=False;st.session_state.active_test_block=block

def build_full():
    st.session_state.full_attempt+=1;exam=[]
    for section,n in SECTION_WEIGHTS.items():exam.extend(fresh_sample(SECTION_CHAPTERS[section],n))
    random.shuffle(exam);st.session_state.full_exam=exam;st.session_state.full_answers={};st.session_state.full_conf={};st.session_state.full_submitted=False

def log_results(items,answers,confidence,mode="practice"):
    record_attempt(st.session_state,items,answers,confidence,mode)
    for i,q in enumerate(items):
        correct=answers.get(i)==q["a"];conf=confidence.get(i,"Not marked")
        if (not correct) or conf in ("Guessed","Unsure"):
            st.session_state.miss_log.append({"chapter":q.get("chapter"),"term":q.get("term"),"question":q.get("q"),"answer":q.get("a"),"why":q.get("why"),"correct":correct,"confidence":conf})
    st.session_state.miss_log=st.session_state.miss_log[-300:]

def render_questions(items,answers_key,conf_key,submitted_key,prefix,exam_mode=False):
    answers=st.session_state[answers_key];confidence=st.session_state[conf_key];submitted=st.session_state[submitted_key]
    for i,q in enumerate(items):
        st.markdown(f"**{i+1}. {q['q']}**")
        val=st.radio("Choose one",q["c"],index=None,key=f"{prefix}_{i}_{q['term']}_{hash(q['q'])}",label_visibility="collapsed",disabled=submitted)
        if val is not None:answers[i]=val
        if not submitted and not exam_mode:
            confidence[i]=st.radio("Confidence",["Know it","Unsure","Guessed"],index=None,horizontal=True,key=f"conf_{prefix}_{i}",label_visibility="collapsed") or confidence.get(i,"Not marked")
        if submitted:
            if answers.get(i)==q["a"]:st.success("Correct — "+q["why"])
            else:st.error("Correct answer: "+q["a"]+" — "+q["why"])
            if confidence.get(i)=="Guessed":st.warning("Lucky correct answers are scheduled for review rather than counted as full mastery.")
        st.divider()

def score(items,answers):return sum(answers.get(i)==q["a"] for i,q in enumerate(items))

def section_stats(items,answers):
    rows=[]
    for sec,chs in SECTION_CHAPTERS.items():
        subset=[(i,q) for i,q in enumerate(items) if q.get("chapter") in chs]
        if subset:
            right=sum(answers.get(i)==q["a"] for i,q in subset);rows.append((sec,right,len(subset),100*right/len(subset)))
    return rows

def show_chapter_deep(ch,extra=None):
    lesson=LESSONS[ch];deep=DEEP_DIVE[ch];st.markdown("### Build the mental model");st.write(deep["narrative"])
    if extra:
        st.markdown("### Major topics to understand")
        for title,text in extra["major"]:st.markdown(f"**{title}** — {text}")
        st.markdown("### Reason through the question");st.info(extra["reason"]);st.markdown("### Math / relationships")
        for x in extra["math"]:st.markdown(f"- 🧮 {x}")
        st.markdown("### Close distinctions");st.write(" • ".join(extra["distinguish"]))
    st.markdown("### Why it works this way")
    for x in lesson["why"]:st.markdown(f"- {x}")
    st.markdown("### How the exam can make you use it");st.success(deep["mental"]);st.markdown("### Connect it to other SIE topics");st.write(deep["connection"]);st.markdown("### Close-answer traps")
    for x in lesson["traps"]:st.markdown(f"- ⚠️ {x}")
    st.markdown("### Question-solving rule");st.success(lesson["apply"]);st.markdown("### Terms — memorize these LAST")
    for term,definition in CHAPTERS[ch]["cards"]:st.markdown(f"**{term}** — {definition}")

def show_weighted_learning():
    st.subheader("FINRA-Weighted Learning Plan");st.caption("Higher-weight functions get more explanation, math and practice.")
    canonical={"Understanding Products and Their Risks":"Products & Risks","Knowledge of Capital Markets":"Capital Markets","Understanding Trading, Customer Accounts and Prohibited Activities":"Trading, Accounts & Prohibited Activities","Overview of Regulatory Framework":"Regulatory Framework"}
    for sec in WEIGHTED_SECTIONS:
        mastery=section_mastery(st.session_state,canonical.get(sec["name"],sec["name"]))
        with st.expander(f"{sec['priority']} — {sec['name']} — {sec['weight']}% • mastery {mastery*100:.0f}%",expanded=sec['weight']>=31):
            c1,c2=st.columns([1,3])
            with c1:st.markdown(f"<div class='weight'>{sec['weight']}%</div>",unsafe_allow_html=True);st.write("Chapters: "+", ".join(map(str,sec["chapters"])));st.write(f"Approx. scored questions: {sec['questions']}")
            with c2:
                st.markdown("#### What to master")
                for x in sec["master"]:st.markdown(f"- {x}")
                st.markdown("#### Math / quantitative relationships")
                for x in sec["math"]:st.markdown(f"- 🧮 {x}")
                st.markdown("#### How questions should feel");st.info(sec["question_logic"])
            for ch in sec["chapters"]:
                with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']} • mastery {chapter_mastery(st.session_state,ch)*100:.0f}%"):show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))
    st.divider();st.markdown("### Best-practice study method")
    for step in STUDY_METHOD:st.markdown(f"- {step}")

def show_block(block):
    chs=BLOCKS[block];target=BLOCK_TARGETS.get(block,35);st.subheader(f"Block {block}: Chapters {chs[0]}–{chs[-1]}");st.caption(f"Up to {target} distinct concepts; quality beats filler.")
    for ch in chs:
        with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']} • mastery {chapter_mastery(st.session_state,ch)*100:.0f}%",expanded=True):show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))

st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">Blueprint-weighted • adaptive mastery • spaced review • confidence calibration • realistic simulation</div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("SIE Command Center");page=st.radio("Study mode",["Dashboard","🎧 40-Minute Audio Review","Today's Study Plan","FINRA-Weighted Learning","Chapter Flashcards + Quiz","5-Chapter Study Blocks","Math & Formula Flashcards","75-Question Full Test","Review & Weak Areas"]);st.caption("Readiness target: repeated 85%+ unseen practice performance with low uncertainty.")

if page=="Dashboard":
    readiness,parts=readiness_score(st.session_state,st.session_state.history);st.subheader("Readiness Command Center")
    a,b,c,d=st.columns(4);a.metric("Readiness",f"{readiness:.0f}/100");b.metric("Recent exams",f"{parts['recent_exam']:.0f}%");c.metric("Objective mastery",f"{parts['mastery']:.0f}%");d.metric("Due reviews",len(due_objectives(st.session_state)))
    st.progress(min(readiness/100,1.0),text="Composite readiness — diagnostic guidance, not a guaranteed pass probability")
    st.markdown("### Blueprint mastery")
    for sec in ["Products & Risks","Trading, Accounts & Prohibited Activities","Capital Markets","Regulatory Framework"]:st.write(f"**{sec}:** {section_mastery(st.session_state,sec)*100:.0f}%")
    st.info("Readiness combines recent full simulations, objective mastery, confidence calibration and coverage. Guessed-correct answers receive reduced mastery credit.")

elif page=="🎧 40-Minute Audio Review":render_audio_review()
elif page=="Today's Study Plan":
    st.subheader("Today's Adaptive Study Plan");minutes=st.segmented_control("Available time",[15,30,60],default=30,format_func=lambda x:f"{x} min") or 30
    for i,x in enumerate(daily_plan(st.session_state,minutes),1):st.markdown(f"**{i}.** {x}")
    st.caption("As you complete quizzes, this prescription shifts toward due, weak and high-weight objectives.")

elif page=="FINRA-Weighted Learning":show_weighted_learning()
elif page=="Chapter Flashcards + Quiz":
    ch=st.selectbox("Choose chapter",list(CHAPTERS),index=st.session_state.chapter_idx-1,format_func=lambda c:f"Chapter {c}: {CHAPTERS[c]['title']} • mastery {chapter_mastery(st.session_state,c)*100:.0f}%")
    if ch!=st.session_state.chapter_idx:st.session_state.chapter_idx=ch;st.session_state.chapter_card_idx=0;st.session_state.chapter_quiz=[];st.session_state.active_quiz_chapter=None
    cards=CHAPTERS[ch]["cards"];idx=st.session_state.chapter_card_idx%len(cards);term,definition=cards[idx];st.subheader(f"Chapter {ch}: {CHAPTERS[ch]['title']}");st.markdown(f"## {term}")
    if st.toggle("Reveal answer",key=f"chapter_reveal_{ch}_{idx}"):st.success(definition)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True):st.session_state.chapter_card_idx=(idx-1)%len(cards);st.rerun()
    if b.button("🔀 Random",use_container_width=True):st.session_state.chapter_card_idx=random.randrange(len(cards));st.rerun()
    if c.button("Next ➡",use_container_width=True):st.session_state.chapter_card_idx=(idx+1)%len(cards);st.rerun()
    st.divider()
    if not st.session_state.chapter_quiz or st.session_state.active_quiz_chapter!=ch:
        if st.button("Start Fresh Chapter Quiz",type="primary",use_container_width=True):build_chapter_quiz(ch);st.rerun()
    else:
        st.caption(f"{len(st.session_state.chapter_quiz)} distinct concepts in this sitting.");render_questions(st.session_state.chapter_quiz,"chapter_answers","chapter_conf","chapter_submitted",f"chapter{ch}_{st.session_state.chapter_attempt}")
        if not st.session_state.chapter_submitted and st.button("Submit Chapter Quiz",type="primary",use_container_width=True):log_results(st.session_state.chapter_quiz,st.session_state.chapter_answers,st.session_state.chapter_conf,"chapter");st.session_state.chapter_submitted=True;st.rerun()
        if st.session_state.chapter_submitted:
            s=score(st.session_state.chapter_quiz,st.session_state.chapter_answers);st.header(f"Score: {s}/{len(st.session_state.chapter_quiz)} — {100*s/len(st.session_state.chapter_quiz):.1f}%")
            if st.button("Generate a New Chapter Quiz"):build_chapter_quiz(ch);st.rerun()

elif page=="5-Chapter Study Blocks":
    block=st.selectbox("Choose study block",list(BLOCKS),index=st.session_state.study_block-1,format_func=lambda b:f"Block {b}: Chapters {BLOCKS[b][0]}–{BLOCKS[b][-1]}")
    if block!=st.session_state.study_block:st.session_state.study_block=block;st.session_state.block_exam=[];st.session_state.active_test_block=None
    show_block(block);st.divider();target=BLOCK_TARGETS.get(block,35);st.markdown(f"## Application Test — up to {target} unique concepts")
    if not st.session_state.block_exam or st.session_state.active_test_block!=block:
        if st.button("Generate Fresh Application Test",type="primary",use_container_width=True):build_block(block);st.rerun()
    else:
        render_questions(st.session_state.block_exam,"block_answers","block_conf","block_submitted",f"b{block}_{st.session_state.block_attempt}")
        if not st.session_state.block_submitted and st.button("Submit & Grade",type="primary",use_container_width=True):log_results(st.session_state.block_exam,st.session_state.block_answers,st.session_state.block_conf,"block");st.session_state.block_submitted=True;st.rerun()
        if st.session_state.block_submitted:
            s=score(st.session_state.block_exam,st.session_state.block_answers);st.header(f"Score: {s}/{len(st.session_state.block_exam)} — {100*s/len(st.session_state.block_exam):.1f}%")
            if st.button("Generate a Different Retake"):build_block(block);st.rerun()

elif page=="Math & Formula Flashcards":
    st.subheader("🧮 SIE Math & Formula Flashcards");idx=st.session_state.math_idx%len(MATH_CARDS);term,answer=MATH_CARDS[idx];st.markdown(f"## {term}")
    if st.toggle("Reveal formula / rule",key=f"math_reveal_{idx}"):st.success(answer)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True):st.session_state.math_idx=(idx-1)%len(MATH_CARDS);st.rerun()
    if b.button("🔀 Random",use_container_width=True):st.session_state.math_idx=random.randrange(len(MATH_CARDS));st.rerun()
    if c.button("Next ➡",use_container_width=True):st.session_state.math_idx=(idx+1)%len(MATH_CARDS);st.rerun()

elif page=="75-Question Full Test":
    st.subheader("Full SIE Simulation — Blueprint Weighted");st.caption("Official scored blueprint target: 12 / 33 / 23 / 7. Simulation mode withholds explanations until submission.")
    if not st.session_state.full_exam:
        if st.button("Generate Fresh Full Test",type="primary",use_container_width=True):build_full();st.rerun()
    else:
        st.progress(len(st.session_state.full_answers)/max(1,len(st.session_state.full_exam)),text=f"Answered {len(st.session_state.full_answers)} of {len(st.session_state.full_exam)}");render_questions(st.session_state.full_exam,"full_answers","full_conf","full_submitted",f"full{st.session_state.full_attempt}",exam_mode=True)
        if not st.session_state.full_submitted and st.button("Submit Full Test",type="primary",use_container_width=True):
            log_results(st.session_state.full_exam,st.session_state.full_answers,st.session_state.full_conf,"full_exam");st.session_state.full_submitted=True;s=score(st.session_state.full_exam,st.session_state.full_answers);st.session_state.history.append(100*s/len(st.session_state.full_exam));st.rerun()
        if st.session_state.full_submitted:
            s=score(st.session_state.full_exam,st.session_state.full_answers);st.header(f"Score: {s}/{len(st.session_state.full_exam)} — {100*s/len(st.session_state.full_exam):.1f}%");st.markdown("### Blueprint breakdown")
            for sec,right,total,pct in section_stats(st.session_state.full_exam,st.session_state.full_answers):st.write(f"**{sec}:** {right}/{total} — {pct:.1f}%")
            if st.button("Generate a Different Full Retake"):build_full();st.rerun()

elif page=="Review & Weak Areas":
    st.subheader("Adaptive Remediation");due=due_objectives(st.session_state);st.metric("Concepts due now",len(due));misses=st.session_state.miss_log
    if not misses:st.info("Missed, unsure and guessed questions populate this queue after practice.")
    else:
        counts={}
        for x in misses:counts[x["chapter"]]=counts.get(x["chapter"],0)+1
        st.markdown("### Weak chapters")
        for ch,n in sorted(counts.items(),key=lambda x:x[1],reverse=True):st.write(f"Chapter {ch} — {CHAPTERS[ch]['title']}: **{n} flags** • mastery {chapter_mastery(st.session_state,ch)*100:.0f}%")
        st.markdown("### Recent remediation cards")
        for x in reversed(misses[-20:]):
            with st.expander(f"Ch {x['chapter']} • {x['term']} • {x['confidence']}"):
                st.write(x["question"]);st.success("Correct answer: "+x["answer"]);st.write(x["why"])

st.divider();st.caption("Independent SIE study tool. Commercial content is being re-authored and reviewed against public regulatory sources under the project's clean-room policy. Not affiliated with or endorsed by FINRA. No proprietary/live exam questions are reproduced.")