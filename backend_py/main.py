"""
Family Nutrition Nexus - 食谱推荐与协同功能后端服务
基于 FastAPI 框架，支持 WebSocket 实时协同编辑
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from datetime import datetime

# 导入服务
from meal_plan_service import MealPlanService
from shopping_list_service import ShoppingListService

# 初始化 FastAPI 应用
app = FastAPI(
    title="Family Nutrition Nexus API",
    description="家庭营养管理系统的食谱推荐与协同功能",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
meal_plan_service = MealPlanService()
shopping_list_service = ShoppingListService()


def json_serial(obj):
    """
    JSON 序列化辅助函数
    处理 datetime 等非标准 JSON 类型
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_shopping_list(shopping_list):
    """
    序列化购物清单，确保所有数据都是 JSON 可序列化的
    
    Args:
        shopping_list: 购物清单对象
        
    Returns:
        dict: 序列化的购物清单
    """
    return {
        "id": shopping_list["id"],
        "family_id": shopping_list["family_id"],
        "items": [
            {
                **item,
                "added_at": item["added_at"].isoformat() if isinstance(item.get("added_at"), datetime) else item.get("added_at", ""),
                "updated_at": item["updated_at"].isoformat() if isinstance(item.get("updated_at"), datetime) else item.get("updated_at", "")
            }
            for item in shopping_list["items"]
        ],
        "last_updated": shopping_list["last_updated"].isoformat() if isinstance(shopping_list.get("last_updated"), datetime) else shopping_list.get("last_updated", "")
    }


@app.get("/")
async def root():
    """API 根路径"""
    return {
        "message": "Family Nutrition Nexus API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "Family Nutrition Nexus API is running"
    }


@app.get("/shopping-list/realtime")
async def realtime_info():
    """
    WebSocket 实时同步接口说明
    返回 WebSocket 连接信息和使用说明
    """
    return {
        "websocket_url": "/ws",
        "description": "WebSocket endpoint for real-time shopping list synchronization",
        "operations": {
            "join-family": "Join a family group to subscribe to shopping list updates",
            "leave-family": "Leave the family group",
            "add-item": "Add a new item to the shopping list",
            "update-item": "Update an existing item",
            "toggle-item": "Toggle item purchased status",
            "remove-item": "Remove an item from the list",
            "clear-purchased": "Clear all purchased items",
            "get-shopping-list": "Get current shopping list"
        }
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 实时通信端点
    
    支持的操作:
    - join-family: 加入家庭组，订阅采购清单更新
    - leave-family: 离开家庭组，取消订阅
    - add-item: 添加采购项
    - update-item: 更新采购项
    - toggle-item: 切换已购/未购状态
    - remove-item: 删除采购项
    - clear-purchased: 清除已购商品
    - get-shopping-list: 获取当前采购清单
    """
    await websocket.accept()
    client_info = {"family_id": None, "user_id": None}
    
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action = message.get("action")
            
            # 处理加入家庭组
            if action == "join-family":
                family_id = message.get("family_id", "family-1")
                user_id = message.get("user_id", f"user-{id(websocket)}")
                client_info["family_id"] = family_id
                client_info["user_id"] = user_id
                
                # 获取当前购物清单
                shopping_list = shopping_list_service.get_shopping_list(family_id)
                
                await websocket.send_json({
                    "type": "success",
                    "action": "join-family",
                    "message": f"Joined family {family_id}",
                    "shopping_list": serialize_shopping_list(shopping_list)
                })
            
            # 处理离开家庭组
            elif action == "leave-family":
                family_id = client_info.get("family_id")
                if family_id:
                    await websocket.send_json({
                        "type": "success",
                        "action": "leave-family",
                        "message": f"Left family {family_id}"
                    })
                client_info["family_id"] = None
                client_info["user_id"] = None
            
            # 处理添加采购项
            elif action == "add-item":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                item = message.get("item", {})
                
                new_item = shopping_list_service.add_item(
                    family_id=family_id,
                    name=item.get("name", ""),
                    quantity=item.get("quantity", 1),
                    unit=item.get("unit", "个"),
                    category=item.get("category", "other")
                )
                
                # 获取更新后的购物清单
                shopping_list = shopping_list_service.get_shopping_list(family_id)
                
                await websocket.send_json({
                    "type": "success",
                    "action": "add-item",
                    "message": "Item added successfully",
                    "item": new_item,
                    "shopping_list": serialize_shopping_list(shopping_list)
                })
            
            # 处理更新采购项
            elif action == "update-item":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                item_id = message.get("item_id")
                updates = message.get("updates", {})
                
                updated_item = shopping_list_service.update_item(
                    family_id=family_id,
                    item_id=item_id,
                    **updates
                )
                
                if updated_item:
                    shopping_list = shopping_list_service.get_shopping_list(family_id)
                    await websocket.send_json({
                        "type": "success",
                        "action": "update-item",
                        "message": "Item updated successfully",
                        "item": updated_item,
                        "shopping_list": serialize_shopping_list(shopping_list)
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "action": "update-item",
                        "message": "Item not found"
                    })
            
            # 处理切换采购项状态
            elif action == "toggle-item":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                item_id = message.get("item_id")
                
                updated_item = shopping_list_service.toggle_item_status(family_id, item_id)
                
                if updated_item:
                    shopping_list = shopping_list_service.get_shopping_list(family_id)
                    await websocket.send_json({
                        "type": "success",
                        "action": "toggle-item",
                        "message": "Item status toggled",
                        "item": updated_item,
                        "shopping_list": serialize_shopping_list(shopping_list)
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "action": "toggle-item",
                        "message": "Item not found"
                    })
            
            # 处理删除采购项
            elif action == "remove-item":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                item_id = message.get("item_id")
                
                success = shopping_list_service.remove_item(family_id, item_id)
                
                if success:
                    shopping_list = shopping_list_service.get_shopping_list(family_id)
                    await websocket.send_json({
                        "type": "success",
                        "action": "remove-item",
                        "message": "Item removed successfully",
                        "shopping_list": serialize_shopping_list(shopping_list)
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "action": "remove-item",
                        "message": "Item not found"
                    })
            
            # 处理清除已购商品
            elif action == "clear-purchased":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                
                cleared_count = shopping_list_service.clear_purchased_items(family_id)
                shopping_list = shopping_list_service.get_shopping_list(family_id)
                
                await websocket.send_json({
                    "type": "success",
                    "action": "clear-purchased",
                    "message": f"Cleared {cleared_count} purchased items",
                    "cleared_count": cleared_count,
                    "shopping_list": serialize_shopping_list(shopping_list)
                })
            
            # 处理获取购物清单
            elif action == "get-shopping-list":
                family_id = client_info.get("family_id") or message.get("family_id", "family-1")
                
                shopping_list = shopping_list_service.get_shopping_list(family_id)
                await websocket.send_json({
                    "type": "success",
                    "action": "get-shopping-list",
                    "shopping_list": serialize_shopping_list(shopping_list)
                })
            
            # 未知操作
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown action: {action}"
                })
    
    except WebSocketDisconnect:
        print(f"Client {client_info.get('user_id')} disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass


async def broadcast_update(family_id: str, action: str, data: dict):
    """
    广播更新到所有订阅该家庭的客户端
    
    Args:
        family_id: 家庭 ID
        action: 操作类型
        data: 更新的数据
    """
    # 广播逻辑（当前实现为单客户端，可扩展为多客户端）
    pass


if __name__ == "__main__":
    # 启动服务
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )
