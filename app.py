import random
import streamlit as st
from curriculum import CHAPTERS, BLOCKS, SECTION_CHAPTERS, SECTION_WEIGHTS
from math_cards import MATH_CARDS

st.set_page_config(page_title="Accelerated SIE Exam", page_icon="🎯", layout="wide")
st.markdown("""<style>.block-container{max-width:1200px;padding-top:1.2rem}.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}.big{font-size:2.1rem;font-weight:800}.muted{opacity:.8}</style>""",unsafe_allow_html=True)

for k,v in {"study_block":1,"math_idx":0,"block_exam":[],"block_answers":{},"block_submitted":False,"block_attempt":0,"active_test_block":None,"full_exam":[],"full_answers":{},"full_submitted":False,"full_attempt":0,"history":[]}.items():
    if k not in st.session_state: st.session_state[k]=v

def close_distractors(ch, term, definition):
    pool=[]
    for n in range(max(1,ch-2), min(20,ch+2)+1):
        for t,d in CHAPTERS[n]["cards"]:
            if t!=term and d!=definition: pool.append(d)
    pool=list(dict.fromkeys(pool))
    if len(pool)<3: pool=[d for x in CHAPTERS.values() for t,d in x["cards"] if t!=term and d!=definition]
    return random.sample(pool,3)

def make_question(ch, card, variant=0):
    term,definition=card; choices=[definition]+close_distractors(ch,term,definition); random.shuffle(choices)
    stems=[f"Which statement most accurately describes {term}?",f"A registered representative is reviewing {term}. Which statement is most accurate?",f"Which of the following best applies to {term}?",f"A customer asks about {term}. Which response is most accurate?",f"Which statement concerning {term} is TRUE?",f"Which characteristic is most closely associated with {term}?"]
    return {"q":stems[(variant+ch)%len(stems)],"c":choices,"a":definition,"why":definition,"chapter":ch,"term":term,"section":CHAPTERS[ch]["section"]}

def build_pool(chapters,variants=10):
    return [make_question(ch,card,v+i) for ch in chapters for i,card in enumerate(CHAPTERS[ch]["cards"]) for v in range(variants)]

def build_block(block):
    st.session_state.block_attempt+=1; st.session_state.block_exam=random.sample(build_pool(BLOCKS[block]),50); random.shuffle(st.session_state.block_exam); st.session_state.block_answers={}; st.session_state.block_submitted=False; st.session_state.active_test_block=block

def build_full():
    st.session_state.full_attempt+=1; exam=[]
    for section,n in SECTION_WEIGHTS.items(): exam.extend(random.sample(build_pool(SECTION_CHAPTERS[section]),n))
    random.shuffle(exam); st.session_state.full_exam=exam; st.session_state.full_answers={}; st.session_state.full_submitted=False

def render_questions(items,answers_key,submitted_key,prefix):
    answers=st.session_state[answers_key]; submitted=st.session_state[submitted_key]
    for i,q in enumerate(items):
        st.markdown(f"**{i+1}. {q['q']}**")
        val=st.radio("Choose one",q["c"],index=None,key=f"{prefix}_{i}_{q['term']}_{q['q']}",label_visibility="collapsed",disabled=submitted)
        if val is not None: answers[i]=val
        if submitted:
            if answers.get(i)==q["a"]: st.success("Correct — "+q["why"])
            else: st.error("Correct answer: "+q["a"]+" — "+q["why"])
        st.divider()

def score(items,answers): return sum(answers.get(i)==q["a"] for i,q in enumerate(items))

def show_cliffnotes(block):
    chs=BLOCKS[block]; st.subheader(f"Block {block}: Chapters {chs[0]}–{chs[-1]}"); st.caption("Finish the five-chapter CliffNotes below, then take the 50-question cumulative test for this block.")
    for ch in chs:
        with st.expander(f"Chapter {ch}: {CHAPTERS[ch]['title']}",expanded=True):
            for term,definition in CHAPTERS[ch]["cards"]: st.markdown(f"**{term}** — {definition}")

