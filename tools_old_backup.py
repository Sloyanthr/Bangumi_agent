# tools.py
import json
import requests
import config  # 导入配置文件，确保里面有 HEADERS 和 NO_PROXY

# ==========================================
# 1. 具体工具函数的实现 (真实联网逻辑)
# ==========================================

def search_anime(keyword):
    """
    根据关键词搜索动画，返回前3个结果的 ID 和名字
    """
    print(f"🤖 [工具] 正在搜动画: {keyword}")
    
    # Bangumi 搜索 API (类型2代表动画)
    url = f"https://api.bgm.tv/search/subject/{keyword}"
    params = {
        "type": 2, 
        "responseGroup": "small", 
        "max_results": 3
    }
    
    try:
        # 使用 config 中的配置
        response = requests.get(
            url, 
            params=params, 
            headers=config.HEADERS, 
            proxies=config.NO_PROXY
        )
        response.raise_for_status()
        data = response.json()
        
        # 精简结果，只返回 AI 需要的信息
        results = []
        if "list" in data and data["list"]:
            for item in data["list"]:
                results.append({
                    "id": item["id"],
                    "name": item["name"],
                    "name_cn": item.get("name_cn", "无中文名"),
                    "score": item.get("rating", {}).get("score", "N/A")
                })
            return json.dumps(results, ensure_ascii=False)
        else:
            return json.dumps({"error": "未找到相关动画"}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"搜索出错: {str(e)}"}, ensure_ascii=False)


def analyze_cv(subject_id):
    """
    根据 Subject ID 查询角色和声优信息
    """
    print(f"🤖 [工具] 正在查声优，ID: {subject_id}")
    
    # Bangumi 角色 API
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}/characters"
    
    try:
        response = requests.get(
            url, 
            headers=config.HEADERS, 
            proxies=config.NO_PROXY
        )
        response.raise_for_status()
        data = response.json()
        
        # 提取前 8 个主要角色及其声优
        char_list = []
        for item in data[:8]: 
            char_name = item.get("name", "未知角色")
            actors = item.get("actors", [])
            
            actor_names = []
            if actors:
                for actor in actors:
                    actor_names.append(actor.get("name", ""))
            
            if actor_names:
                char_list.append(f"角色: {char_name} -> 声优: {', '.join(actor_names)}")
        
        if not char_list:
            return json.dumps({"result": "该动画暂无声优信息"}, ensure_ascii=False)
            
        return json.dumps(char_list, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"查询详情出错: {str(e)}"}, ensure_ascii=False)


def search_seiyu(name):
    """
    搜索声优/人物信息
    """
    print(f"🤖 [工具] 正在搜声优: {name}")
    
    # 搜索人物 API (类型1代表人物)
    url = f"https://api.bgm.tv/search/person/{name}"
    params = {"max_results": 3}
    
    try:
        response = requests.get(
            url, 
            params=params, 
            headers=config.HEADERS, 
            proxies=config.NO_PROXY
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        if "list" in data and data["list"]:
            for item in data["list"]:
                results.append({
                    "id": item["id"],
                    "name": item["name"],
                    "info": "声优/人物"
                })
            return json.dumps(results, ensure_ascii=False)
        else:
            return json.dumps({"error": "未找到该声优"}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"搜索声优出错: {str(e)}"}, ensure_ascii=False)


# ==========================================
# 2. 核心映射表 (Function Map)
# ==========================================
AVAILABLE_FUNCTIONS = {
    "search_anime": search_anime,
    "analyze_cv_data": analyze_cv,
    "search_seiyu": search_seiyu
}


# ==========================================
# 3. 工具描述 (Schema) - 给 AI 看的说明书
# ==========================================
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_anime",
            "description": "当用户提到动画名但不知道具体ID时使用。搜索动画获取ID。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "动画名称，例如：进击的巨人"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_cv_data",
            "description": "必须先有了动画的ID (Subject ID) 才能调用此工具。查询该动画的配音演员表。",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "integer",
                        "description": "动画的条目ID"
                    }
                },
                "required": ["subject_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_seiyu",
            "description": "当用户直接询问某位声优的信息时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "声优姓名，例如：花泽香菜"
                    }
                },
                "required": ["name"]
            }
        }
    }
]