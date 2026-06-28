from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

class MealPlanResponse(BaseModel):
    week: str
    meals: List[dict]

class ShoppingListResponse(BaseModel):
    items: List[dict]
    last_updated: datetime

class MealPlanRequest(BaseModel):
    family_id: int
    health_restrictions: List[str] = []

@app.post("/meal-plan/generate", response_model=MealPlanResponse)
def generate_meal_plan(request: MealPlanRequest):
    family_id = request.family_id
    health_restrictions = request.health_restrictions
    return {
        "week": "2026-06-16 ~ 2026-06-22",
        "meals": [
            {"day": "周一", "breakfast": "燕麦粥+鸡蛋", "lunch": "清蒸鱼+青菜", "dinner": "鸡胸肉沙拉", "snacks": ["苹果"]},
            {"day": "周二", "breakfast": "全麦面包+牛奶", "lunch": "杂粮饭+番茄炒蛋", "dinner": "豆腐汤+凉拌黄瓜", "snacks": ["坚果"]},
            {"day": "周三", "breakfast": "豆浆+油条", "lunch": "牛肉面", "dinner": "清蒸虾+西兰花", "snacks": ["香蕉"]},
            {"day": "周四", "breakfast": "粥+小菜", "lunch": "鸡肉炒饭", "dinner": "蔬菜豆腐煲", "snacks": ["酸奶"]},
            {"day": "周五", "breakfast": "三明治", "lunch": "红烧肉+土豆", "dinner": "酸菜鱼", "snacks": ["橙子"]},
            {"day": "周六", "breakfast": "葱油饼", "lunch": "火锅", "dinner": "烧烤", "snacks": ["西瓜"]},
            {"day": "周日", "breakfast": "小笼包", "lunch": "披萨", "dinner": "意大利面", "snacks": ["葡萄"]}
        ]
    }

@app.get("/shopping-list/realtime", response_model=ShoppingListResponse)
def get_shopping_list(family_id: int):
    return {
        "items": [
            {"name": "苹果", "quantity": "5个", "category": "水果", "purchased": False},
            {"name": "香蕉", "quantity": "3根", "category": "水果", "purchased": False},
            {"name": "鸡胸肉", "quantity": "500g", "category": "肉类", "purchased": True},
            {"name": "西兰花", "quantity": "300g", "category": "蔬菜", "purchased": False},
            {"name": "鸡蛋", "quantity": "10个", "category": "蛋类", "purchased": True},
            {"name": "牛奶", "quantity": "2盒", "category": "乳品", "purchased": False}
        ],
        "last_updated": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)