# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from crewai_script import run_market_research
from question_generator import generate_questions

class ResearchRequest(BaseModel):
    objective: str
    category: str
    subcategory: str
    age: str
    income: str
    location: str
    num_questions: int

app = FastAPI(
    title="Market Research API",
    description="API for generating market research questions with customizable question count"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Market Research API",
        "endpoints": {
            "Generate Questions": "/research",
            "View Categories": "/categories",
            "Documentation": "/docs"
        }
    }

@app.get("/categories")
async def get_categories():
    """Return available categories and subcategories."""
    categories = {
        "Electronics": ["Tablets", "Laptops", "Smartwatches"],
        "Fitness": ["Fitness Trackers", "Gym Equipment"],
        "Appliances": ["Refrigerators", "Microwaves"],
        "Luxury Fashion": ["Apparel","shoes"]
    }
    return categories

@app.post("/research")
async def start_research(request: ResearchRequest):
    try:
        # Run market research
        run_market_research(request.category, request.subcategory)
        
        # Generate context for questions
        context = (
            f"Objective: {request.objective}, Age: {request.age}, "
            f"Income: {request.income}, Location: {request.location}"
        )
        
        # Generate questions with user-specified count
        questions = generate_questions(
            request.category,
            request.subcategory,
            context,
            request.num_questions  # Use the user-provided number
        )
        
        return {
            "status": "success",
            "data": {
                "questions": questions,
                "metadata": {
                    "category": request.category,
                    "subcategory": request.subcategory,
                    "requested_questions": request.num_questions,
                    "generated_questions": len(questions)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)