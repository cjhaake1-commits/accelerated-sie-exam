import random
import streamlit as st
from curriculum import CHAPTERS, BLOCKS, SECTION_CHAPTERS, SECTION_WEIGHTS
from math_cards import MATH_CARDS
from finra_style_engine import build_pool
from study_lessons import LESSONS
from deep_dive import DEEP_DIVE

st.set_page_config(page_title="Accelerated SIE Exam", page_icon="🎯", layout="wide")
st.markdown("""<style>.block-container{max-width:1200px;padding-top:1.2rem}.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}.big{font-size:2.1rem;font-weight:800}.muted{opacity:.8}</style>""",unsafe_allow_html=True)
DEFAULTS={"study_block":1,"math_idx":0,"chapter_idx":1,"chapter_card_idx":0,"chapter_quiz":[],"chapter_answers":{},"chapter_submitted":False,"chapter_attempt":0,"active_quiz_chapter":None,"block_exam":[],"block_answers":{},"block_submitted":False,"block_attempt":0,"active_test_block":None,"full_exam":[],"full_answers":{},"full_submitted":False,"full_attempt":0,"history":[]}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

def fresh_sample(chapters,n,variants=16):
    pool=build_pool(chapters,variants); random.shuffle(pool); chosen=[]; seen=set()
    for q in pool:
        key=(q["term"],q["q"])
        if key not in seen: chosen.append(q); seen.add(key)
        if len(chosen)==n: break
    if len(chosen)<n: chosen.extend(random.sample(pool,n-len(chosen)))
    random.shuffle(chosen); return chosen

def build_chapter_quiz(ch):
    st.session_state.chapter_attempt+=1; st.session_state.chapter_quiz=fresh_sample([ch],20); st.session_state.chapter_answers={}; st.session_state.chapter_submitted=False; st.session_state.active_quiz_chapter=ch

def build_block(block):
    st.session_state.block_attempt+=1; st.session_state.block_exam=fresh_sample(BLOCKS[block],50); st.session_state.block_answers={}; st.session_state.block_submitted=False; st.session_state.active_test_block=block

def build_full():
    st.session_state.full_attempt+=1; exam=[]
    for section,n in SECTION_WEIGHTS.items(): exam.extend(fresh_sample(SECTION_CHAPTERS[section],n))
    random.shuffle(exam); st.session_state.full_exam=exam; st.session_state.full_answers={}; st.session_state.full_submitted=False

def render_questions(items,answers_key,submitted_key,prefix):
    answers=st.session_state[answers_key]; submitted=st.session_state[submitted_key]
    for i,q in enumerate(items):
        st.markdown(f"**{i+1}. {q['q']}**")
        val=st.radio("Choose one",q["c"],index=None,key=f"{prefix}_{i}_{q['term']}_{hash(q['q'])}",label_visibility="collapsed",disabled=submitted)
        if val is not None: answers[i]=val
        if submitted:
            if answers.get(i)==q["a"]: st.success("Correct — "+q["why"])
            else: st.error("Correct answer: "+q["a"]+" — "+q["why"])
        st.divider()

def score(items,answers): return sum(answers.get(i)==q["a"] for i,q in enumerate(items))

def show_cliffnotes(block):
    chs=BLOCKS[block]
    st.subheader(f"Block {block}: Chapters {chs[0]}–{chs[-1]}")
    st.caption("Learn the concept first, then the tested distinctions, then the terminology. This layer is intentionally more robust than flashcards.")
    for ch in chs:
        lesson=LESSONS[ch]; deep=DEEP_DIVE[ch]
        with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}",expanded=True):
            st.markdown("### 1. Build the mental model")
            st.write(deep["narrative"])
            st.markdown("### 2. The core idea")
            st.info(lesson["big"])
            st.markdown("### 3. Why it works this way")
            for x in lesson["why"]: st.markdown(f"- {x}")
            st.markdown("### 4. How FINRA is likely to make you use it")
            st.success(deep["mental"])
            st.markdown("### 5. Connect it to the rest of the exam")
            st.write(deep["connection"])
            st.markdown("### 6. Close-answer traps")
            for x in lesson["traps"]: st.markdown(f"- ⚠️ {x}")
            st.markdown("### 7. Question-solving rule")
            st.success(lesson["apply"])
            st.markdown("### 8. Terms — memorize these LAST")
            for term,definition in CHAPTERS[ch]["cards"]: st.markdown(f"**{term}** — {definition}")

