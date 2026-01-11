# 基础搜索
import json
import requests
import config

def search_anime_by_keyword(keyword: str):
    print(f"搜索动画，关键词: {keyword}")
    url = f"https://api.bgm.tv/search/subject/{keyword}"
    """根据关键词搜动画，返回列表 (ID, 中文名, 原名, 评分)"""
    try:
        response = requests.get(
            url,
            params={
                "type": 2,  # 类型2代表动画
                "responseGroup": "small",
                "max_results": 5
            },
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
                    "name_cn": item.get("name_cn", "无中文名"),
                    "score": item.get("rating", {}).get("score", "N/A")
                })
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"搜索出错: {str(e)}"}, ensure_ascii=False)


# 详情查询
def get_anime_details(subject_id: int):
    """根据ID获取动画详细信息 (简介, 发行日期, 总集数, 官方网站)"""
    pass

# 评分与吐槽
def get_anime_reviews(subject_id: int):
    """获取动画的最新短评或高分长评 (用于分析舆论)"""
    pass

# 剧集信息 (进阶)
def get_episode_list(subject_id: int):
    """获取该动画的剧集列表 (例如: 第1话标题, 第2话标题...)"""
    pass

# 关联推荐
def get_related_subjects(subject_id: int):
    """获取关联作品 (续作, 前传, 番外, 相同世界观)"""
    pass

# 标签系统 (用于推荐)
def get_anime_tags(subject_id: int):
    """获取该动画的标签 (例如: '科幻', '百合', '机战')"""
    pass