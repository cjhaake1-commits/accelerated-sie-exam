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
st.markdown("""
<style>
.block-container{max-width:1200px;padding-top:1.2rem}
.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}
.big{font-size:2.1rem;font-weight:800}.muted{opacity:.82}
.weight{font-size:1.7rem;font-weight:800}
</style>
""",unsafe_allow_html=True)

DEFAULTS={"study_block":1,"math_idx":0,"chapter_idx":1,"chapter_card_idx":0,"chapter_quiz":[],"chapter_answers":{},"chapter_submitted":False,"chapter_attempt":0,"active_quiz_chapter":None,"block_exam":[],"block_answers":{},"block_submitted":False,"block_attempt":0,"active_test_block":None,"full_exam":[],"full_answers":{},"full_submitted":False,"full_attempt":0,"history":[],"question_history":[]}
for k,v in DEFAULTS.items():
    if k not in st.session_state:st.session_state[k]=v

def fresh_sample(chapters,n):
    q=balanced_sample(chapters,n,st.session_state.question_history)
    st.session_state.question_history.extend(identities(q))
    st.session_state.question_history=st.session_state.question_history[-500:]
    return q

def build_chapter_quiz(ch):
    st.session_state.chapter_attempt+=1
    st.session_state.chapter_quiz=fresh_sample([ch],20)
    st.session_state.chapter_answers={};st.session_state.chapter_submitted=False;st.session_state.active_quiz_chapter=ch

def build_block(block):
    n=BLOCK_TARGETS.get(block,35)
    st.session_state.block_attempt+=1
    st.session_state.block_exam=fresh_sample(BLOCKS[block],n)
    st.session_state.block_answers={};st.session_state.block_submitted=False;st.session_state.active_test_block=block

def build_full():
    st.session_state.full_attempt+=1;exam=[]
    for section,n in SECTION_WEIGHTS.items():exam.extend(fresh_sample(SECTION_CHAPTERS[section],n))
    random.shuffle(exam);st.session_state.full_exam=exam;st.session_state.full_answers={};st.session_state.full_submitted=False

def render_questions(items,answers_key,submitted_key,prefix):
    answers=st.session_state[answers_key];submitted=st.session_state[submitted_key]
    for i,q in enumerate(items):
        st.markdown(f"**{i+1}. {q['q']}**")
        val=st.radio("Choose one",q["c"],index=None,key=f"{prefix}_{i}_{q['term']}_{hash(q['q'])}",label_visibility="collapsed",disabled=submitted)
        if val is not None:answers[i]=val
        if submitted:
            if answers.get(i)==q["a"]:st.success("Correct — "+q["why"])
            else:st.error("Correct answer: "+q["a"]+" — "+q["why"])
        st.divider()

def score(items,answers):return sum(answers.get(i)==q["a"] for i,q in enumerate(items))

def show_chapter_deep(ch,extra=None):
    lesson=LESSONS[ch];deep=DEEP_DIVE[ch]
    st.markdown("### Build the mental model");st.write(deep["narrative"])
    if extra:
        st.markdown("### Major topics to understand")
        for title,text in extra["major"]:st.markdown(f"**{title}** — {text}")
        st.markdown("### Reason through the question");st.info(extra["reason"])
        st.markdown("### Math / relationships")
        for x in extra["math"]:st.markdown(f"- 🧮 {x}")
        st.markdown("### Close distinctions")
        st.write(" • ".join(extra["distinguish"]))
    st.markdown("### Why it works this way")
    for x in lesson["why"]:st.markdown(f"- {x}")
    st.markdown("### How the exam can make you use it");st.success(deep["mental"])
    st.markdown("### Connect it to other SIE topics");st.write(deep["connection"])
    st.markdown("### Close-answer traps")
    for x in lesson["traps"]:st.markdown(f"- ⚠️ {x}")
    st.markdown("### Question-solving rule");st.success(lesson["apply"])
    st.markdown("### Terms — memorize these LAST")
    for term,definition in CHAPTERS[ch]["cards"]:st.markdown(f"**{term}** — {definition}")