st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">Understand → Reason → Distinguish → Apply → Memorize Terms Last → Test</div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("SIE Command Center"); page=st.radio("Study mode",["Dashboard","Chapter Flashcards + 20Q Quiz","5-Chapter Study Blocks","Math & Formula Flashcards","75-Question Full Test","Review"]); st.caption("Training target: consistently score 85%+ before exam day.")

if page=="Dashboard":
    st.subheader("Course flow"); st.write("The block lessons are now the teaching layer: mental model → rationale → application → cross-chapter connections → close-answer traps → terms last. Flashcards remain the memorization layer, and tests require choosing among related concepts rather than obvious unrelated distractors.")
    for b,chs in BLOCKS.items(): st.info(f"Block {b}: Chapters {chs[0]}–{chs[-1]} deep lessons → 50-question randomized cumulative test")
elif page=="Chapter Flashcards + 20Q Quiz":
    ch=st.selectbox("Choose chapter",list(CHAPTERS),index=st.session_state.chapter_idx-1,format_func=lambda c:f"Chapter {c}: {CHAPTERS[c]['title']}")
    if ch!=st.session_state.chapter_idx: st.session_state.chapter_idx=ch; st.session_state.chapter_card_idx=0; st.session_state.chapter_quiz=[]; st.session_state.chapter_answers={}; st.session_state.chapter_submitted=False; st.session_state.active_quiz_chapter=None
    cards=CHAPTERS[ch]["cards"]; idx=st.session_state.chapter_card_idx%len(cards); term,definition=cards[idx]
    st.subheader(f"Chapter {ch}: {CHAPTERS[ch]['title']}"); st.caption("This section is deliberately concise for memorization. Learn concepts in the 5-Chapter Study Blocks first."); st.markdown(f"## {term}")
    if st.toggle("Reveal answer",key=f"chapter_reveal_{ch}_{idx}"): st.success(definition)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True): st.session_state.chapter_card_idx=(idx-1)%len(cards); st.rerun()
    if b.button("🔀 Random",use_container_width=True): st.session_state.chapter_card_idx=random.randrange(len(cards)); st.rerun()
    if c.button("Next ➡",use_container_width=True): st.session_state.chapter_card_idx=(idx+1)%len(cards); st.rerun()
    st.progress((idx+1)/len(cards),text=f"Card {idx+1} of {len(cards)}"); st.divider(); st.markdown("### 20-Question Chapter Quiz")
    if not st.session_state.chapter_quiz or st.session_state.active_quiz_chapter!=ch:
        if st.button("Start Fresh Harder 20-Question Quiz",type="primary",use_container_width=True): build_chapter_quiz(ch); st.rerun()
    else:
        if st.button("Generate 20 New Questions",use_container_width=True): build_chapter_quiz(ch); st.rerun()
        st.progress(len(st.session_state.chapter_answers)/20,text=f"Answered {len(st.session_state.chapter_answers)} / 20"); render_questions(st.session_state.chapter_quiz,"chapter_answers","chapter_submitted",f"chapter{ch}_{st.session_state.chapter_attempt}")
        if not st.session_state.chapter_submitted:
            if st.button("Submit Chapter Quiz",type="primary",use_container_width=True): st.session_state.chapter_submitted=True; st.rerun()
        else:
            s=score(st.session_state.chapter_quiz,st.session_state.chapter_answers); st.header(f"Chapter {ch} Score: {s}/20 — {s/20*100:.1f}%")
