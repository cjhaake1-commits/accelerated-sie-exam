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

st.set_page_config(page_title="Accelerated SIE Exam",page_icon="🎯",layout="wide")
st.markdown("""<style>.block-container{max-width:1200px;padding-top:1.2rem}.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}.big{font-size:2.1rem;font-weight:800}.muted{opacity:.82}.weight{font-size:1.7rem;font-weight:800}</style>""",unsafe_allow_html=True)
DEFAULTS={"study_block":1,"math_idx":0,"chapter_idx":1,"chapter_card_idx":0,"chapter_quiz":[],"chapter_answers":{},"chapter_conf":{},"chapter_submitted":False,"chapter_attempt":0,"active_quiz_chapter":None,"block_exam":[],"block_answers":{},"block_conf":{},"block_submitted":False,"block_attempt":0,"active_test_block":None,"full_exam":[],"full_answers":{},"full_conf":{},"full_submitted":False,"full_attempt":0,"history":[],"question_history":[],"miss_log":[]}
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

def log_results(items,answers,confidence):
    for i,q in enumerate(items):
        correct=answers.get(i)==q["a"];conf=confidence.get(i,"Not marked")
        if (not correct) or conf=="Guessed":
            st.session_state.miss_log.append({"chapter":q.get("chapter"),"term":q.get("term"),"question":q.get("q"),"answer":q.get("a"),"why":q.get("why"),"correct":correct,"confidence":conf})
    st.session_state.miss_log=st.session_state.miss_log[-300:]

def render_questions(items,answers_key,conf_key,submitted_key,prefix):
    answers=st.session_state[answers_key];confidence=st.session_state[conf_key];submitted=st.session_state[submitted_key]
    for i,q in enumerate(items):
        st.markdown(f"**{i+1}. {q['q']}**")
        val=st.radio("Choose one",q["c"],index=None,key=f"{prefix}_{i}_{q['term']}_{hash(q['q'])}",label_visibility="collapsed",disabled=submitted)
        if val is not None:answers[i]=val
        if not submitted:
            confidence[i]=st.radio("Confidence",["Know it","Unsure","Guessed"],index=None,horizontal=True,key=f"conf_{prefix}_{i}",label_visibility="collapsed") or confidence.get(i,"Not marked")
        if submitted:
            if answers.get(i)==q["a"]:st.success("Correct — "+q["why"])
            else:st.error("Correct answer: "+q["a"]+" — "+q["why"])
            if confidence.get(i)=="Guessed":st.warning("You marked this as a guess. Treat a lucky correct answer as a review item.")
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
    for sec in WEIGHTED_SECTIONS:
        with st.expander(f"{sec['priority']} — {sec['name']} — {sec['weight']}% / about {sec['questions']} scored questions",expanded=sec['weight']>=31):
            c1,c2=st.columns([1,3])
            with c1:st.markdown(f"<div class='weight'>{sec['weight']}%</div>",unsafe_allow_html=True);st.write("Chapters: "+", ".join(map(str,sec["chapters"])));st.write(f"Approx. scored questions: {sec['questions']}")
            with c2:
                st.markdown("#### What to master")
                for x in sec["master"]:st.markdown(f"- {x}")
                st.markdown("#### Math / quantitative relationships")
                for x in sec["math"]:st.markdown(f"- 🧮 {x}")
                st.markdown("#### How questions should feel");st.info(sec["question_logic"])
            st.markdown("#### Deep chapter lessons")
            for ch in sec["chapters"]:
                with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}"):show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))
    st.divider();st.markdown("### Best-practice study method")
    for step in STUDY_METHOD:st.markdown(f"- {step}")

def show_block(block):
    chs=BLOCKS[block];target=BLOCK_TARGETS.get(block,35);st.subheader(f"Block {block}: Chapters {chs[0]}–{chs[-1]}");st.caption(f"Up to {target} distinct concepts. The app now returns fewer items rather than clone a concept just to hit a number.")
    for ch in chs:
        with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}",expanded=True):show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))

