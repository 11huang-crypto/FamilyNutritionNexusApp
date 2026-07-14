# 🥬 AI 智能菜篮子 — 家庭营养管理系统

> FamilyNutritionNexus — 面向家庭场景的智能食材管理与营养分析 Web 应用

一个集 **AI 食材识别、营养分析、食材禁忌检测、家庭健康档案、食谱推荐、协同采购清单** 于一体的家庭营养管理平台。

---

## ✨ 核心功能

| 功能模块 | 说明 |
|---------|------|
| 📸 **拍照识材** | 上传食材照片，AI 自动识别食材种类并返回营养信息（基于百度 AI 识别 API + MobileNetV2） |
| 🥗 **营养分析** | 30+ 种常见食材的详细营养数据（热量、蛋白质、脂肪、碳水、纤维、维生素） |
| ⚠️ **食材禁忌检测** | 扫描菜篮子中的食材组合，自动检测相克/禁忌搭配并发出风险预警 |
| 👨‍👩‍👧‍👦 **家庭管理** | 创建家庭、邀请码加入、成员管理，支持多家庭切换 |
| 🏥 **健康档案** | 记录家庭成员的健康状况、过敏原、饮食禁忌，个性化推荐 |
| 📅 **食谱推荐** | 根据家庭成员健康档案生成一周食谱计划 |
| 📝 **协同采购清单** | 家庭成员实时协同编辑采购清单（WebSocket 同步） |
| 🔐 **用户认证** | JWT 令牌认证、注册/登录/忘记密码/重置密码全流程 |

---

## 🛠️ 技术栈

### 前端
- **Vue 3** + **Vite 5** — 响应式 SPA 框架与构建工具
- **Vant 4** — 移动端 UI 组件库
- **Pinia** — 状态管理
- **Vue Router 4** — 路由管理（含登录守卫）
- **Axios** — HTTP 请求
- **Sass** — 样式预处理

### 后端
- **FastAPI** — 高性能异步 Web 框架
- **SQLAlchemy 2.0** — ORM 数据库操作
- **SQLite** — 轻量级数据库（零配置开箱即用）
- **Pydantic 2** — 数据校验与序列化
- **python-jose** — JWT 令牌签发与验证
- **passlib** — 密码哈希加密

### AI 能力
- **百度 AI 开放平台** — 菜品识别、果蔬识别、通用物体识别
- **MobileNetV2** — 轻量级图像分类模型（PyTorch 迁移学习）

### 实时通信
- **WebSocket** — 采购清单多人协同编辑

---

## 📁 项目结构

```
FamilyNutritionNexus-2/
├── main.py                    # 主后端服务（FastAPI + SQLite + JWT）
├── requirements.txt           # Python 依赖
├── package.json               # 前端依赖
├── vite.config.js             # Vite 配置（含 API 代理）
├── index.html                 # 入口 HTML
│
├── src/                       # 前端源码
│   ├── api/                   # API 请求封装
│   ├── components/            # 公共组件（导航栏、食材卡片、状态组件等）
│   ├── views/                 # 页面视图（15 个页面）
│   │   ├── Login.vue          # 登录/注册
│   │   ├── HomeView.vue       # 首页
│   │   ├── Recognize.vue      # 拍照识材
│   │   ├── Nutrition.vue      # 营养分析
│   │   ├── FamilyHealth.vue   # 家庭健康档案
│   │   ├── MealPlan.vue       # 食谱推荐
│   │   ├── ShoppingList.vue   # 采购清单
│   │   ├── BasketView.vue     # 菜篮子
│   │   ├── Profile.vue        # 个人中心
│   │   └── ...
│   ├── router/                # 路由配置（含登录守卫）
│   ├── stores/                # Pinia 状态管理
│   ├── styles/                # 全局样式
│   ├── utils/                 # 工具函数
│   └── App.vue                # 根组件
│
├── backend_py/                # 辅助后端服务
│   ├── main.py                # WebSocket 实时协同服务
│   ├── meal_plan_service.py   # 食谱推荐逻辑
│   ├── shopping_list_service.py # 采购清单管理
│   └── mock_data.py           # 模拟数据
│
└── backend_vision/            # AI 视觉模型
    └── model/
        └── checkpoints/
            └── best_model.pth # MobileNetV2 训练权重（27.7MB）
```

