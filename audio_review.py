"""Browser-based SIE audio review.
Uses the browser's built-in speechSynthesis voices so no binary audio asset or paid TTS service is required.
The script is assembled from independently authored app lessons and math review content.
"""
import json
import re
import streamlit as st
import streamlit.components.v1 as components
from deep_dive import DEEP_DIVE
from study_lessons import LESSONS
from math_cards import MATH_CARDS
from weighted_learning import WEIGHTED_SECTIONS
from curriculum import CHAPTERS


def build_audio_script():
    parts=[]
    parts.append("Accelerated SIE audio review. This is a day-off style review designed to reinforce understanding, not replace active practice. Listen for relationships, contrasts, causes and effects, and the handful of calculations that repeatedly matter.")
    parts.append("The SIE blueprint is weighted. Products and risks carry the most weight. Trading, customer accounts and prohibited activities come next. Capital markets follow, and the regulatory framework is the smallest section. Your study time should roughly follow that order, while still giving extra time to your personal weak areas.")

    for sec in WEIGHTED_SECTIONS:
        parts.append(f"Section focus: {sec['name']}. This represents about {sec['weight']} percent of the scored exam, or roughly {sec['questions']} questions.")
        for item in sec['master']:
            parts.append(item)
        parts.append(sec['question_logic'])

    for ch in range(1,21):
        title=CHAPTERS[ch]['title']
        parts.append(f"Chapter {ch}. {title}.")
        parts.append(DEEP_DIVE[ch]['narrative'])
        parts.append(DEEP_DIVE[ch]['mental'])
        for why in LESSONS[ch]['why']:
            parts.append(why)
        for trap in LESSONS[ch]['traps']:
            parts.append("Exam trap: "+trap)
        parts.append("Question-solving rule: "+LESSONS[ch]['apply'])

    parts.append("Now the high-yield math and numerical relationships.")
    for term,rule in MATH_CARDS:
        parts.append(f"{term}. {rule}")

    parts.append("Final review reminders. On bonds, think cash flows first, then price, yield, maturity, call features and credit. On options, identify call or put, long or short, right or obligation, bullish or bearish, then do the math. On orders, translate the customer's priority into execution certainty, price protection, or a trigger. On regulation and prohibited conduct, identify the activity before choosing the rule. On risk questions, name the source of the loss before choosing the label. Do not reward yourself for a lucky guess. If you cannot explain why the other answers are wrong, the concept is not fully mastered yet.")
    return "\n\n".join(parts)


def _estimated_minutes(text, wpm=155):
    words=len(re.findall(r"\b\w+\b",text))
    return max(1,round(words/wpm))


def render_audio_review():
    script=build_audio_script()
    minutes=_estimated_minutes(script)
    st.subheader("🎧 SIE Audio Review")
    st.caption(f"Browser-playable review • approximately {minutes} minutes at normal speed • no download or paid TTS required")
    st.info("Choose a voice available on your phone/computer, set the speed, then press Play. The browser generates the narration locally.")

    payload=json.dumps(script)
    html=f"""
    <div style='font-family:system-ui,-apple-system,Segoe UI,sans-serif;border:1px solid #dbe3ee;border-radius:16px;padding:18px;background:#fff'>
      <div style='font-weight:700;font-size:18px;margin-bottom:12px'>Accelerated SIE — Audio Review</div>
      <div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px'>
        <button id='play' style='padding:10px 16px;border-radius:10px;border:0;background:#2563eb;color:white;font-weight:700'>▶ Play</button>
        <button id='pause' style='padding:10px 16px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc'>⏸ Pause</button>
        <button id='resume' style='padding:10px 16px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc'>↻ Resume</button>
        <button id='stop' style='padding:10px 16px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc'>■ Stop</button>
      </div>
      <div style='display:grid;grid-template-columns:1fr 140px;gap:10px;margin-bottom:12px'>
        <select id='voice' style='padding:10px;border:1px solid #cbd5e1;border-radius:10px'></select>
        <select id='rate' style='padding:10px;border:1px solid #cbd5e1;border-radius:10px'>
          <option value='0.85'>0.85×</option><option value='0.95'>0.95×</option><option value='1.0' selected>1.0×</option><option value='1.1'>1.1×</option><option value='1.2'>1.2×</option><option value='1.35'>1.35×</option>
        </select>
      </div>
      <div style='height:10px;background:#e2e8f0;border-radius:999px;overflow:hidden'><div id='bar' style='height:100%;width:0%;background:#2563eb'></div></div>
      <div id='status' style='font-size:13px;color:#475569;margin-top:8px'>Ready</div>
    </div>
    <script>
      const fullText={payload};
      let chunks=fullText.split(/\n\n+/).map(x=>x.trim()).filter(Boolean);
      let idx=0, stopped=false;
      const synth=window.speechSynthesis;
      const voiceSel=document.getElementById('voice');
      const rateSel=document.getElementById('rate');
      const bar=document.getElementById('bar');
      const status=document.getElementById('status');
      function loadVoices(){{
        const voices=synth.getVoices();
        voiceSel.innerHTML='';
        voices.filter(v=>/^en/i.test(v.lang)).forEach((v,i)=>{{
          const o=document.createElement('option'); o.value=v.name; o.textContent=`${{v.name}} (${{v.lang}})`; voiceSel.appendChild(o);
        }});
        const preferred=[...voiceSel.options].find(o=>/Google US English|Samantha|Microsoft Aria|Natural|Neural/i.test(o.text));
        if(preferred) voiceSel.value=preferred.value;
      }}
      loadVoices(); synth.onvoiceschanged=loadVoices;
      function speakNext(){{
        if(stopped || idx>=chunks.length){{ if(idx>=chunks.length){{status.textContent='Finished';bar.style.width='100%';}} return; }}
        const u=new SpeechSynthesisUtterance(chunks[idx]);
        const v=synth.getVoices().find(x=>x.name===voiceSel.value); if(v) u.voice=v;
        u.rate=parseFloat(rateSel.value||'1.0'); u.pitch=1.0;
        u.onstart=()=>{{ status.textContent=`Playing section ${{idx+1}} of ${{chunks.length}}`; bar.style.width=`${{(idx/chunks.length)*100}}%`; }};
        u.onend=()=>{{ idx++; speakNext(); }};
        u.onerror=(e)=>{{ status.textContent='Playback interrupted. Press Play or Resume.'; }};
        synth.speak(u);
      }}
      document.getElementById('play').onclick=()=>{{ synth.cancel(); idx=0; stopped=false; speakNext(); }};
      document.getElementById('pause').onclick=()=>{{ synth.pause(); status.textContent='Paused'; }};
      document.getElementById('resume').onclick=()=>{{ stopped=false; if(synth.paused) synth.resume(); else if(!synth.speaking) speakNext(); status.textContent='Playing'; }};
      document.getElementById('stop').onclick=()=>{{ stopped=true; synth.cancel(); status.textContent='Stopped'; }};
      window.addEventListener('beforeunload',()=>synth.cancel());
    </script>
    """
    components.html(html,height=300,scrolling=False)
    with st.expander("Show audio review transcript"):
        st.text_area("Transcript",script,height=360,label_visibility="collapsed")