def show_weighted_learning():
    st.subheader("FINRA-Weighted Learning Plan")
    st.caption("Study time and depth follow the scored SIE blueprint. Higher-weight functions get more explanation, examples, math and practice.")
    for sec in WEIGHTED_SECTIONS:
        with st.expander(f"{sec['priority']} — {sec['name']} — {sec['weight']}% / about {sec['questions']} scored questions",expanded=sec['weight']>=31):
            c1,c2=st.columns([1,3])
            with c1:
                st.markdown(f"<div class='weight'>{sec['weight']}%</div>",unsafe_allow_html=True)
                st.write("Chapters: "+", ".join(map(str,sec["chapters"])))
                st.write(f"Approx. scored questions: {sec['questions']}")
            with c2:
                st.markdown("#### What to master")
                for x in sec["master"]:st.markdown(f"- {x}")
                st.markdown("#### Math / quantitative relationships")
                for x in sec["math"]:st.markdown(f"- 🧮 {x}")
                st.markdown("#### How questions should feel")
                st.info(sec["question_logic"])
            st.markdown("#### Deep chapter lessons for this function")
            for ch in sec["chapters"]:
                with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}"):
                    show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))
    st.divider();st.markdown("### Best-practice study method")
    for step in STUDY_METHOD:st.markdown(f"- {step}")

def show_block(block):
    chs=BLOCKS[block];target=BLOCK_TARGETS.get(block,35)
    st.subheader(f"Block {block}: Chapters {chs[0]}–{chs[-1]}")
    st.caption(f"This block uses a {target}-question cap so quality and unique coverage beat repetition. Learn first; then test application.")
    for ch in chs:
        with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}",expanded=True):show_chapter_deep(ch,BLOCK1_MASTERY.get(ch))

st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">Blueprint-weighted learning • robust chapter teaching • fewer repetitive questions • 75-question final simulation</div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("SIE Command Center")
    page=st.radio("Study mode",["Dashboard","FINRA-Weighted Learning","Chapter Flashcards + 20Q Quiz","5-Chapter Study Blocks","Math & Formula Flashcards","75-Question Full Test","Review"])
    st.caption("Training target: consistently score 85%+ before exam day.")

if page=="Dashboard":
    st.subheader("What matters most")
    cols=st.columns(4)
    for col,sec in zip(cols,WEIGHTED_SECTIONS):
        with col:
            st.metric(sec["priority"],f"{sec['weight']}%",f"~{sec['questions']} questions")
            st.caption(sec["name"])
    st.info("75% of the scored exam comes from Products & Risks plus Trading/Accounts/Prohibited Activities. The app now gives those functions the greatest learning depth and practice emphasis.")
    st.markdown("### Recommended order")
    st.write("1) FINRA-Weighted Learning → 2) chapter flashcards/20Q checks → 3) 5-chapter block exam → 4) math deck → 5) weighted 75Q simulation.")

elif page=="FINRA-Weighted Learning":
    show_weighted_learning()

elif page=="Chapter Flashcards + 20Q Quiz":
    ch=st.selectbox("Choose chapter",list(CHAPTERS),index=st.session_state.chapter_idx-1,format_func=lambda c:f"Chapter {c}: {CHAPTERS[c]['title']}")
    if ch!=st.session_state.chapter_idx:st.session_state.chapter_idx=ch;st.session_state.chapter_card_idx=0;st.session_state.chapter_quiz=[];st.session_state.chapter_answers={};st.session_state.chapter_submitted=False;st.session_state.active_quiz_chapter=None
    cards=CHAPTERS[ch]["cards"];idx=st.session_state.chapter_card_idx%len(cards);term,definition=cards[idx]
    st.subheader(f"Chapter {ch}: {CHAPTERS[ch]['title']}");st.caption("Flashcards are the memorization layer. Use weighted/deep learning before relying on these.");st.markdown(f"## {term}")
    if st.toggle("Reveal answer",key=f"chapter_reveal_{ch}_{idx}"):st.success(definition)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True):st.session_state.chapter_card_idx=(idx-1)%len(cards);st.rerun()
    if b.button("🔀 Random",use_container_width=True):st.session_state.chapter_card_idx=random.randrange(len(cards));st.rerun()
    if c.button("Next ➡",use_container_width=True):st.session_state.chapter_card_idx=(idx+1)%len(cards);st.rerun()
    st.progress((idx+1)/len(cards),text=f"Card {idx+1} of {len(cards)}");st.divider();st.markdown("### 20-Question Chapter Quiz")
    if not st.session_state.chapter_quiz or st.session_state.active_quiz_chapter!=ch:
        if st.button("Start Fresh 20-Question Quiz",type="primary",use_container_width=True):build_chapter_quiz(ch);st.rerun()
    else:
        if st.button("Generate 20 New Questions",use_container_width=True):build_chapter_quiz(ch);st.rerun()
        render_questions(st.session_state.chapter_quiz,"chapter_answers","chapter_submitted",f"chapter{ch}_{st.session_state.chapter_attempt}")
        if not st.session_state.chapter_submitted:
            if st.button("Submit Chapter Quiz",type="primary",use_container_width=True):st.session_state.chapter_submitted=True;st.rerun()
        else:
            s=score(st.session_state.chapter_quiz,st.session_state.chapter_answers);st.header(f"Chapter {ch} Score: {s}/20 — {s/20*100:.1f}%")

