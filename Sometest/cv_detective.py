import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
NO_PROXY = {"http": None, "https": None}
HEADERS = {
    "User-Agent": "StudentDemo/CV_Miner/1.0 (tianheng2171@163.com)", # 记得改名
    "Content-Type": "application/json"
}

# --- 1. 搜索动画 ID (直接复用你之前的逻辑) ---
def get_anime_id(keyword):
    print(f"🔍 1. 正在搜索动画: {keyword}...")
    url = "https://api.bgm.tv/v0/search/subjects"
    payload = {"keyword": keyword, "filter": {"type": [2]}, "sort": "match"}
    
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, proxies=NO_PROXY, verify=False)
        data = resp.json().get("data", [])
        if not data: return None, None
        
        # 排序取最热
        sorted_data = sorted(data, key=lambda x: x.get('rating', {}).get('total', 0), reverse=True)
        best = sorted_data[0]
        return best['id'], (best['name_cn'] or best['name'])
    except Exception as e:
        print(e)
        return None, None

# --- 2. 获取主角的声优 ID (需要你来填空) ---
def get_main_cv(subject_id):
    print(f"🕵️ 2. 正在查询动画 (ID:{subject_id}) 的主角声优...")
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}/characters"
    
    try:
        resp = requests.get(url, headers=HEADERS, proxies=NO_PROXY, verify=False)
        char_list = resp.json() # 这是一个列表
        
        # TODO: 请写一个循环，遍历 char_list
        # 1. 检查 item['relation'] 是否等于 "主角"
        # 2. 如果是，检查 item['actors'] 是否不为空
        # 3. 如果有 actors，提取第一个 actor 的 'id' 和 'name'
        # 4. 返回 (actor_id, actor_name, character_name)
        for char in char_list:
            #输出测试
            #print(char)
            if char.get('relation') == '主角':
                actors = char.get('actors',[])
                if actors:
                    #输出测试
                    '''
                    for atr in actors:
                        print(atr)
                    '''
                    actor=actors[0]
                    return actor['id'],actor['name'],char['name']

        
        return None, None, None
    except Exception as e:
        print(f"❌ 查角色出错: {e}")
        return None, None, None

# --- 3. 获取声优的其他作品 (需要你来填空) ---
def get_cv_works(person_id, person_name):
    print(f"🎤 3. 正在挖掘声优【{person_name}】的其他角色...")
    url = f"https://api.bgm.tv/v0/persons/{person_id}/characters"
    
    try:
        resp = requests.get(url, headers=HEADERS, proxies=NO_PROXY, verify=False)
        works_list = resp.json() # 列表
        
        print(f"\n✨ 声优 {person_name} 还配过这些角色：")
        print("-" * 30)
        # TODO: 请遍历 works_list 的前 5 个结果 (works_list[:5])
        # 打印格式例如： 角色名(xxxx) ---出自---> 动画名(xxxx)
        # 提示：角色名在 item['name']，动画名在 item['subject_name']
        
        # --- 你的代码写在这里 ---
        for char in works_list[:5]:
            print(char.get('name')+' 出自 '+char.get('subject_name_cn')+'('+char.get('subject_name')+')')
        # -----------------------
        
    except Exception as e:
        print(f"❌ 查声优作品出错: {e}")

# --- 主程序 ---
def main():
    keyword = "芙莉莲"
    print('动画名'+keyword)
    # 第一步：找动画
    sid, sname = get_anime_id(keyword)
    if not sid:
        print("未找到动画")
        return

    print(f"✅ 锁定动画：{sname} (ID: {sid})")
    
    # 第二步：找声优
    cv_id, cv_name, char_name = get_main_cv(sid)
    if not cv_id:
        print("❌ 未找到主角声优信息")
        return
        
    print(f"✅ 锁定主角：{char_name}，声优是：{cv_name} (ID: {cv_id})")
    
    # 第三步：找其他作品
    get_cv_works(cv_id, cv_name)

if __name__ == "__main__":
    main()