st.markdown('<div class="hero"><div class="big">🎯 Accelerated SIE Exam</div><div class="muted">Four 5-Chapter CliffNotes Blocks → Math Flashcards → Four Fresh 50-Question Tests → 75-Question Full Simulation</div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("SIE Command Center")
    page=st.radio("Study mode",["Dashboard","5-Chapter Study Blocks","Math & Formula Flashcards","75-Question Full Test","Review"])
    st.caption("Training target: consistently score 85%+ before exam day.")

if page=="Dashboard":
    st.subheader("Course flow"); st.write("Four study blocks only: five chapters of CliffNotes followed by a 50-question cumulative test. The separate Math & Formula Flashcards section isolates calculations, equations, yield relationships and numerical thresholds.")
    for b,chs in BLOCKS.items(): st.info(f"Block {b}: Chapters {chs[0]}–{chs[-1]} CliffNotes → 50-question randomized cumulative test")
    st.success("After Block 4, finish with the 75-question full SIE practice test.")

elif page=="5-Chapter Study Blocks":
    block=st.selectbox("Choose study block",list(BLOCKS),index=st.session_state.study_block-1,format_func=lambda b:f"Block {b}: Chapters {BLOCKS[b][0]}–{BLOCKS[b][-1]}")
    if block!=st.session_state.study_block: st.session_state.study_block=block; st.session_state.block_exam=[]; st.session_state.block_answers={}; st.session_state.block_submitted=False; st.session_state.active_test_block=None
    show_cliffnotes(block); st.divider(); st.markdown(f"## Chapters {BLOCKS[block][0]}–{BLOCKS[block][-1]} Cumulative Test")
    if not st.session_state.block_exam or st.session_state.active_test_block!=block:
        if st.button("I Finished the CliffNotes — Generate Fresh 50-Question Test",type="primary",use_container_width=True): build_block(block); st.rerun()
    else:
        if st.button("Generate a Different 50-Question Retake",use_container_width=True): build_block(block); st.rerun()
        st.progress(len(st.session_state.block_answers)/50,text=f"Answered {len(st.session_state.block_answers)} / 50"); render_questions(st.session_state.block_exam,"block_answers","block_submitted",f"b{block}_{st.session_state.block_attempt}")
        if not st.session_state.block_submitted:
            if st.button("Submit & Grade This Test",type="primary",use_container_width=True): st.session_state.block_submitted=True; st.rerun()
        else:
            s=score(st.session_state.block_exam,st.session_state.block_answers); st.header(f"Block {block} Score: {s}/50 — {s/50*100:.1f}%")

elif page=="Math & Formula Flashcards":
    st.subheader("🧮 SIE Math & Formula Flashcards")
    st.write("Dedicated rapid-recall deck for equations, yield relationships, option math, bond conversions, fund pricing, splits and numerical thresholds. YTM/YTC cards emphasize the relationships you need to recognize and include approximation formulas as study aids.")
    idx=st.session_state.math_idx%len(MATH_CARDS); term,answer=MATH_CARDS[idx]
    st.markdown(f"## {term}")
    if st.toggle("Reveal formula / rule",key=f"math_reveal_{idx}"): st.success(answer)
    a,b,c=st.columns(3)
    if a.button("⬅ Previous",use_container_width=True): st.session_state.math_idx=(idx-1)%len(MATH_CARDS); st.rerun()
    if b.button("🔀 Random",use_container_width=True): st.session_state.math_idx=random.randrange(len(MATH_CARDS)); st.rerun()
    if c.button("Next ➡",use_container_width=True): st.session_state.math_idx=(idx+1)%len(MATH_CARDS); st.rerun()
    st.progress((idx+1)/len(MATH_CARDS),text=f"Math card {idx+1} of {len(MATH_CARDS)}")
    with st.expander("Show complete formula sheet"):
        for t,a in MATH_CARDS: st.markdown(f"**{t}** — {a}")

elif page=="75-Question Full Test":
    st.subheader("75-Question Full SIE Practice Test"); st.caption("Weighted to the SIE blueprint: 12 Capital Markets, 33 Products & Risks, 23 Trading/Accounts/Prohibited Activities, 7 Regulatory Framework.")
    if not st.session_state.full_exam:
        if st.button("Generate Fresh Full Practice Test",type="primary",use_container_width=True): build_full(); st.rerun()
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

st.divider(); st.caption("Original training questions and paraphrased study content aligned to the uploaded STC SIE manual. Questions are not copied from or represented as live FINRA exam questions.")