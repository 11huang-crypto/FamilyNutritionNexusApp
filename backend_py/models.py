"""
Pydantic 数据模型定义
用于请求/响应的数据验证
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class NutritionInfo(BaseModel):
    """营养信息模型"""
    calories: int = Field(..., description="卡路里 (kcal)")
    protein: float = Field(..., description="蛋白质 (g)")
    carbs: float = Field(..., description="碳水化合物 (g)")
    fat: float = Field(..., description="脂肪 (g)")


class DietaryPreference(BaseModel):
    """饮食偏好模型"""
    cuisine_type: List[str] = Field(default_factory=list, description="菜系类型")
    dislikes: List[str] = Field(default_factory=list, description="不喜欢食材")
    meal_schedule: Optional[dict] = Field(default=None, description="用餐时间安排")


class FamilyMember(BaseModel):
    """家庭成员模型"""
    id: str
    name: str
    age: int
    nutrition_goals: NutritionInfo
    preferences: DietaryPreference
    allergies: List[str] = Field(default_factory=list, description="食物过敏")


class GenerateMealPlanRequest(BaseModel):
    """生成食谱计划请求"""
    family_id: str = Field(default="family-1", description="家庭 ID")
    start_date: Optional[str] = Field(default=None, description="开始日期 (YYYY-MM-DD)")
    days: int = Field(default=7, description="生成天数")
    include_shopping_list: bool = Field(default=True, description="是否包含购物清单")


class Meal(BaseModel):
    """餐点模型"""
    id: str
    name: str
    meal_type: str  # breakfast, lunch, dinner
    recipe_id: str
    nutrition: NutritionInfo
    ingredients: List[dict]
    cooking_time: int  # 分钟


class DayMeals(BaseModel):
    """一天三餐模型"""
    day: str
    date: str
    breakfast: Optional[Meal] = None
    lunch: Optional[Meal] = None
    dinner: Optional[Meal] = None


class MealPlan(BaseModel):
    """食谱计划模型"""
    id: str
    family_id: str
    start_date: str
    end_date: str
    days: List[DayMeals]
    total_nutrition: NutritionInfo
    created_at: datetime


class ShoppingItem(BaseModel):
    """购物清单项模型"""
    id: str
    name: str
    quantity: float
    unit: str
    category: str
    is_purchased: bool = False
    added_at: datetime
    updated_at: datetime


class ShoppingList(BaseModel):
    """购物清单模型"""
    id: str
    family_id: str
    items: List[ShoppingItem]
    last_updated: datetime


class AddItemRequest(BaseModel):
    """添加购物项请求"""
    name: str
    quantity: float = 1.0
    unit: str = "个"
    category: str = "other"


class UpdateItemRequest(BaseModel):
    """更新购物项请求"""
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    is_purchased: Optional[bool] = None
