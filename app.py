import streamlit as st
import pickle
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Smart Career Advisor", page_icon="🚀")

st.title("🚀 Smart Career Advisor")
st.write("Answer the questions one by one")

# =========================
# LOAD ML MODEL
# =========================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =========================
# QUESTION LIST (MIXED)
# =========================
questions = [
    "Do you enjoy building applications?",
    "Do you like analyzing data?",
    "Are you interested in cyber security?",
    "Do you enjoy designing user interfaces?",
    "Do you like solving programming problems?",
    "Do you enjoy statistics and math?",
    "Are you interested in ethical hacking?",
    "Do you like creativity and visual design?"
]

options = ["Strongly Yes", "Yes", "No", "Strongly No"]

# =========================
# SESSION STATE INIT
# =========================
if "question_number" not in st.session_state:
    st.session_state.question_number = 0
    st.session_state.answers = []

# =========================
# SHOW CURRENT QUESTION
# =========================
if st.session_state.question_number < len(questions):

    q_no = st.session_state.question_number
    st.subheader(f"Question {q_no + 1}")

    answer = st.radio(
        questions[q_no],
        options,
        key=q_no
    )

    if st.button("Submit & Next"):

        st.session_state.answers.append(options.index(answer))
        st.session_state.question_number += 1
        st.rerun()

# =========================
# SHOW RESULT AFTER LAST QUESTION
# =========================
else:

    st.subheader("Calculating Result...")

    A = st.session_state.answers.count(0)
    B = st.session_state.answers.count(1)
    C = st.session_state.answers.count(2)
    D = st.session_state.answers.count(3)

    X_input = np.array([[A, B, C, D]])

    prediction = model.predict(X_input)
    career = label_encoder.inverse_transform(prediction)

    st.success(f"🎯 Recommended Career: {career[0]}")
    st.balloons()

    if st.button("Restart Quiz"):
        st.session_state.question_number = 0
        st.session_state.answers = []
        st.rerun()
