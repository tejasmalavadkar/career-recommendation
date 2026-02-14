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
# ANIMATED PARTICLE BACKGROUND 🎨
# =========================
particles = """
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 80},
    "size": {"value": 3},
    "color": {"value": "#ffffff"},
    "line_linked": {"enable": true},
    "move": {"speed": 2}
  }
});
</script>
<style>
#particles-js{
  position:fixed;
  width:100%;
  height:100%;
  z-index:-1;
  top:0;
  left:0;
  background:linear-gradient(to right,#141e30,#243b55);
}
</style>
"""
st.components.v1.html(particles, height=0)

# =========================
# RESPONSIVE CSS 📱
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 30px;
    padding-bottom: 50px;
}
.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 6px 30px rgba(0,0,0,0.4);
}
.result-card {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    padding: 35px;
    border-radius: 25px;
    color:white;
    text-align:center;
}
@media (max-width: 768px) {
    .card {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
with open("career_ml_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# =========================
# NAVIGATION
# =========================
menu = st.radio("", ["🏠 Home", "📝 Career Test"], horizontal=True)

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.title("🚀 Smart Career Advisor Pro")
    st.write("Discover your perfect tech career with AI-powered assessment.")

# =========================
# CAREER TEST
# =========================
elif menu == "📝 Career Test":

    if "start" not in st.session_state:
        st.session_state.start = False

    # =========================
    # USER INFO
    # =========================
    if not st.session_state.start:

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Your Details")

        name = st.text_input("Full Name")
        age = st.number_input("Age", 16, 40)
        field = st.selectbox("Studied Field",
                             ["Science", "Commerce", "Arts", "Diploma", "Other"])
        program = st.selectbox("Program",
                               ["BSc", "BTech", "BE", "Diploma", "MSc"])

        if st.button("🚀 Start Test"):
            st.session_state.start = True
            st.session_state.q = 0
            st.session_state.ans = []
            st.session_state.user = name
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        questions = [
            "I enjoy building applications.",
            "I like analyzing data.",
            "Cybersecurity interests me.",
            "I enjoy UI/UX design.",
            "I love programming challenges.",
            "Math & statistics excite me.",
            "I enjoy networking concepts.",
            "Creativity attracts me."
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
                        st.session_state.ans.append(weights[ans])
                        st.session_state.q += 1
                        st.rerun()
                else:
                    if st.button("✅ Submit"):
                        st.session_state.ans.append(weights[ans])
                        st.session_state.q += 1
                        st.rerun()

        else:

            strongly = st.session_state.ans.count(3)
            agree = st.session_state.ans.count(2)
            neutral = st.session_state.ans.count(1)
            disagree = st.session_state.ans.count(0)

            X_input = np.array([[strongly, agree, neutral, disagree]])

            prediction = model.predict(X_input)
            probabilities = model.predict_proba(X_input)[0]
            career = label_encoder.inverse_transform(prediction)[0]

            # =========================
            # RESULT CARD 🏆
            # =========================
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"🎉 {st.session_state.user}, Your Ideal Career is")
            st.markdown(f"# {career}")
            st.markdown('</div>', unsafe_allow_html=True)

            # =========================
            # CAREER DESCRIPTION CARD 🏆
            # =========================
            career_info = {
                "Data Scientist": {
                    "desc": "Analyze data to find patterns and build predictive models.",
                    "skills": "Python, ML, Statistics",
                    "salary": "₹6L - ₹20L per year"
                },
                "Full Stack Developer": {
                    "desc": "Build complete web applications (frontend + backend).",
                    "skills": "HTML, CSS, JS, Node, DB",
                    "salary": "₹4L - ₹15L per year"
                },
                "Cybersecurity Analyst": {
                    "desc": "Protect systems from cyber attacks.",
                    "skills": "Networking, Security Tools",
                    "salary": "₹5L - ₹18L per year"
                }
            }

            if career in career_info:
                info = career_info[career]
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🏆 Career Overview")
                st.write(f"**Role:** {info['desc']}")
                st.write(f"**Skills Needed:** {info['skills']}")
                st.write(f"**Salary Range:** {info['salary']}")
                st.markdown('</div>', unsafe_allow_html=True)

            # =========================
            # PERCENTAGES
            # =========================
            st.subheader("📊 Match Percentage")
            for i, prob in enumerate(probabilities):
                career_name = label_encoder.inverse_transform([i])[0]
                st.progress(float(prob))

            if st.button("🔄 Restart"):
                st.session_state.start = False
                st.rerun()
