from fastapi import APIRouter, HTTPException
from backend.services.recommender import generate_tips, generate_chat_response
from backend.core.schemas import TipsResponse

router = APIRouter(prefix="/reco", tags=["Recommendations"])

@router.post("/generate", response_model=TipsResponse)
def generate_recommendations(inputs: dict):
    try:
        tips = generate_tips(inputs)
        return TipsResponse(tips=tips)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.post("/chat")
def chat_with_ai(payload: dict):
    try:
        response = generate_chat_response(payload)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chat response: {str(e)}")
