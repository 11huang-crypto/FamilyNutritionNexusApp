"""
食谱推荐服务
基于家庭成员的营养目标、偏好和禁忌，生成一周食谱计划
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from mock_data import RECIPES, FAMILY_MEMBERS, FAMILIES


class MealPlanService:
    """食谱推荐服务类"""
    
    def __init__(self):
        """初始化食谱推荐服务"""
        self.recipes = RECIPES
        self.family_members = FAMILY_MEMBERS
        self.families = FAMILIES
    
    def get_family_members(self, family_id: str) -> List[Dict]:
        """
        获取家庭成员列表
        
        Args:
            family_id: 家庭 ID
            
        Returns:
            List[Dict]: 家庭成员列表
        """
        family = self.families.get(family_id)
        if not family:
            return []
        
        member_ids = family.get("members", [])
        return [
            self.family_members[mid]
            for mid in member_ids
            if mid in self.family_members
        ]
    
    def calculate_daily_nutrition(self, members: List[Dict]) -> Dict:
        """
        计算家庭每日所需营养总量
        
        Args:
            members: 家庭成员列表
            
        Returns:
            Dict: 每日营养需求
        """
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for member in members:
            goals = member.get("nutrition_goals", {})
            total_calories += goals.get("calories", 2000)
            total_protein += goals.get("protein", 60)
            total_carbs += goals.get("carbs", 250)
            total_fat += goals.get("fat", 60)
        
        return {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat
        }
    
    def get_allergies(self, members: List[Dict]) -> List[str]:
        """
        获取所有家庭成员的食物过敏列表
        
        Args:
            members: 家庭成员列表
            
        Returns:
            List[str]: 过敏食材列表
        """
        allergies = set()
        for member in members:
            allergies.update(member.get("allergies", []))
        return list(allergies)
    
    def get_dislikes(self, members: List[Dict]) -> List[str]:
        """
        获取所有家庭成员不喜欢食材列表
        
        Args:
            members: 家庭成员列表
            
        Returns:
            List[str]: 不喜欢食材列表
        """
        dislikes = set()
        for member in members:
            prefs = member.get("preferences", {})
            dislikes.update(prefs.get("dislikes", []))
        return list(dislikes)
    
    def filter_recipes(
        self,
        recipes: List[Dict],
        allergies: List[str],
        dislikes: List[str],
        meal_type: Optional[str] = None
    ) -> List[Dict]:
        """
        根据过敏和不喜好筛选食谱
        
        Args:
            recipes: 食谱列表
            allergies: 过敏食材列表
            dislikes: 不喜欢食材列表
            meal_type: 餐次类型 (breakfast/lunch/dinner)
            
        Returns:
            List[Dict]: 筛选后的食谱列表
        """
        filtered = []
        
        for recipe in recipes:
            # 检查是否适合该餐次
            if meal_type and meal_type not in recipe.get("meal_type", []):
                continue
            
            # 检查过敏
            ingredients = recipe.get("ingredients", [])
            has_allergy = False
            
            for ingredient in ingredients:
                name = ingredient.get("name", "")
                for allergy in allergies:
                    if allergy in name:
                        has_allergy = True
                        break
                if has_allergy:
                    break
            
            if has_allergy:
                continue
            
            # 检查不喜好
            has_dislike = False
            for ingredient in ingredients:
                name = ingredient.get("name", "")
                for dislike in dislikes:
                    if dislike in name:
                        has_dislike = True
                        break
                if has_dislike:
                    break
            
            if has_dislike:
                continue
            
            filtered.append(recipe)
        
        return filtered
    
    def select_recipe(
        self,
        available_recipes: List[Dict],
        used_recipe_ids: set,
        target_nutrition: Dict,
        meal_type: str
    ) -> Optional[Dict]:
        """
        选择最佳食谱
        
        Args:
            available_recipes: 可用食谱列表
            used_recipe_ids: 已使用食谱 ID 集合
            target_nutrition: 目标营养值
            meal_type: 餐次类型
            
        Returns:
            Optional[Dict]: 最佳食谱
        """
        candidates = [r for r in available_recipes if r["id"] not in used_recipe_ids]
        
        if not candidates:
            candidates = available_recipes
        
        # 计算每餐的目标营养
        meal_targets = {
            "breakfast": 0.25,
            "lunch": 0.40,
            "dinner": 0.35
        }
        
        ratio = meal_targets.get(meal_type, 0.33)
        
        # 选择营养最接近目标的食谱
        best_recipe = None
        best_score = float('inf')
        
        for recipe in candidates:
            nutrition = recipe.get("nutrition", {})
            
            # 计算与目标的差距
            calorie_diff = abs(nutrition.get("calories", 0) - target_nutrition.get("calories", 2000) * ratio)
            protein_diff = abs(nutrition.get("protein", 0) - target_nutrition.get("protein", 60) * ratio)
            
            # 综合评分（归一化）
            score = calorie_diff / 100 + protein_diff * 2
            
            if score < best_score:
                best_score = score
                best_recipe = recipe
        
        return best_recipe
    
    def create_meal(
        self,
        recipe: Dict,
        meal_type: str,
        day_index: int
    ) -> Dict:
        """
        创建餐点对象
        
        Args:
            recipe: 食谱数据
            meal_type: 餐次类型
            day_index: 第几天
            
        Returns:
            Dict: 餐点数据
        """
        return {
            "id": f"meal-{day_index}-{meal_type}-{recipe['id']}",
            "name": recipe["name"],
            "meal_type": meal_type,
            "recipe_id": recipe["id"],
            "nutrition": recipe["nutrition"],
            "ingredients": recipe["ingredients"],
            "cooking_time": recipe["cooking_time"]
        }
    
    def generate_weekly_plan(
        self,
        family_id: str,
        start_date: Optional[str] = None,
        days: int = 7
    ) -> Dict:
        """
        生成一周食谱计划
        
        Args:
            family_id: 家庭 ID
            start_date: 开始日期 (YYYY-MM-DD)
            days: 生成天数
            
        Returns:
            Dict: 食谱计划数据
        """
        # 获取家庭成员
        members = self.get_family_members(family_id)
        if not members:
            members = [self.family_members["member-1"]]
        
        # 计算营养需求
        daily_nutrition = self.calculate_daily_nutrition(members)
        
        # 获取过敏和不喜好
        allergies = self.get_allergies(members)
        dislikes = self.get_dislikes(members)
        
        # 解析开始日期
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start = datetime.now()
        
        # 生成每日食谱
        weekly_plan = []
        used_recipe_ids = set()
        total_nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        
        meal_types = ["breakfast", "lunch", "dinner"]
        meal_names = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}
        
        for day in range(days):
            current_date = start + timedelta(days=day)
            
            day_meals = {
                "day": f"第{day + 1}天",
                "date": current_date.strftime("%Y-%m-%d"),
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][current_date.weekday()]
            }
            
            for meal_type in meal_types:
                # 筛选可用食谱
                available = self.filter_recipes(
                    list(self.recipes.values()),
                    allergies,
                    dislikes,
                    meal_type
                )
                
                if not available:
                    continue
                
                # 选择最佳食谱
                selected = self.select_recipe(
                    available,
                    used_recipe_ids,
                    daily_nutrition,
                    meal_type
                )
                
                if selected:
                    # 创建餐点
                    meal = self.create_meal(selected, meal_type, day)
                    day_meals[meal_type] = meal
                    
                    # 更新已使用食谱
                    used_recipe_ids.add(selected["id"])
                    
                    # 累加营养
                    for key in total_nutrition:
                        total_nutrition[key] += selected["nutrition"].get(key, 0)
            
            weekly_plan.append(day_meals)
        
        # 生成食谱计划
        meal_plan = {
            "id": f"mp-{uuid.uuid4().hex[:8]}",
            "family_id": family_id,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": (start + timedelta(days=days-1)).strftime("%Y-%m-%d"),
            "days": weekly_plan,
            "total_nutrition": {
                "calories": int(total_nutrition["calories"]),
                "protein": round(total_nutrition["protein"], 1),
                "carbs": round(total_nutrition["carbs"], 1),
                "fat": round(total_nutrition["fat"], 1)
            },
            "created_at": datetime.now()
        }
        
        return meal_plan
    
    def get_meal_plan(self, meal_plan_id: str) -> Optional[Dict]:
        """
        获取食谱计划
        
        Args:
            meal_plan_id: 食谱计划 ID
            
        Returns:
            Optional[Dict]: 食谱计划数据
        """
        # 当前实现返回 None，实际项目中应该从数据库查询
        return None