st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">Learn deeply • apply under uncertainty • track guesses as weaknesses • simulate the FINRA blueprint</div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("SIE Command Center");page=st.radio("Study mode",["Dashboard","FINRA-Weighted Learning","Chapter Flashcards + 20Q Quiz","5-Chapter Study Blocks","Math & Formula Flashcards","75-Question Full Test","Review & Weak Areas"]);st.caption("Readiness target: repeated 85%+ practice scores with few guesses.")

if page=="Dashboard":
    st.subheader("What matters most");cols=st.columns(4)
    for col,sec in zip(cols,WEIGHTED_SECTIONS):
        with col:st.metric(sec["priority"],f"{sec['weight']}%",f"~{sec['questions']} questions");st.caption(sec["name"])
    st.info("75% of scored SIE content is Products & Risks plus Trading/Accounts/Prohibited Activities. Correct guesses are not mastery, so the app now tracks them for remediation.")
    if st.session_state.history:
        recent=st.session_state.history[-3:];st.metric("Recent full-exam average",f"{sum(recent)/len(recent):.1f}%")
    st.markdown("### Recommended order");st.write("Weighted learning → chapter checks → block application tests → math deck → 75Q simulation → remediate every miss and guess.")

elif page=="FINRA-Weighted Learning":show_weighted_learning()
elif page=="Chapter Flashcards + 20Q Quiz":
    ch=st.selectbox("Choose chapter",list(CHAPTERS),index=st.session_state.chapter_idx-1,format_func=lambda c:f"Chapter {c}: {CHAPTERS[c]['title']}")
    if ch!=st.session_state.chapter_idx:st.session_state.chapter_idx=ch;st.session_state.chapter_card_idx=0;st.session_state.chapter_quiz=[];st.session_state.active_quiz_chapter=None
    cards=CHAPTERS[ch]["cards"];idx=st.session_state.chapter_card_idx%len(cards);term,definition=cards[idx];st.subheader(f"Chapter {ch}: {CHAPTERS[ch]['title']}");st.caption("Flashcards are the memorization layer. Deep learning comes first.");st.markdown(f"## {term}")
    if st.toggle("Reveal answer",key=f"chapter_reveal_{ch}_{idx}"):st.success(definition)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True):st.session_state.chapter_card_idx=(idx-1)%len(cards);st.rerun()
    if b.button("🔀 Random",use_container_width=True):st.session_state.chapter_card_idx=random.randrange(len(cards));st.rerun()
    if c.button("Next ➡",use_container_width=True):st.session_state.chapter_card_idx=(idx+1)%len(cards);st.rerun()
    st.divider()
    if not st.session_state.chapter_quiz or st.session_state.active_quiz_chapter!=ch:
        if st.button("Start Fresh Chapter Quiz",type="primary",use_container_width=True):build_chapter_quiz(ch);st.rerun()
    else:
        st.caption(f"{len(st.session_state.chapter_quiz)} distinct concepts available in this sitting.");render_questions(st.session_state.chapter_quiz,"chapter_answers","chapter_conf","chapter_submitted",f"chapter{ch}_{st.session_state.chapter_attempt}")
        if not st.session_state.chapter_submitted and st.button("Submit Chapter Quiz",type="primary",use_container_width=True):log_results(st.session_state.chapter_quiz,st.session_state.chapter_answers,st.session_state.chapter_conf);st.session_state.chapter_submitted=True;st.rerun()
        if st.session_state.chapter_submitted:
            s=score(st.session_state.chapter_quiz,st.session_state.chapter_answers);st.header(f"Score: {s}/{len(st.session_state.chapter_quiz)} — {100*s/len(st.session_state.chapter_quiz):.1f}%")
            if st.button("Generate a New Chapter Quiz"):build_chapter_quiz(ch);st.rerun()

