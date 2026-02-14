import streamlit as st
import pickle
import numpy as np

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Career Guide for 10th Students",
    page_icon="🎓",
    layout="centered"
)

# =============================
# ATTRACTIVE BACKGROUND
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
.block-container {
    padding-top: 40px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
}
.result-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding: 30px;
    border-radius: 25px;
    color: white;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Career Guidance for 10th Students")
st.write("Answer honestly and discover your future career path 🚀")

# =============================
# LOAD MODEL
# =============================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =============================
# START SECTION
# =============================
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Student Information")

    name = st.text_input("Your Name")
    age = st.number_input("Age", 14, 17)

    if st.button("🚀 Start Career Test"):
        st.session_state.started = True
        st.session_state.q = 0
        st.session_state.answers = []
        st.session_state.student_name = name
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# QUIZ SECTION
# =============================
else:

    questions = [
        "I enjoy solving math problems.",
        "I like using computers.",
        "I enjoy drawing or designing.",
        "I am curious about hacking and security.",
        "I enjoy solving puzzles and logical questions.",
        "I like science experiments.",
        "I enjoy gaming and technology.",
        "I like explaining things to others."
    ]

    options = ["Strongly Agree", "Agree", "Neutral", "Disagree"]

    weights = {
        "Strongly Agree": 3,
        "Agree": 2,
        "Neutral": 1,
        "Disagree": 0
    }

    q = st.session_state.q
    st.progress(q / len(questions))

    if q < len(questions):

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"Question {q+1} of {len(questions)}")

        ans = st.radio(questions[q], options, key=q)
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if q > 0:
                if st.button("⬅ Back"):
                    st.session_state.q -= 1
                    st.rerun()

        with col2:
            if q < len(questions)-1:
                if st.button("Next ➡"):
                    st.session_state.answers.append(weights[ans])
                    st.session_state.q += 1
                    st.rerun()
            else:
                if st.button("✅ Submit"):
                    st.session_state.answers.append(weights[ans])
                    st.session_state.q += 1
                    st.rerun()

    # =============================
    # RESULT SECTION
    # =============================
    else:

        strongly = st.session_state.answers.count(3)
        agree = st.session_state.answers.count(2)
        neutral = st.session_state.answers.count(1)
        disagree = st.session_state.answers.count(0)

        X_input = np.array([[strongly, agree, neutral, disagree]])

        prediction = model.predict(X_input)
        probabilities = model.predict_proba(X_input)[0]
        career = label_encoder.inverse_transform(prediction)[0]

        # Result Card
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f"🎉 Congratulations {st.session_state.student_name}!")
        st.markdown(f"### Your Best Career Option is:")
        st.markdown(f"# {career}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Match Percentage
        st.subheader("📊 Career Match Percentage")

        for i, prob in enumerate(probabilities):
            career_name = label_encoder.inverse_transform([i])[0]
            percent = round(prob * 100, 2)
            st.write(f"**{career_name} — {percent}%**")
            st.progress(float(prob))

        # Career Guidance Section
        st.subheader("🛤️ What Should You Do Next?")

        guidance = {
            "Software Engineer": "👉 Choose Science stream (PCM). Start learning basic coding (Python).",
            "Data Scientist": "👉 Focus on Math & Statistics. Learn Python and data basics.",
            "Cybersecurity Analyst": "👉 Choose Science. Learn networking and basic ethical hacking.",
            "Graphic Designer": "👉 Focus on creativity. Learn design tools like Canva, Photoshop.",
            "AI Engineer": "👉 Choose PCM. Learn Python and Machine Learning basics."
        }

        if career in guidance:
            st.success(guidance[career])
        else:
            st.info("👉 Focus on your interests and explore technology-related careers.")

        if st.button("🔄 Restart Test"):
            st.session_state.started = False
            st.rerun()
