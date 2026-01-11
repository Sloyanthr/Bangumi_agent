# tools/__init__.py

# 1. 从各个子模块导入你刚才定义的函数
# 注意：使用 . 表示当前目录
from .anime import (
    search_anime_by_keyword,
    get_anime_details,
    get_related_subjects,
    # ... 把你在 anime.py 里写的其他函数都导进来
)

from .people import (
    search_person_by_name,
    get_anime_staff_list,
    # ... 把你在 people.py 里写的其他函数都导进来
)

from .calendar import (
    get_today_schedule,
    # ... 把你在 calendar.py 里写的其他函数都导进来
)

# ==========================================
# 2. 核心映射表 (Function Map)
# main.py 会通过这个字典找到要执行的代码
# ==========================================
AVAILABLE_FUNCTIONS = {
    # 格式： "AI调用的工具名": 对应的Python函数
    
    # --- 动画类 ---
    "search_anime": search_anime_by_keyword,
    "get_anime_details": get_anime_details,
    "get_related_subjects": get_related_subjects,
    
    # --- 人物类 ---
    "search_seiyu": search_person_by_name,     # AI 叫 search_seiyu，实际执行 search_person_by_name
    "get_staff_info": get_anime_staff_list,
    
    # --- 时间类 ---
    "get_daily_calendar": get_today_schedule,
}

# ==========================================
# 3. 工具描述 (Schema)
# 这里是给 AI 看的“菜单”，告诉它每个工具怎么用
# ==========================================
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_anime",  # 必须和上面 AVAILABLE_FUNCTIONS 的 Key 保持一致！
            "description": "搜索动画，当用户不知道具体ID时使用",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "动画名称关键词"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_anime_details",
            "description": "根据ID获取动画的详细信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "integer",
                        "description": "动画ID"
                    }
                },
                "required": ["subject_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_daily_calendar",
            "description": "查询今天更新了哪些动画",
            "parameters": {
                "type": "object",
                "properties": {}, # 无参数工具
                "required": []
            }
        }
    },
    # ... 你需要按照这个格式，把剩下所有函数的描述都补全 ...
]