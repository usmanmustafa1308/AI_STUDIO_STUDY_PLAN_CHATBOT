
import streamlit as st
import requests
import re
import time

# --- CONFIGURATION ---
API_URL = "http://localhost:8000/generate-study-plan"
STAGES = [
    "attendance", 
    "quiz_score", 
    "assignment_score", 
    "study_hours", 
    "midterm_score"
]
STAGE_LABELS = {
    "attendance": "Attendance Percentage (0.0 to 1.0)",
    "quiz_score": "Quiz Performance (0 to 10)",
    "assignment_score": "Assignment Performance (0 to 10)",
    "study_hours": "Daily Study Hours (0 to 20)",
    "midterm_score": "Midterm Score (0 to 100)"
}
QUESTIONS = {
    "attendance": "Hello! I am your Academic Advisor. Let's start by looking at your attendance. What is your attendance percentage? (e.g., 0.85 for 85%)",
    "quiz_score": "Great. Now, what is your average quiz score? (Scale 0 to 10)",
    "assignment_score": "And how did you perform in your assignments? (Scale 0 to 10)",
    "study_hours": "How many hours do you typically spend studying per day?",
    "midterm_score": "Finally, what was your score in the Midterm examination? (Scale 0 to 100)"
}

st.set_page_config(page_title="AI Academic Advisor", page_icon="🎓", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stChatMessage { border-radius: 15px; }
    .stSidebar { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": QUESTIONS["attendance"]}]

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

if "current_stage_idx" not in st.session_state:
    st.session_state.current_stage_idx = 0

if "completed" not in st.session_state:
    st.session_state.completed = False

def extract_number(text):
    """Extract first floating point or integer number from text."""
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    return float(numbers[0]) if numbers else None

def get_final_plan(payload):
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# --- SIDEBAR (FORM MODE) ---
with st.sidebar:
    st.title("📋 Manual Input")
    st.info("You can use this form or chat with the bot.")
    
    with st.form("manual_entry"):
        f_attendance = st.slider("Attendance", 0.0, 1.0, 0.8)
        f_quiz = st.number_input("Quiz Score", 0, 10, 7)
        f_assignment = st.number_input("Assignment Score", 0, 10, 7)
        f_hours = st.number_input("Study Hours/Day", 0, 20, 4)
        f_midterm = st.number_input("Midterm Score", 0, 100, 70)
        
        submit_btn = st.form_submit_button("Generate Plan via Form")
        
        if submit_btn:
            payload = {
                "attendance": f_attendance,
                "quiz_score": f_quiz,
                "assignment_score": f_assignment,
                "study_hours": f_hours,
                "midterm_score": f_midterm
            }
            with st.spinner("Analyzing risk..."):
                result = get_final_plan(payload)
                if result:
                    st.session_state.messages.append({"role": "assistant", "content": f"Form analysis complete! Your predicted risk score is **{result['risk_score']:.2f}**.\n\n{result['detailed_study_plan']}"})
                    st.success("Plan Generated!")
                else:
                    st.error("Backend offline. Please start FastAPI.")

# --- MAIN CHAT INTERFACE ---
st.title("🎓 AI Student Advisor")
st.write("Helping you navigate academic success with Machine Learning.")

# Progress Bar
progress = (st.session_state.current_stage_idx) / len(STAGES)
st.progress(progress, text=f"Data Collection: {st.session_state.current_stage_idx}/{len(STAGES)}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Logic
if prompt := st.chat_input("Type your response here..."):
    if st.session_state.completed:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": "I have already generated your plan! You can use the sidebar to try again with different values."})
        st.rerun()

    # User's turn
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process numeric value from prompt
    val = extract_number(prompt)
    
    if val is not None:
        current_stage = STAGES[st.session_state.current_stage_idx]
        st.session_state.chat_data[current_stage] = val
        st.session_state.current_stage_idx += 1
        
        # Next Question or Final Process
        if st.session_state.current_stage_idx < len(STAGES):
            next_q = QUESTIONS[STAGES[st.session_state.current_stage_idx]]
            st.session_state.messages.append({"role": "assistant", "content": f"Received. {next_q}"})
        else:
            # Process Everything
            st.session_state.messages.append({"role": "assistant", "content": "I have collected all 5 details. Analyzing your academic profile now..."})
            
            with st.spinner("Running RandomForest Prediction..."):
                result = get_final_plan(st.session_state.chat_data)
                if result:
                    risk_msg = f"Based on my analysis, your academic risk score is **{result['risk_score']:.2f}**."
                    st.session_state.messages.append({"role": "assistant", "content": risk_msg})
                    st.session_state.messages.append({"role": "assistant", "content": result['detailed_study_plan']})
                    st.session_state.completed = True
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "Error: Backend unreachable. Ensure the FastAPI server is running at port 8000."})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "I couldn't detect a number in your response. Please provide a numeric value so I can help you!"})
    
    st.rerun()
