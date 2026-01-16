
# AI-Powered Student Study Plan Chatbot (FYP Project)

This project is a Final Year Project (FYP) demonstration of a Machine Learning based Academic Advisor.

## 🚀 Step-by-Step Run Instructions

### 1. Prerequisites
- Python 3.8+ installed.

### 2. Setup Environment
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Run the Backend (FastAPI)
In terminal 1:
```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run the Frontend (Streamlit)
In terminal 2:
```bash
streamlit run ui/chatbot.py
```

## 🧠 FYP-Level Explanation
- **Machine Learning**: Uses `RandomForestClassifier` trained on historical student performance data (`attendance`, `scores`, `study_hours`).
- **Risk Prediction**: The model outputs the probability of failure (`risk = 1 - P(Pass)`).
- **Adaptive Scheduling**: A heuristic engine generates a Markdown study schedule. If risk is > 0.4, it creates an "Intensive Intervention" plan with more focus on core remediation.
- **Dual Input**: Supports structured Form input via sidebar and Natural Language Processing (regex-based) numeric extraction via a conversational chat interface.
