
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .model import AcademicModel
from .scheduler import generate_plan

app = FastAPI(title="Student Study API")

# Initialize Model on Startup
academic_model = AcademicModel()

class StudentData(BaseModel):
    attendance: float = Field(..., ge=0, le=1)
    quiz_score: float = Field(..., ge=0, le=10)
    assignment_score: float = Field(..., ge=0, le=10)
    study_hours: float = Field(..., ge=0, le=24)
    midterm_score: float = Field(..., ge=0, le=100)

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Academic Support API is running."}

@app.post("/generate-study-plan")
async def process_student_plan(data: StudentData):
    try:
        risk = academic_model.predict_risk(
            data.attendance, 
            data.quiz_score, 
            data.assignment_score, 
            data.study_hours, 
            data.midterm_score
        )
        
        plan = generate_plan(risk, data.dict())
        
        return {
            "risk_score": risk,
            "detailed_study_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
