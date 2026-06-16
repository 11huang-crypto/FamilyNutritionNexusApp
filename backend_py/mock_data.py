"""
模拟数据
包含食谱库和家庭成员数据
"""

# 12道食谱的完整信息
RECIPES = {
    "recipe-1": {
        "id": "recipe-1",
        "name": "清蒸鲈鱼",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 180,
            "protein": 25.0,
            "carbs": 2.0,
            "fat": 8.0
        },
        "ingredients": [
            {"name": "鲈鱼", "quantity": 600, "unit": "克", "category": "proteins"},
            {"name": "葱", "quantity": 4, "unit": "根", "category": "vegetables"},
            {"name": "姜", "quantity": 5, "unit": "片", "category": "vegetables"},
            {"name": "料酒", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "生抽", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "香油", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 25,
        "difficulty": "easy",
        "suitable_for": ["减脂", "高蛋白"]
    },
    "recipe-2": {
        "id": "recipe-2",
        "name": "清炒西兰花虾仁",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 150,
            "protein": 20.0,
            "carbs": 5.0,
            "fat": 6.0
        },
        "ingredients": [
            {"name": "西兰花", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "虾仁", "quantity": 200, "unit": "克", "category": "proteins"},
            {"name": "蒜", "quantity": 3, "unit": "瓣", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "橄榄油", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 15,
        "difficulty": "easy",
        "suitable_for": ["减脂", "高蛋白", "低碳水"]
    },
    "recipe-3": {
        "id": "recipe-3",
        "name": "西红柿炒蛋",
        "meal_type": ["breakfast", "lunch", "dinner"],
        "nutrition": {
            "calories": 200,
            "protein": 12.0,
            "carbs": 10.0,
            "fat": 14.0
        },
        "ingredients": [
            {"name": "西红柿", "quantity": 2, "unit": "个", "category": "vegetables"},
            {"name": "鸡蛋", "quantity": 3, "unit": "个", "category": "proteins"},
            {"name": "葱", "quantity": 2, "unit": "根", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "花生油", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 15,
        "difficulty": "easy",
        "suitable_for": ["快手菜", "家常"]
    },
    "recipe-4": {
        "id": "recipe-4",
        "name": "燕麦牛奶杯",
        "meal_type": ["breakfast"],
        "nutrition": {
            "calories": 280,
            "protein": 12.0,
            "carbs": 45.0,
            "fat": 8.0
        },
        "ingredients": [
            {"name": "燕麦", "quantity": 60, "unit": "克", "category": "grains"},
            {"name": "牛奶", "quantity": 200, "unit": "毫升", "category": "dairy"},
            {"name": "香蕉", "quantity": 1, "unit": "根", "category": "fruits"},
            {"name": "蓝莓", "quantity": 30, "unit": "克", "category": "fruits"}
        ],
        "cooking_time": 5,
        "difficulty": "easy",
        "suitable_for": ["快手早餐", "高纤维"]
    },
    "recipe-5": {
        "id": "recipe-5",
        "name": "杂粮粥",
        "meal_type": ["breakfast"],
        "nutrition": {
            "calories": 220,
            "protein": 8.0,
            "carbs": 48.0,
            "fat": 3.0
        },
        "ingredients": [
            {"name": "大米", "quantity": 100, "unit": "克", "category": "grains"},
            {"name": "小米", "quantity": 30, "unit": "克", "category": "grains"},
            {"name": "黑米", "quantity": 20, "unit": "克", "category": "grains"},
            {"name": "红枣", "quantity": 5, "unit": "颗", "category": "grains"}
        ],
        "cooking_time": 40,
        "difficulty": "easy",
        "suitable_for": ["养生", "易消化"]
    },
    "recipe-6": {
        "id": "recipe-6",
        "name": "煎蛋",
        "meal_type": ["breakfast"],
        "nutrition": {
            "calories": 180,
            "protein": 10.0,
            "carbs": 1.0,
            "fat": 15.0
        },
        "ingredients": [
            {"name": "鸡蛋", "quantity": 2, "unit": "个", "category": "proteins"},
            {"name": "盐", "quantity": 1, "unit": "小勺", "category": "seasonings"},
            {"name": "花生油", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 10,
        "difficulty": "easy",
        "suitable_for": ["快手菜", "高蛋白"]
    },
    "recipe-7": {
        "id": "recipe-7",
        "name": "清蒸鸡胸肉",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 165,
            "protein": 31.0,
            "carbs": 0.0,
            "fat": 3.6
        },
        "ingredients": [
            {"name": "鸡胸肉", "quantity": 200, "unit": "克", "category": "proteins"},
            {"name": "葱", "quantity": 2, "unit": "根", "category": "vegetables"},
            {"name": "姜", "quantity": 3, "unit": "片", "category": "vegetables"},
            {"name": "料酒", "quantity": 1, "unit": "勺", "category": "seasonings"},
            {"name": "生抽", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 20,
        "difficulty": "easy",
        "suitable_for": ["减脂", "高蛋白", "低碳水"]
    },
    "recipe-8": {
        "id": "recipe-8",
        "name": "番茄炒蛋",
        "meal_type": ["breakfast", "lunch", "dinner"],
        "nutrition": {
            "calories": 190,
            "protein": 11.0,
            "carbs": 12.0,
            "fat": 13.0
        },
        "ingredients": [
            {"name": "番茄", "quantity": 200, "unit": "克", "category": "vegetables"},
            {"name": "鸡蛋", "quantity": 2, "unit": "个", "category": "proteins"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "白糖", "quantity": 1, "unit": "勺", "category": "seasonings"},
            {"name": "花生油", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 15,
        "difficulty": "easy",
        "suitable_for": ["家常", "开胃"]
    },
    "recipe-9": {
        "id": "recipe-9",
        "name": "豆腐汤",
        "meal_type": ["breakfast", "lunch", "dinner"],
        "nutrition": {
            "calories": 120,
            "protein": 10.0,
            "carbs": 5.0,
            "fat": 7.0
        },
        "ingredients": [
            {"name": "豆腐", "quantity": 200, "unit": "克", "category": "vegetables"},
            {"name": "鸡蛋", "quantity": 1, "unit": "个", "category": "proteins"},
            {"name": "葱", "quantity": 2, "unit": "根", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "香油", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 15,
        "difficulty": "easy",
        "suitable_for": ["清淡", "养生"]
    },
    "recipe-10": {
        "id": "recipe-10",
        "name": "蒜蓉菠菜",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 80,
            "protein": 5.0,
            "carbs": 4.0,
            "fat": 5.0
        },
        "ingredients": [
            {"name": "菠菜", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "蒜", "quantity": 3, "unit": "瓣", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "橄榄油", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 10,
        "difficulty": "easy",
        "suitable_for": ["减脂", "高铁"]
    },
    "recipe-11": {
        "id": "recipe-11",
        "name": "黑米红枣粥",
        "meal_type": ["breakfast", "lunch", "dinner"],
        "nutrition": {
            "calories": 250,
            "protein": 6.0,
            "carbs": 52.0,
            "fat": 2.0
        },
        "ingredients": [
            {"name": "黑米", "quantity": 80, "unit": "克", "category": "grains"},
            {"name": "红枣", "quantity": 10, "unit": "颗", "category": "grains"},
            {"name": "水", "quantity": 1000, "unit": "毫升", "category": "other"}
        ],
        "cooking_time": 60,
        "difficulty": "medium",
        "suitable_for": ["养生", "补血"]
    },
    "recipe-12": {
        "id": "recipe-12",
        "name": "荞麦凉面",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 280,
            "protein": 8.0,
            "carbs": 55.0,
            "fat": 5.0
        },
        "ingredients": [
            {"name": "荞麦面", "quantity": 200, "unit": "克", "category": "grains"},
            {"name": "黄瓜", "quantity": 100, "unit": "克", "category": "vegetables"},
            {"name": "醋", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "生抽", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "香油", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 20,
        "difficulty": "easy",
        "suitable_for": ["减脂", "快手"]
    }
}

# 4位家庭成员信息
FAMILY_MEMBERS = {
    "member-1": {
        "id": "member-1",
        "name": "爸爸",
        "age": 40,
        "nutrition_goals": {
            "calories": 2200,
            "protein": 80.0,
            "carbs": 250.0,
            "fat": 70.0
        },
        "preferences": {
            "cuisine_type": ["家常菜", "清淡"],
            "dislikes": ["太辣", "太咸"],
            "meal_schedule": {
                "breakfast": "7:00-8:00",
                "lunch": "12:00-13:00",
                "dinner": "18:00-19:00"
            }
        },
        "allergies": []
    },
    "member-2": {
        "id": "member-2",
        "name": "妈妈",
        "age": 38,
        "nutrition_goals": {
            "calories": 1800,
            "protein": 65.0,
            "carbs": 200.0,
            "fat": 55.0
        },
        "preferences": {
            "cuisine_type": ["养生", "清淡"],
            "dislikes": ["太油腻"],
            "meal_schedule": {
                "breakfast": "7:30-8:30",
                "lunch": "12:00-13:00",
                "dinner": "18:00-19:00"
            }
        },
        "allergies": []
    },
    "member-3": {
        "id": "member-3",
        "name": "小明",
        "age": 12,
        "nutrition_goals": {
            "calories": 2000,
            "protein": 70.0,
            "carbs": 280.0,
            "fat": 60.0
        },
        "preferences": {
            "cuisine_type": ["甜", "可口"],
            "dislikes": ["苦瓜", "青椒"],
            "meal_schedule": {
                "breakfast": "7:00-7:30",
                "lunch": "12:00-13:00",
                "dinner": "18:00-18:30"
            }
        },
        "allergies": ["虾"]
    },
    "member-4": {
        "id": "member-4",
        "name": "奶奶",
        "age": 65,
        "nutrition_goals": {
            "calories": 1600,
            "protein": 55.0,
            "carbs": 200.0,
            "fat": 50.0
        },
        "preferences": {
            "cuisine_type": ["软烂", "易消化"],
            "dislikes": ["太硬", "太辣"],
            "meal_schedule": {
                "breakfast": "8:00-9:00",
                "lunch": "11:30-12:30",
                "dinner": "17:30-18:30"
            }
        },
        "allergies": []
    }
}

# 家庭信息
FAMILIES = {
    "family-1": {
        "id": "family-1",
        "name": "张三家庭",
        "members": ["member-1", "member-2", "member-3", "member-4"]
    }
}

# 品类分类配置
CATEGORY_CONFIG = {
    "vegetables": {
        "keywords": ["西红柿", "番茄", "西兰花", "菠菜", "黄瓜", "土豆", "红薯", "山药", "藕", "南瓜",
                    "白菜", "青菜", "生菜", "芹菜", "韭菜", "蒜", "葱", "姜", "洋葱", "胡萝卜",
                    "白萝卜", "冬瓜", "丝瓜", "苦瓜", "茄子", "青椒", "辣椒", "豆角", "四季豆",
                    "荷兰豆", "香菇", "蘑菇", "木耳", "金针菇", "豆腐", "腐竹", "豆皮"],
        "exclude_patterns": ["薯片", "薯条", "土豆泥"]
    },
    "fruits": {
        "keywords": ["苹果", "香蕉", "橙子", "葡萄", "西瓜", "哈密瓜", "芒果", "草莓", "蓝莓",
                    "猕猴桃", "火龙果", "菠萝", "柚子", "梨", "桃子", "杏子", "樱桃", "荔枝",
                    "龙眼", "石榴", "枇杷", "椰子", "百香果", "牛油果", "柠檬"],
        "exclude_patterns": []
    },
    "proteins": {
        "keywords": ["鸡蛋", "鸡胸肉", "鸡腿肉", "猪肉", "牛肉", "羊肉", "鱼肉", "虾", "虾仁",
                    "蟹", "贝类", "海带", "紫菜", "鲈鱼", "鲫鱼", "草鱼", "鳕鱼", "三文鱼",
                    "排骨", "里脊肉", "五花肉", "牛腩", "牛排", "鸡翅", "鸡爪", "鸭肉", "鹅肉"],
        "exclude_patterns": []
    },
    "grains": {
        "keywords": ["大米", "面粉", "面条", "馒头", "面包", "燕麦", "小米", "黑米", "糯米",
                    "玉米", "玉米面", "红薯粉", "土豆粉", "荞麦", "荞麦面", "意面", "通心粉",
                    "红枣", "桂圆", "枸杞", "莲子", "芡实", "薏米", "红豆", "绿豆", "黑豆",
                    "黄豆", "花生", "核桃", "杏仁", "腰果"],
        "exclude_patterns": ["枣糕", "枣泥", "月饼"]
    },
    "dairy": {
        "keywords": ["牛奶", "酸奶", "奶酪", "黄油", "奶油", "芝士", "豆浆", "豆奶"],
        "exclude_patterns": ["牛奶巧克力", "奶糖", "奶油蛋糕", "奶油冰激凌"]
    },
    "seasonings": {
        "keywords": ["盐", "酱油", "生抽", "老抽", "醋", "料酒", "白糖", "红糖", "冰糖",
                    "花椒", "八角", "桂皮", "香叶", "胡椒", "辣椒", "豆瓣酱", "番茄酱",
                    "蚝油", "鸡精", "味精", "香油", "芝麻油", "花生油", "菜籽油", "橄榄油",
                    "芥末", "咖喱", "五香粉", "孜然"],
        "exclude_patterns": []
    },
    "snacks": {
        "keywords": ["薯片", "薯条", "饼干", "蛋糕", "面包", "巧克力", "糖果", "冰激凌",
                    "瓜子", "坚果", "果干", "蜜饯", "肉干", "鱼干", "海苔", "爆米花",
                    "薯条", "鸡米花", "鸡柳", "炸鸡", "汉堡", "披萨", "炸薯条"],
        "exclude_patterns": []
    }
}
