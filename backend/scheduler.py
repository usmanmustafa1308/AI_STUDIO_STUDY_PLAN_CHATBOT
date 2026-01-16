
def generate_plan(risk_score, student_data):
    is_high_risk = risk_score > 0.4
    
    # Adaptive configuration
    daily_limit = 6 # Max 6 hours
    plan_type = "Intensive Intervention" if is_high_risk else "Standard Balanced"
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Priority subjects based on scores
    priorities = []
    if student_data['quiz_score'] < 6: priorities.append("Quiz Review & Fundamentals")
    if student_data['assignment_score'] < 6: priorities.append("Assignment & Practical Application")
    if student_data['midterm_score'] < 50: priorities.append("Core Concept Remediation")
    
    if not priorities:
        priorities.append("Advanced Topics & Research")

    plan_str = f"### {plan_type} Study Plan (Risk: {risk_score:.2f})\n"
    plan_str += f"**Overall Status:** {'High Risk - Focus on Core Reinforcement' if is_high_risk else 'Healthy Progress - Maintain Consistency'}\n\n"
    
    for day in days:
        plan_str += f"#### {day}\n"
        if is_high_risk:
            plan_str += f"- **08:00 - 10:00:** {priorities[0]} (Priority Focus)\n"
            plan_str += "- **10:00 - 10:30:** Short Break\n"
            plan_str += "- **10:30 - 12:30:** Subject Revision (Midterm Prep)\n"
            plan_str += "- **12:30 - 14:00:** Lunch & Rest\n"
            plan_str += "- **14:00 - 16:00:** Practice Quizzes & Exercises\n"
        else:
            plan_str += "- **09:00 - 11:00:** New Topic Coverage\n"
            plan_str += "- **11:00 - 11:30:** Short Break\n"
            plan_str += "- **11:30 - 13:00:** Assignment Work\n"
            plan_str += "- **13:00 - 14:30:** Lunch & Rest\n"
            plan_str += "- **14:30 - 16:00:** Subject Review & Summary Notes\n"
        plan_str += "\n"
        
    plan_str += "---\n**Advisor Notes:** "
    if is_high_risk:
        plan_str += "Your current performance indicates a need for immediate intervention. Focus on fundamental concepts and attend all remaining lectures."
    else:
        plan_str += "You are doing well! Keep this pace up to ensure a strong final grade."
        
    return plan_str
