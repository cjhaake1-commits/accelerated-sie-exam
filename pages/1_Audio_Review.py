import streamlit as st
from audio_review import render_audio_review

st.set_page_config(page_title="SIE Audio Review",page_icon="🎧",layout="wide")
st.markdown("""<style>.block-container{max-width:1000px;padding-top:1.4rem}</style>""",unsafe_allow_html=True)
st.title("🎧 40-Minute SIE Review")
st.write("Use this when driving, walking, or between study sessions. For best retention, follow it later with active questions in the main study app.")
render_audio_review()
st.caption("Independent SIE study tool. Browser speech uses a voice installed on your device. Not affiliated with or endorsed by FINRA.")
