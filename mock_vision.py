from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class AnalysisResponse(BaseModel):
    ingredients: List[dict]
    recommendations: List[dict]

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_image():
    return {
        "ingredients": [
            {
                "name": "苹果",
                "confidence": 0.95,
                "nutrition": {
                    "calories": 52,
                    "protein": 0.3,
                    "fat": 0.2,
                    "carbs": 14,
                    "fiber": 2.4,
                    "vitamins": {"C": 4.6}
                }
            },
            {
                "name": "香蕉",
                "confidence": 0.92,
                "nutrition": {
                    "calories": 89,
                    "protein": 1.1,
                    "fat": 0.3,
                    "carbs": 23,
                    "fiber": 2.6,
                    "vitamins": {"B6": 0.4}
                }
            }
        ],
        "recommendations": [
            {"ingredient": "牛奶", "reason": "促进钙吸收", "type": "synergy"},
            {"ingredient": "花生", "reason": "相克组合，不建议同食", "type": "conflict"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)