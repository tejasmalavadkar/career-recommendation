import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Smart Career Advisor", page_icon="🚀", layout="centered")

# =========================
# DARK / LIGHT MODE
# =========================
theme = st.toggle("🌙 Dark Mode")

if theme:
    bg_color = "#0e1117"
    card_color = "#1c1f26"
else:
    bg_color = "#f5f7fa"
    card_color = "white"

st.markdown(f"""
<style>
.block-container {{
    max-width: 650px;
    margin: auto;
    padding-top: 40px;
}}
body {{
    background-color: {bg_color};
}}
.card {{
    background-color: {card_color};
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Smart Career Advisor")

# =========================
# LOAD MODEL
# =========================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =========================
# QUESTIONS
# =========================
questions = [
    "I enjoy building applications.",
    "I like analyzing data.",
    "Cybersecurity interests me.",
    "I enjoy UI/UX design.",
    "I love programming challenges.",
    "Math & statistics excite me.",
    "I enjoy system/network concepts.",
    "Creativity attracts me."
]

options = [
    "Strongly Agree",
    "Agree",
    "Neutral",
    "Disagree"
]

weights = {
    "Strongly Agree": 3,
    "Agree": 2,
    "Neutral": 1,
    "Disagree": 0
}

# =========================
# SESSION STATE
# =========================
if "question_number" not in st.session_state:
    st.session_state.question_number = 0
    st.session_state.answers = [None] * len(questions)

q_no = st.session_state.question_number

# =========================
# PROGRESS BAR 🔥
# =========================
progress = q_no / len(questions)
st.progress(progress)

# =========================
# QUESTION SECTION
# =========================
if q_no < len(questions):

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"Question {q_no + 1} of {len(questions)}")

    selected = st.radio(
        questions[q_no],
        options,
        index=1 if st.session_state.answers[q_no] is None else options.index(st.session_state.answers[q_no])
    )

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # BACK
    with col1:
        if q_no > 0:
            if st.button("⬅ Back"):
                st.session_state.question_number -= 1
                st.rerun()

    # NEXT / SUBMIT
    with col2:
        if q_no < len(questions) - 1:
            if st.button("Next ➡"):
                st.session_state.answers[q_no] = selected
                st.session_state.question_number += 1
                st.rerun()
        else:
            if st.button("✅ Submit"):
                st.session_state.answers[q_no] = selected
                st.session_state.question_number += 1
                st.rerun()

# =========================
# RESULT SECTION
# =========================
else:

    numeric_answers = [weights[a] for a in st.session_state.answers]

    # ✅ 4 FEATURES (MODEL FIX)
    strongly = numeric_answers.count(3)
    agree = numeric_answers.count(2)
    neutral = numeric_answers.count(1)
    disagree = numeric_answers.count(0)

    X_input = np.array([[strongly, agree, neutral, disagree]])

    prediction = model.predict(X_input)
    probabilities = model.predict_proba(X_input)[0]
    career = label_encoder.inverse_transform(prediction)[0]

    st.success(f"🎯 Recommended Career: {career}")

    # =========================
    # 📊 PERCENTAGE MATCH
    # =========================
    st.subheader("📊 Career Match Percentage")

    for i, prob in enumerate(probabilities):
        career_name = label_encoder.inverse_transform([i])[0]
        st.write(f"{career_name}: {round(prob * 100, 2)}%")

    # =========================
    # 🧠 RADAR CHART
    # =========================
    st.subheader("🧠 Your Interest Profile")

    labels = ["Strongly Agree", "Agree", "Neutral", "Disagree"]
    values = [strongly, agree, neutral, disagree]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    st.pyplot(fig)

    if st.button("🔄 Restart"):
        st.session_state.question_number = 0
        st.session_state.answers = [None] * len(questions)
        st.rerun()
