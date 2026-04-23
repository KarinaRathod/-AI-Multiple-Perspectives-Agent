import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import datetime

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Multiple Perspectives Agent", layout="wide")
st.title("🧠🎭 Multiple Perspectives Decision Agent")
st.caption("Answer questions and see decisions from different perspectives")

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# MCQ QUESTIONS
# -----------------------------
st.subheader("📝 Answer These Questions")

goal = st.text_input("🎯 What decision are you trying to make?")

q1 = st.radio("1. What is your risk tolerance?", [
    "Low", "Medium", "High"
])

q2 = st.radio("2. Time commitment available?", [
    "Less than 1 hour/day", "1-3 hours/day", "Full-time"
])

q3 = st.radio("3. What matters most?", [
    "Stability", "Growth", "Passion"
])

q4 = st.radio("4. Your current situation?", [
    "Student", "Working professional", "Exploring options"
])

# -----------------------------
# GENERATE OUTPUT
# -----------------------------
if st.button("🚀 Analyze Perspectives"):

    if not goal.strip():
        st.warning("⚠️ Please enter your goal")
        st.stop()

    with st.spinner("🧠 Analyzing from multiple minds..."):

        prompt = f"""
        A user is making this decision:
        {goal}

        Their answers:
        - Risk: {q1}
        - Time: {q2}
        - Priority: {q3}
        - Situation: {q4}

        Provide perspectives from:

        1. CEO:
        - Strategic, long-term thinking

        2. Psychologist:
        - Emotional and behavioral insight

        3. Investor:
        - Risk vs reward analysis

        4. Beginner:
        - Simple, practical advice

        Finally:
        - Give a clear recommendation
        """

        response = model.generate_content(prompt)
        result = response.text

        # Save
        st.session_state.history.append({
            "time": str(datetime.datetime.now()),
            "goal": goal,
            "result": result
        })

        # -----------------------------
        # DISPLAY
        # -----------------------------
        st.subheader("🎭 Perspectives")
        st.write(result)

# -----------------------------
# HISTORY
# -----------------------------
if st.session_state.history:
    st.subheader("💾 Past Decisions")

    for item in reversed(st.session_state.history[-5:]):
        st.write(f"🕒 {item['time']}")
        st.write(f"🎯 {item['goal']}")
        st.info(item['result'])
        st.divider()