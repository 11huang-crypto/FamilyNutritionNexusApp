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
        "suitable_for": ["减脂", "高蛋白"],
        "steps": [
            "鲈鱼去鳞去内脏，洗净擦干，在鱼身上划几刀",
            "葱切段，姜切片，均匀铺在鱼身上",
            "淋上料酒腌制15分钟",
            "蒸锅中水烧开后，将鱼放入蒸8-10分钟",
            "取出蒸好的鱼，倒掉盘中的汤汁",
            "重新铺上葱丝姜丝，淋上热香油和生抽即可"
        ]
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
        "suitable_for": ["减脂", "高蛋白", "低碳水"],
        "steps": [
            "西兰花切小朵，虾仁去虾线洗净",
            "锅中水烧开，放入西兰花焯水1分钟捞出备用",
            "热锅凉油，放入蒜末爆香",
            "加入虾仁翻炒至变色",
            "放入西兰花继续翻炒2分钟",
            "加盐调味，翻炒均匀即可出锅"
        ]
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
        "suitable_for": ["快手菜", "家常"],
        "steps": [
            "西红柿洗净切块，鸡蛋打散备用",
            "热锅凉油，倒入鸡蛋液炒至凝固盛出",
            "锅中再加少许油，放入西红柿翻炒出汁",
            "加入炒好的鸡蛋，加盐调味",
            "翻炒均匀即可出锅，撒上葱花装饰"
        ]
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
        "suitable_for": ["快手早餐", "高纤维"],
        "steps": [
            "燕麦片放入杯中",
            "倒入牛奶浸泡5分钟",
            "香蕉切片铺在上面",
            "撒上蓝莓即可食用"
        ]
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
        "suitable_for": ["养生", "易消化"],
        "steps": [
            "所有杂粮淘洗干净",
            "放入电饭煲，加入约8倍体积的水",
            "选择煮粥模式，煮40分钟",
            "煮好后焖10分钟即可食用"
        ]
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
        "suitable_for": ["快手菜", "高蛋白"],
        "steps": [
            "鸡蛋打入碗中，加少许盐打散",
            "平底锅烧热，倒入花生油",
            "倒入蛋液，小火煎至两面金黄",
            "出锅装盘即可"
        ]
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
        "suitable_for": ["减脂", "高蛋白", "低碳水"],
        "steps": [
            "鸡胸肉洗净，用料酒腌制10分钟",
            "葱切段，姜切片铺在盘子底部",
            "将鸡胸肉放在葱姜上面",
            "蒸锅中水烧开后，放入蒸15分钟",
            "取出后淋上生抽即可"
        ]
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
        "suitable_for": ["家常", "开胃"],
        "steps": [
            "番茄洗净切块，鸡蛋打散备用",
            "热锅凉油，倒入鸡蛋液炒至凝固盛出",
            "锅中再加少许油，放入番茄翻炒出汁",
            "加少许白糖提鲜，加入炒好的鸡蛋",
            "加盐调味，翻炒均匀即可出锅"
        ]
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
        "suitable_for": ["清淡", "养生"],
        "steps": [
            "豆腐切块，鸡蛋打散备用",
            "锅中加水烧开，放入豆腐块煮5分钟",
            "将蛋液缓缓倒入锅中，搅拌均匀",
            "加盐调味，撒上葱花",
            "滴入香油即可出锅"
        ]
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
        "suitable_for": ["减脂", "高铁"],
        "steps": [
            "菠菜洗净，锅中水烧开后放入焯1分钟",
            "捞出菠菜沥干水分，切成段",
            "热锅凉油，放入蒜末爆香",
            "放入菠菜翻炒1分钟",
            "加盐调味，翻炒均匀即可出锅"
        ]
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
        "suitable_for": ["养生", "补血"],
        "steps": [
            "黑米淘洗干净，提前浸泡4小时",
            "红枣洗净去核",
            "锅中加水烧开，放入黑米煮30分钟",
            "加入红枣继续煮20分钟",
            "煮至粥变得粘稠即可"
        ]
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
        "suitable_for": ["减脂", "快手"],
        "steps": [
            "锅中水烧开，放入荞麦面煮8-10分钟",
            "捞出面条过凉水，沥干水分",
            "黄瓜切丝备用",
            "碗中加入醋、生抽、香油调制成酱汁",
            "将酱汁淋在面条上，放上黄瓜丝，拌匀即可"
        ]
    },
    "recipe-13": {
        "id": "recipe-13",
        "name": "芒果糯米饭",
        "meal_type": ["breakfast", "dessert"],
        "nutrition": {
            "calories": 320,
            "protein": 4.0,
            "carbs": 60.0,
            "fat": 8.0
        },
        "ingredients": [
            {"name": "芒果", "quantity": 1, "unit": "个", "category": "fruits"},
            {"name": "糯米", "quantity": 100, "unit": "克", "category": "grains"},
            {"name": "椰汁", "quantity": 100, "unit": "毫升", "category": "dairy"},
            {"name": "白糖", "quantity": 2, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 30,
        "difficulty": "medium",
        "suitable_for": ["甜品", "早餐"],
        "steps": [
            "糯米淘洗干净，提前浸泡2小时",
            "将糯米放入蒸锅蒸20-25分钟至熟",
            "椰汁加糖搅拌至融化，淋在糯米饭上",
            "芒果去皮切块，放在糯米饭上即可"
        ]
    },
    "recipe-14": {
        "id": "recipe-14",
        "name": "芒果酸奶杯",
        "meal_type": ["breakfast", "dessert"],
        "nutrition": {
            "calories": 250,
            "protein": 8.0,
            "carbs": 35.0,
            "fat": 8.0
        },
        "ingredients": [
            {"name": "芒果", "quantity": 1, "unit": "个", "category": "fruits"},
            {"name": "酸奶", "quantity": 200, "unit": "克", "category": "dairy"},
            {"name": "燕麦", "quantity": 30, "unit": "克", "category": "grains"}
        ],
        "cooking_time": 5,
        "difficulty": "easy",
        "suitable_for": ["减脂", "早餐"],
        "steps": [
            "芒果去皮切块，一半打成芒果泥",
            "杯中先铺一层燕麦",
            "倒入一层酸奶，再铺一层芒果块",
            "重复几次，最后淋上芒果泥即可"
        ]
    },
    "recipe-15": {
        "id": "recipe-15",
        "name": "土豆炖牛肉",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 350,
            "protein": 25.0,
            "carbs": 25.0,
            "fat": 18.0
        },
        "ingredients": [
            {"name": "土豆", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "牛肉", "quantity": 200, "unit": "克", "category": "proteins"},
            {"name": "胡萝卜", "quantity": 100, "unit": "克", "category": "vegetables"},
            {"name": "葱", "quantity": 2, "unit": "根", "category": "vegetables"},
            {"name": "姜", "quantity": 3, "unit": "片", "category": "vegetables"},
            {"name": "料酒", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "生抽", "quantity": 2, "unit": "勺", "category": "seasonings"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"}
        ],
        "cooking_time": 60,
        "difficulty": "medium",
        "suitable_for": ["滋补", "家常"],
        "steps": [
            "牛肉切块，冷水下锅焯水去血沫",
            "土豆、胡萝卜切块备用",
            "热锅凉油，放入葱姜爆香",
            "加入牛肉翻炒，加料酒、生抽调味",
            "加入开水没过牛肉，小火炖40分钟",
            "加入土豆、胡萝卜继续炖20分钟",
            "加盐调味，大火收汁即可"
        ]
    },
    "recipe-16": {
        "id": "recipe-16",
        "name": "莲藕排骨汤",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 280,
            "protein": 20.0,
            "carbs": 15.0,
            "fat": 15.0
        },
        "ingredients": [
            {"name": "莲藕", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "排骨", "quantity": 200, "unit": "克", "category": "proteins"},
            {"name": "姜", "quantity": 3, "unit": "片", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"}
        ],
        "cooking_time": 60,
        "difficulty": "medium",
        "suitable_for": ["养生", "清淡"],
        "steps": [
            "排骨冷水下锅焯水去血沫",
            "莲藕洗净切块，姜切片备用",
            "锅中加水烧开，放入排骨和姜片",
            "小火慢炖30分钟",
            "加入莲藕继续炖20分钟",
            "加盐调味即可"
        ]
    },
    "recipe-17": {
        "id": "recipe-17",
        "name": "青椒土豆丝",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 180,
            "protein": 4.0,
            "carbs": 25.0,
            "fat": 8.0
        },
        "ingredients": [
            {"name": "土豆", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "青椒", "quantity": 1, "unit": "个", "category": "vegetables"},
            {"name": "蒜", "quantity": 2, "unit": "瓣", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "醋", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 15,
        "difficulty": "easy",
        "suitable_for": ["家常", "下饭"],
        "steps": [
            "土豆去皮切丝，泡水去除淀粉",
            "青椒切丝，蒜切末备用",
            "热锅凉油，放入蒜末爆香",
            "加入土豆丝翻炒2分钟",
            "加入青椒丝继续翻炒1分钟",
            "加盐和醋调味，翻炒均匀即可出锅"
        ]
    },
    "recipe-18": {
        "id": "recipe-18",
        "name": "清炒莲藕",
        "meal_type": ["lunch", "dinner"],
        "nutrition": {
            "calories": 100,
            "protein": 3.0,
            "carbs": 18.0,
            "fat": 3.0
        },
        "ingredients": [
            {"name": "莲藕", "quantity": 300, "unit": "克", "category": "vegetables"},
            {"name": "蒜", "quantity": 2, "unit": "瓣", "category": "vegetables"},
            {"name": "盐", "quantity": 2, "unit": "小勺", "category": "seasonings"},
            {"name": "白醋", "quantity": 1, "unit": "勺", "category": "seasonings"}
        ],
        "cooking_time": 10,
        "difficulty": "easy",
        "suitable_for": ["清淡", "家常"],
        "steps": [
            "莲藕洗净切片，放入清水中加白醋浸泡防止变黑",
            "蒜切末备用",
            "热锅凉油，放入蒜末爆香",
            "加入莲藕片翻炒2分钟",
            "加盐调味，翻炒均匀即可出锅"
        ]
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
