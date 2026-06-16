"""
购物清单服务
处理购物清单的增删改查，支持智能去重和按品类整理
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from mock_data import CATEGORY_CONFIG


class ShoppingListService:
    """购物清单服务类"""
    
    def __init__(self):
        """初始化购物清单服务"""
        # 存储购物清单数据
        self.shopping_lists: Dict[str, Dict] = {}
        
        # 单位转换配置（转换为克或毫升）
        self.unit_conversions = {
            "公斤": ("克", 1000),
            "千克": ("克", 1000),
            "kg": ("克", 1000),
            "斤": ("克", 500),
            "两": ("克", 50),
            "升": ("毫升", 1000),
            "L": ("毫升", 1000),
            "ml": ("毫升", 1),
            "毫升": ("毫升", 1),
            "克": ("克", 1),
            "g": ("克", 1),
        }
    
    def convert_to_base_unit(self, quantity: float, unit: str) -> tuple:
        """
        将数量转换为基础单位
        
        Args:
            quantity: 数量
            unit: 单位
            
        Returns:
            tuple: (转换后的数量, 基础单位)
        """
        unit_lower = unit.lower().strip()
        
        for key, (base_unit, factor) in self.unit_conversions.items():
            if key in unit_lower:
                return (quantity * factor, base_unit)
        
        return (quantity, unit)
    
    def find_matching_item(
        self,
        items: List[Dict],
        name: str,
        unit: str
    ) -> Optional[Dict]:
        """
        查找匹配的商品项（支持单位转换）
        
        Args:
            items: 商品列表
            name: 商品名称
            unit: 单位
            
        Returns:
            Optional[Dict]: 匹配的商品，如果没有匹配则返回 None
        """
        # 转换为小写进行匹配
        name_lower = name.lower()
        
        for item in items:
            item_name_lower = item["name"].lower()
            
            # 检查名称是否包含匹配
            if name_lower in item_name_lower or item_name_lower in name_lower:
                # 检查单位是否可以转换
                item_qty, item_base_unit = self.convert_to_base_unit(item["quantity"], item["unit"])
                target_qty, target_base_unit = self.convert_to_base_unit(1, unit)
                
                # 如果基础单位相同，可以合并
                if item_base_unit == target_base_unit:
                    return item
        
        return None
    
    def get_shopping_list(self, family_id: str) -> Dict:
        """
        获取购物清单
        
        Args:
            family_id: 家庭 ID
            
        Returns:
            Dict: 购物清单数据
        """
        if family_id not in self.shopping_lists:
            self.shopping_lists[family_id] = {
                "id": f"sl-{uuid.uuid4().hex[:8]}",
                "family_id": family_id,
                "items": [],
                "last_updated": datetime.now()
            }
        
        return self.shopping_lists[family_id]
    
    def add_item(
        self,
        family_id: str,
        name: str,
        quantity: float = 1.0,
        unit: str = "个",
        category: Optional[str] = None
    ) -> Dict:
        """
        添加购物项（智能去重）
        
        Args:
            family_id: 家庭 ID
            name: 商品名称
            quantity: 数量
            unit: 单位
            category: 品类
            
        Returns:
            Dict: 添加的商品项
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        # 检查是否已存在相同商品
        existing_item = self.find_matching_item(items, name, unit)
        
        if existing_item:
            # 合并数量
            old_qty, base_unit = self.convert_to_base_unit(existing_item["quantity"], existing_item["unit"])
            new_qty, _ = self.convert_to_base_unit(quantity, unit)
            
            # 更新数量
            total_qty = old_qty + new_qty
            
            # 转换为合理的显示单位
            if total_qty >= 1000 and base_unit == "克":
                display_qty = total_qty / 1000
                display_unit = "公斤"
            elif total_qty >= 1000 and base_unit == "毫升":
                display_qty = total_qty / 1000
                display_unit = "升"
            else:
                display_qty = total_qty
                display_unit = existing_item["unit"]
            
            existing_item["quantity"] = round(display_qty, 2)
            existing_item["unit"] = display_unit
            existing_item["updated_at"] = datetime.now()
            
            shopping_list["last_updated"] = datetime.now()
            
            return existing_item
        
        # 如果未指定品类，自动分类
        if not category:
            category = self.determine_category(name)
        
        # 创建新商品项
        new_item = {
            "id": f"si-{uuid.uuid4().hex[:8]}",
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "category": category,
            "is_purchased": False,
            "added_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        items.append(new_item)
        shopping_list["last_updated"] = datetime.now()
        
        return new_item
    
    def remove_item(self, family_id: str, item_id: str) -> bool:
        """
        删除购物项
        
        Args:
            family_id: 家庭 ID
            item_id: 商品项 ID
            
        Returns:
            bool: 是否删除成功
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        for i, item in enumerate(items):
            if item["id"] == item_id:
                items.pop(i)
                shopping_list["last_updated"] = datetime.now()
                return True
        
        return False
    
    def toggle_item_status(self, family_id: str, item_id: str) -> Optional[Dict]:
        """
        切换购物项的已购状态
        
        Args:
            family_id: 家庭 ID
            item_id: 商品项 ID
            
        Returns:
            Optional[Dict]: 更新后的商品项
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        for item in items:
            if item["id"] == item_id:
                item["is_purchased"] = not item["is_purchased"]
                item["updated_at"] = datetime.now()
                shopping_list["last_updated"] = datetime.now()
                return item
        
        return None
    
    def update_item(
        self,
        family_id: str,
        item_id: str,
        **updates
    ) -> Optional[Dict]:
        """
        更新购物项
        
        Args:
            family_id: 家庭 ID
            item_id: 商品项 ID
            **updates: 要更新的字段
            
        Returns:
            Optional[Dict]: 更新后的商品项
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        for item in items:
            if item["id"] == item_id:
                for key, value in updates.items():
                    if key in ["name", "quantity", "unit", "category", "is_purchased"]:
                        item[key] = value
                
                item["updated_at"] = datetime.now()
                shopping_list["last_updated"] = datetime.now()
                return item
        
        return None
    
    def clear_purchased_items(self, family_id: str) -> int:
        """
        清除已购买的商品
        
        Args:
            family_id: 家庭 ID
            
        Returns:
            int: 清除的商品数量
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        original_count = len(items)
        items[:] = [item for item in items if not item["is_purchased"]]
        
        cleared_count = original_count - len(items)
        
        if cleared_count > 0:
            shopping_list["last_updated"] = datetime.now()
        
        return cleared_count
    
    def generate_shopping_list_from_meal_plan(
        self,
        family_id: str,
        meal_plan: Dict
    ) -> Dict:
        """
        从食谱计划生成购物清单
        
        Args:
            family_id: 家庭 ID
            meal_plan: 食谱计划数据
            
        Returns:
            Dict: 生成的购物清单
        """
        shopping_list = self.get_shopping_list(family_id)
        
        # 收集所有食材
        all_ingredients = []
        
        for day_meals in meal_plan.get("days", []):
            for meal_type in ["breakfast", "lunch", "dinner"]:
                meal = day_meals.get(meal_type)
                if meal:
                    all_ingredients.extend(meal.get("ingredients", []))
        
        # 添加食材到购物清单
        for ingredient in all_ingredients:
            self.add_meal_plan_items(
                family_id=family_id,
                name=ingredient.get("name", ""),
                quantity=ingredient.get("quantity", 1),
                unit=ingredient.get("unit", "个"),
                category=ingredient.get("category", "other")
            )
        
        return self.get_shopping_list(family_id)
    
    def add_meal_plan_items(
        self,
        family_id: str,
        name: str,
        quantity: float,
        unit: str,
        category: str
    ) -> Dict:
        """
        添加食谱食材到购物清单
        
        Args:
            family_id: 家庭 ID
            name: 食材名称
            quantity: 数量
            unit: 单位
            category: 品类
            
        Returns:
            Dict: 添加的食材项
        """
        return self.add_item(
            family_id=family_id,
            name=name,
            quantity=quantity,
            unit=unit,
            category=category
        )
    
    def determine_category(self, item_name: str) -> str:
        """
        根据商品名称自动判断品类
        
        Args:
            item_name: 商品名称
            
        Returns:
            str: 品类名称
        """
        name_lower = item_name.lower()
        
        # 按优先级排序品类（零食最后判断，避免误判）
        category_order = ["vegetables", "fruits", "proteins", "grains", "dairy", "seasonings", "snacks"]
        
        for category in category_order:
            config = CATEGORY_CONFIG.get(category, {})
            keywords = config.get("keywords", [])
            exclude_patterns = config.get("exclude_patterns", [])
            
            # 先检查是否在排除列表中
            is_excluded = False
            for pattern in exclude_patterns:
                if pattern.lower() in name_lower:
                    is_excluded = True
                    break
            
            if is_excluded:
                continue
            
            # 检查是否匹配关键词
            for keyword in keywords:
                if keyword.lower() in name_lower:
                    return category
        
        return "other"
    
    def get_grouped_shopping_list(self, family_id: str) -> Dict:
        """
        获取按品类分组的购物清单
        
        Args:
            family_id: 家庭 ID
            
        Returns:
            Dict: 按品类分组的购物清单
        """
        shopping_list = self.get_shopping_list(family_id)
        items = shopping_list["items"]
        
        # 按品类分组
        grouped = {}
        
        for item in items:
            category = item.get("category", "other")
            
            if category not in grouped:
                grouped[category] = []
            
            grouped[category].append(item)
        
        # 转换格式
        result = {
            "id": shopping_list["id"],
            "family_id": family_id,
            "grouped_items": {},
            "total_count": len(items),
            "purchased_count": sum(1 for item in items if item.get("is_purchased", False)),
            "last_updated": shopping_list["last_updated"]
        }
        
        # 按品类排序
        category_order = ["vegetables", "fruits", "proteins", "grains", "dairy", "seasonings", "snacks", "other"]
        
        for category in category_order:
            if category in grouped:
                result["grouped_items"][category] = {
                    "display_name": self.get_category_display_name(category),
                    "items": grouped[category],
                    "count": len(grouped[category])
                }
        
        return result
    
    def get_category_display_name(self, category: str) -> str:
        """
        获取品类的中文显示名称
        
        Args:
            category: 品类代码
            
        Returns:
            str: 中文显示名称
        """
        display_names = {
            "vegetables": "🥬 蔬菜",
            "fruits": "🍎 水果",
            "proteins": "🥩 蛋白质",
            "grains": "🍚 主食",
            "dairy": "🥛 乳制品",
            "seasonings": "🧂 调味品",
            "snacks": "🍿 零食",
            "other": "📦 其他"
        }
        
        return display_names.get(category, "📦 其他")
