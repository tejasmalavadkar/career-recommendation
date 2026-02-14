import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Career Advisor Pro",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CUSTOM CSS (PREMIUM UI)
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
}
.navbar {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
}
.card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
}
.result-card {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    color: white;
    font-size: 22px;
    box-shadow: 0px 8px 40px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =========================
# NAVIGATION BAR
# =========================
menu = st.radio(
    "",
    ["🏠 Home", "📝 Career Test", "ℹ About"],
    horizontal=True
)

# =========================
# HOME PAGE
# =========================
if menu == "🏠 Home":

    st.title("🚀 Smart Career Advisor Pro")
    st.markdown("""
    ### Discover Your Perfect Tech Career Path  
    Powered by Machine Learning 🧠  
    Take our smart assessment and unlock your future.
    """)

# =========================
# ABOUT PAGE
# =========================
elif menu == "ℹ About":

    st.title("ℹ About This Project")
    st.write("""
    This AI-powered system analyzes your interests
    and predicts the best tech career for you using
    Machine Learning.
    """)

# =========================
# CAREER TEST PAGE
# =========================
elif menu == "📝 Career Test":

    # =========================
    # USER INFO FORM
    # =========================
    if "start_quiz" not in st.session_state:
        st.session_state.start_quiz = False

    if not st.session_state.start_quiz:

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Enter Your Details")

        name = st.text_input("Full Name")
        age = st.number_input("Age", 16, 40)
        field = st.selectbox("Studied Field", 
                             ["Science", "Commerce", "Arts", "Diploma", "Other"])
        program = st.selectbox("Current Program",
                               ["BSc", "BTech", "BE", "Diploma", "MSc", "Other"])

        if st.button("🚀 Start Career Test"):
            st.session_state.start_quiz = True
            st.session_state.question_number = 0
            st.session_state.answers = []
            st.session_state.user_name = name
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # QUIZ SECTION
    # =========================
    else:

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

        options = ["Strongly Agree", "Agree", "Neutral", "Disagree"]

        weights = {
            "Strongly Agree": 3,
            "Agree": 2,
            "Neutral": 1,
            "Disagree": 0
        }

        q_no = st.session_state.question_number

        progress = q_no / len(questions)
        st.progress(progress)

        if q_no < len(questions):

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"Question {q_no+1} of {len(questions)}")

            answer = st.radio(
                questions[q_no],
                options,
                key=q_no
            )

            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                if q_no > 0:
                    if st.button("⬅ Back"):
                        st.session_state.question_number -= 1
                        st.rerun()

            with col2:
                if q_no < len(questions)-1:
                    if st.button("Next ➡"):
                        st.session_state.answers.append(weights[answer])
                        st.session_state.question_number += 1
                        st.rerun()
                else:
                    if st.button("✅ Submit"):
                        st.session_state.answers.append(weights[answer])
                        st.session_state.question_number += 1
                        st.rerun()

        # =========================
        # RESULT PAGE
        # =========================
        else:

            strongly = st.session_state.answers.count(3)
            agree = st.session_state.answers.count(2)
            neutral = st.session_state.answers.count(1)
            disagree = st.session_state.answers.count(0)

            X_input = np.array([[strongly, agree, neutral, disagree]])

            prediction = model.predict(X_input)
            probabilities = model.predict_proba(X_input)[0]
            career = label_encoder.inverse_transform(prediction)[0]

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"🎉 Congratulations {st.session_state.user_name}!")
            st.markdown(f"### Your Ideal Career is:")
            st.markdown(f"# {career}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("📊 Career Match Percentages")

            for i, prob in enumerate(probabilities):
                career_name = label_encoder.inverse_transform([i])[0]
                st.progress(float(prob))

            # Radar Chart
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

            if st.button("🔄 Restart Test"):
                st.session_state.start_quiz = False
                st.rerun()