elif page=="5-Chapter Study Blocks":
    block=st.selectbox("Choose study block",list(BLOCKS),index=st.session_state.study_block-1,format_func=lambda b:f"Block {b}: Chapters {BLOCKS[b][0]}–{BLOCKS[b][-1]}")
    if block!=st.session_state.study_block:st.session_state.study_block=block;st.session_state.block_exam=[];st.session_state.active_test_block=None
    show_block(block);st.divider();target=BLOCK_TARGETS.get(block,35);st.markdown(f"## Application Test — target up to {target} unique concepts")
    if not st.session_state.block_exam or st.session_state.active_test_block!=block:
        if st.button("Generate Fresh Application Test",type="primary",use_container_width=True):build_block(block);st.rerun()
    else:
        st.caption(f"This sitting contains {len(st.session_state.block_exam)} non-duplicate underlying concepts.");render_questions(st.session_state.block_exam,"block_answers","block_conf","block_submitted",f"b{block}_{st.session_state.block_attempt}")
        if not st.session_state.block_submitted and st.button("Submit & Grade",type="primary",use_container_width=True):log_results(st.session_state.block_exam,st.session_state.block_answers,st.session_state.block_conf);st.session_state.block_submitted=True;st.rerun()
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
    st.subheader("75-Question Full SIE Practice Test — Blueprint Weighted");st.caption("12 Capital Markets • 33 Products & Risks • 23 Trading/Accounts/Prohibited Activities • 7 Regulatory Framework. The app will not clone concepts if a source-grounded section bank is temporarily smaller than its target.")
    if not st.session_state.full_exam:
        if st.button("Generate Fresh Full Test",type="primary",use_container_width=True):build_full();st.rerun()
    else:
        st.progress(len(st.session_state.full_answers)/max(1,len(st.session_state.full_exam)),text=f"Answered {len(st.session_state.full_answers)} of {len(st.session_state.full_exam)}");render_questions(st.session_state.full_exam,"full_answers","full_conf","full_submitted",f"full{st.session_state.full_attempt}")
        if not st.session_state.full_submitted and st.button("Submit Full Test",type="primary",use_container_width=True):
            log_results(st.session_state.full_exam,st.session_state.full_answers,st.session_state.full_conf);st.session_state.full_submitted=True;s=score(st.session_state.full_exam,st.session_state.full_answers);st.session_state.history.append(100*s/len(st.session_state.full_exam));st.rerun()
        if st.session_state.full_submitted:
            s=score(st.session_state.full_exam,st.session_state.full_answers);st.header(f"Score: {s}/{len(st.session_state.full_exam)} — {100*s/len(st.session_state.full_exam):.1f}%");st.markdown("### Blueprint breakdown")
            for sec,right,total,pct in section_stats(st.session_state.full_exam,st.session_state.full_answers):st.write(f"**{sec}:** {right}/{total} — {pct:.1f}%")
            if st.button("Generate a Different Full Retake"):build_full();st.rerun()

elif page=="Review & Weak Areas":
    st.subheader("Adaptive remediation")
    if st.session_state.history:st.line_chart(st.session_state.history)
    misses=st.session_state.miss_log
    if not misses:st.info("Missed and guessed questions will appear here after you submit a quiz or test.")
    else:
        st.write(f"Review queue: **{len(misses)}** misses/guesses (recent history).")
        counts={}
        for x in misses:counts[x["chapter"]]=counts.get(x["chapter"],0)+1
        st.markdown("### Weak chapters")
        for ch,n in sorted(counts.items(),key=lambda x:x[1],reverse=True):st.write(f"Chapter {ch} — {CHAPTERS[ch]['title']}: **{n}** review flags")
        st.markdown("### Recent remediation cards")
        for x in reversed(misses[-20:]):
            with st.expander(f"Ch {x['chapter']} • {x['term']} • {x['confidence']}"):
                st.write(x["question"]);st.success("Correct answer: "+x["answer"]);st.write(x["why"])

st.divider();st.caption("Study lessons are grounded in the uploaded STC SIE manual. Public FINRA materials inform blueprint weighting and exam-skill design; no proprietary/live FINRA questions are reproduced.")