---

## 🚀 快速开始

### 环境要求

- **Node.js** ≥ 18
- **Python** ≥ 3.10

### 1. 克隆仓库

```bash
git clone https://github.com/11huang-crypto/FamilyNutritionNexusApp.git
cd FamilyNutritionNexusApp
```

### 2. 启动前端

```bash
npm install
npm run dev
```

前端运行在 `http://localhost:5173`

### 3. 启动主后端

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload --port 3000
```

主后端运行在 `http://localhost:3000`

### 4. （可选）启动协同服务

```bash
cd backend_py
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### 5. （可选）配置环境变量

在项目根目录创建 `.env` 文件：

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./family-nutrition.db
BAIDU_API_KEY=your-baidu-api-key
BAIDU_SECRET_KEY=your-baidu-secret-key
```

> 未配置百度 AI Key 时，食材识别功能将使用 Mock 数据作为兜底。

---

## 📡 API 概览

主后端提供 28 个 RESTful API 端点：

| 模块 | 端点 | 方法 | 说明 |
|------|------|------|------|
| **认证** | `/auth/register` | POST | 用户注册 |
| | `/auth/login` | POST | 用户登录 |
| | `/auth/forgot-password` | POST | 忘记密码 |
| | `/auth/reset-password` | POST | 重置密码 |
| **家庭** | `/family/create` | POST | 创建家庭 |
| | `/family/my` | GET | 获取我的家庭 |
| | `/family/join` | POST | 邀请码加入家庭 |
| | `/family/{id}/members` | GET | 家庭成员列表 |
| **健康档案** | `/health/profile` | POST | 创建健康档案 |
| | `/health/family/{id}` | GET | 家庭健康档案 |
| | `/health/profile/{id}` | PUT/DELETE | 更新/删除档案 |
| **菜篮子** | `/basket/item` | POST | 添加食材 |
| | `/basket/family/{id}` | GET | 获取菜篮子 |
| | `/basket/item/{id}` | PUT/DELETE | 更新/删除食材 |
| | `/basket/check` | GET | 扫描食材禁忌 |
| **AI 识别** | `/analyze` | POST | 上传图片识别食材 |
| **食谱** | `/recipes/search` | GET | 搜索食谱 |
| | `/meal-plan/generate` | POST | 生成一周食谱 |
| **采购清单** | `/shopping-list/realtime` | GET | 获取实时清单 |
| | `/shopping-list/item` | POST | 添加采购项 |

---

## 🧩 系统架构

```
┌─────────────────────────────────────────────┐
│              前端 (Vue 3 + Vant)              │
│         http://localhost:5173                │
└──────────────────┬──────────────────────────┘
                   │ Axios / WebSocket
                   ▼
┌─────────────────────────────────────────────┐
│        Vite Dev Server (代理转发)             │
│         http://localhost:5173 → :3000        │
└──────────┬──────────────────┬───────────────┘
           │                  │
           ▼                  ▼
┌──────────────────┐  ┌───────────────────────┐
│   主后端 :3000    │  │  协同服务 :8002        │
│  FastAPI + JWT   │  │  FastAPI + WebSocket  │
│  SQLite 数据库    │  │  食谱推荐 + 采购清单   │
└────────┬─────────┘  └───────────────────────┘
         │
         ▼
┌──────────────────┐
│   百度 AI API     │
│  菜品/果蔬/物体识别 │
└──────────────────┘
```

---

## 👥 团队成员

本项目由 5 人团队协作开发。

---

## 📄 License

本项目为课程实践项目，仅供学习交流使用。