elif page=="5-Chapter Study Blocks":
    block=st.selectbox("Choose study block",list(BLOCKS),index=st.session_state.study_block-1,format_func=lambda b:f"Block {b}: Chapters {BLOCKS[b][0]}–{BLOCKS[b][-1]}")
    if block!=st.session_state.study_block:st.session_state.study_block=block;st.session_state.block_exam=[];st.session_state.block_answers={};st.session_state.block_submitted=False;st.session_state.active_test_block=None
    show_block(block);st.divider();target=BLOCK_TARGETS.get(block,35);st.markdown(f"## Chapters {BLOCKS[block][0]}–{BLOCKS[block][-1]} Application Test — {target} Questions")
    if not st.session_state.block_exam or st.session_state.active_test_block!=block:
        if st.button(f"Generate Fresh {target}-Question Test",type="primary",use_container_width=True):build_block(block);st.rerun()
    else:
        if st.button(f"Generate a Different {target}-Question Retake",use_container_width=True):build_block(block);st.rerun()
        render_questions(st.session_state.block_exam,"block_answers","block_submitted",f"b{block}_{st.session_state.block_attempt}")
        if not st.session_state.block_submitted:
            if st.button("Submit & Grade This Test",type="primary",use_container_width=True):st.session_state.block_submitted=True;st.rerun()
        else:
            s=score(st.session_state.block_exam,st.session_state.block_answers);pct=s/len(st.session_state.block_exam)*100;st.header(f"Block {block} Score: {s}/{len(st.session_state.block_exam)} — {pct:.1f}%")

elif page=="Math & Formula Flashcards":
    st.subheader("🧮 SIE Math & Formula Flashcards");idx=st.session_state.math_idx%len(MATH_CARDS);term,answer=MATH_CARDS[idx];st.markdown(f"## {term}")
    if st.toggle("Reveal formula / rule",key=f"math_reveal_{idx}"):st.success(answer)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True):st.session_state.math_idx=(idx-1)%len(MATH_CARDS);st.rerun()
    if b.button("🔀 Random",use_container_width=True):st.session_state.math_idx=random.randrange(len(MATH_CARDS));st.rerun()
    if c.button("Next ➡",use_container_width=True):st.session_state.math_idx=(idx+1)%len(MATH_CARDS);st.rerun()

elif page=="75-Question Full Test":
    st.subheader("75-Question Full SIE Practice Test — Blueprint Weighted")
    st.caption("12 Capital Markets • 33 Products & Risks • 23 Trading/Accounts/Prohibited Activities • 7 Regulatory Framework")
    if not st.session_state.full_exam:
        if st.button("Generate Fresh Full Test",type="primary",use_container_width=True):build_full();st.rerun()
    else:
        if st.button("Generate a Different 75-Question Retake",use_container_width=True):build_full();st.rerun()
        render_questions(st.session_state.full_exam,"full_answers","full_submitted",f"full{st.session_state.full_attempt}")
        if not st.session_state.full_submitted:
            if st.button("Submit Full Test",type="primary",use_container_width=True):st.session_state.full_submitted=True;s=score(st.session_state.full_exam,st.session_state.full_answers);st.session_state.history.append(s/75*100);st.rerun()
        else:
            s=score(st.session_state.full_exam,st.session_state.full_answers);st.header(f"Score: {s}/75 — {s/75*100:.1f}%")

elif page=="Review":
    st.subheader("Performance & remediation")
    if st.session_state.history:st.line_chart(st.session_state.history)
    else:st.info("Submit a full practice test to begin tracking performance.")

st.divider();st.caption("Original study lessons grounded in the uploaded STC SIE manual. Public FINRA materials inform weighting and exam-skill design; no proprietary/live FINRA exam questions are reproduced.")