elif page=="5-Chapter Study Blocks":
    block=st.selectbox("Choose study block",list(BLOCKS),index=st.session_state.study_block-1,format_func=lambda b:f"Block {b}: Chapters {BLOCKS[b][0]}–{BLOCKS[b][-1]}")
    if block!=st.session_state.study_block: st.session_state.study_block=block; st.session_state.block_exam=[]; st.session_state.block_answers={}; st.session_state.block_submitted=False; st.session_state.active_test_block=None
    show_cliffnotes(block); st.divider(); st.markdown(f"## Chapters {BLOCKS[block][0]}–{BLOCKS[block][-1]} Cumulative Test")
    if not st.session_state.block_exam or st.session_state.active_test_block!=block:
        if st.button("I Understand the Block — Generate 50-Question Test",type="primary",use_container_width=True): build_block(block); st.rerun()
    else:
        if st.button("Generate a Different 50-Question Retake",use_container_width=True): build_block(block); st.rerun()
        st.progress(len(st.session_state.block_answers)/50,text=f"Answered {len(st.session_state.block_answers)} / 50"); render_questions(st.session_state.block_exam,"block_answers","block_submitted",f"b{block}_{st.session_state.block_attempt}")
        if not st.session_state.block_submitted:
            if st.button("Submit & Grade This Test",type="primary",use_container_width=True): st.session_state.block_submitted=True; st.rerun()
        else:
            s=score(st.session_state.block_exam,st.session_state.block_answers); st.header(f"Block {block} Score: {s}/50 — {s/50*100:.1f}%")
elif page=="Math & Formula Flashcards":
    st.subheader("🧮 SIE Math & Formula Flashcards"); idx=st.session_state.math_idx%len(MATH_CARDS); term,answer=MATH_CARDS[idx]; st.markdown(f"## {term}")
    if st.toggle("Reveal formula / rule",key=f"math_reveal_{idx}"): st.success(answer)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True): st.session_state.math_idx=(idx-1)%len(MATH_CARDS); st.rerun()
    if b.button("🔀 Random",use_container_width=True): st.session_state.math_idx=random.randrange(len(MATH_CARDS)); st.rerun()
    if c.button("Next ➡",use_container_width=True): st.session_state.math_idx=(idx+1)%len(MATH_CARDS); st.rerun()
    st.progress((idx+1)/len(MATH_CARDS),text=f"Math card {idx+1} of {len(MATH_CARDS)}")
elif page=="75-Question Full Test":
    st.subheader("75-Question Full SIE Practice Test — Hard Mode"); st.caption("Blueprint weighted: 12 Capital Markets, 33 Products & Risks, 23 Trading/Accounts/Prohibited Activities, 7 Regulatory Framework.")
    if not st.session_state.full_exam:
        if st.button("Generate Fresh Hard-Mode Full Test",type="primary",use_container_width=True): build_full(); st.rerun()
    else:
        if st.button("Generate a Different 75-Question Retake",use_container_width=True): build_full(); st.rerun()
        st.progress(len(st.session_state.full_answers)/75,text=f"Answered {len(st.session_state.full_answers)} / 75"); render_questions(st.session_state.full_exam,"full_answers","full_submitted",f"full{st.session_state.full_attempt}")
        if not st.session_state.full_submitted:
            if st.button("Submit Full Test",type="primary",use_container_width=True): st.session_state.full_submitted=True; s=score(st.session_state.full_exam,st.session_state.full_answers); st.session_state.history.append(s/75*100); st.rerun()
        else:
            s=score(st.session_state.full_exam,st.session_state.full_answers); st.header(f"Score: {s}/75 — {s/75*100:.1f}%")
elif page=="Review":
    st.subheader("Performance & remediation")
    if st.session_state.history: st.line_chart(st.session_state.history)
    else: st.info("Submit a full practice test to begin tracking performance.")
st.divider(); st.caption("Original study lessons grounded in the uploaded SIE manual. FINRA's public SIE outline/practice materials inform the exam-skill design; no live or proprietary FINRA exam questions are reproduced.")