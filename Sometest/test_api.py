import requests
import urllib3

# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
NO_PROXY = {"http": None, "https": None}
HEADERS = {
    "User-Agent": "StudentDemo/AnimeAgent/0.1 (my_email@test.com)",
    "Content-Type": "application/json"
}

def search_and_rank_final(keyword):
    print(f"🔍 正在搜索：{keyword} ...")
    url = "https://api.bgm.tv/v0/search/subjects"
    
    payload = {
        "keyword": keyword,
        "filter": {"type": [2]}, # 2=动画
        "sort": "match"
    }
    
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, proxies=NO_PROXY, verify=False)
        resp.raise_for_status()
        
        data = resp.json().get("data", [])
        
        if not data:
            print("❌ 未找到结果")
            return

        # --- 智能排序：按打分人数(热度)倒序 ---
        # 这样 3万人打分的正片 就会排在 100人打分的第二季 前面
        sorted_data = sorted(data, key=lambda x: x.get('rating', {}).get('total', 0), reverse=True)

        print(f"✅ 找到 {len(data)} 个结果，按热度排序Top 3：\n")

        for i, item in enumerate(sorted_data[:3]):
            name = item.get('name_cn') or item.get('name')
            sid = item.get('id')
            
            # --- 核心修复：更强壮的分数获取逻辑 ---
            # 1. 先试着直接拿 score
            score = item['rating'].get('score')
            # 2. 如果没有，去 rating 盒子里拿
            #if not score and 'rating' in item:
            #    score = item['rating'].get('score')
            # 3. 如果还是没有，显示暂无
            if not score:
                score = "暂无"
                
            count = item.get('rating', {}).get('total', 0)
            
            # 排版美化
            prefix = "🏆 [首选]" if i == 0 else f"   [备选 {i}]"
            print(f"{prefix} ID: {sid:<6} | 评分: {str(score):<4} | {count:>5}人打分 | {name}")

    except Exception as e:
        print(f"❌ 出错啦: {e}")

if __name__ == "__main__":
    search_and_rank_final("高达00")