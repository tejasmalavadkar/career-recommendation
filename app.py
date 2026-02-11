import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="AI Career Advisor", page_icon="🚀")

st.title("🚀 Smart Career Advisor")

# =========================
# LOAD ML MODEL
# =========================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =========================
# MODE SELECTION
# =========================
mode = st.selectbox(
    "Choose Mode",
    ["Mixed Questions (All Domains)", "Category Based Questions"]
)

# =========================
# QUESTION BANK
# =========================
question_bank = {
    "Software Development": [
        "Do you enjoy building applications?",
        "Do you like solving coding problems?",
        "Do you prefer backend or frontend development?"
    ],
    "Data Science": [
        "Do you enjoy analyzing data?",
        "Do you like statistics and math?",
        "Do you enjoy finding patterns in data?"
    ],
    "Cyber Security": [
        "Are you interested in ethical hacking?",
        "Do you enjoy securing systems?",
        "Do you like networking and firewalls?"
    ],
    "UI/UX Design": [
        "Do you enjoy designing interfaces?",
        "Do you like creativity and visual design?",
        "Do you enjoy improving user experience?"
    ]
}

options = ["Strongly Yes", "Yes", "No", "Strongly No"]

# =========================
# MODE 1 → MIXED QUESTIONS
# =========================
if mode == "Mixed Questions (All Domains)":

    st.subheader("Answer Mixed Domain Questions")

    mixed_questions = []
    for domain in question_bank:
        mixed_questions.extend(question_bank[domain])

    user_answers = []

    for i, q in enumerate(mixed_questions):
        answer = st.radio(q, options, key=i)
        user_answers.append(options.index(answer))

    if st.button("Find My Career"):

        A = user_answers.count(0)
        B = user_answers.count(1)
        C = user_answers.count(2)
        D = user_answers.count(3)

        X_input = np.array([[A, B, C, D]])

        prediction = model.predict(X_input)
        career = label_encoder.inverse_transform(prediction)

        st.success(f"🎯 Recommended Career: {career[0]}")
        st.balloons()


# =========================
# MODE 2 → CATEGORY BASED
# =========================
else:

    category = st.selectbox("Select Category", list(question_bank.keys()))
    st.subheader(f"{category} Assessment")

    questions = question_bank[category]
    score = 0

    for i, q in enumerate(questions):
        answer = st.radio(q, options, key=i)
        if answer == "Strongly Yes":
            score += 2
        elif answer == "Yes":
            score += 1

    if st.button("Check My Rating"):

        if score >= 5:
            st.success("🌟 Excellent Fit! You are highly suitable for this domain.")
        elif score >= 3:
            st.warning("👍 Moderate Fit. You can improve and grow in this domain.")
        else:
            st.error("⚠️ Needs Improvement. Consider exploring other domains.")

