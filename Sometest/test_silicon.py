from openai import OpenAI
import httpx

# 1. 配置客户端
# ⚠️ 请务必替换成你在硅基流动申请的真实 Key
API_KEY = "sk-wycrwqukgakttyjijpctburmhgzughymabuomhsniqadimno" 
BASE_URL = "https://api.siliconflow.cn/v1"

http_client = httpx.Client(trust_env=False)

client = OpenAI(
    api_key=API_KEY, 
    base_url=BASE_URL,
    http_client=http_client  # 关键在这里！
)


print("正在发送请求给 Qwen2.5 ...")

# 2. 发送对话请求
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct", # 模型名称
    messages=[
        # system: 给 AI 设定人设（你是谁）
        {'role': 'system', 'content': '你是一个鲁迅风格的文学家。'},
        # user: 用户的提问
        {'role': 'user', 'content': '今天天气真好，怎么夸？'}
    ],
stream=True # 【修改点1】改为 True，开启水龙头
)

# 3. 循环接收并打印结果
# 【修改点2】不再直接读取 content，而是用循环去接“水流”
for chunk in response:
    # 这一步是为了防止有时候返回空数据报错
    if chunk.choices[0].delta.content:
        # 获取这一个瞬间蹦出来的字
        content = chunk.choices[0].delta.content
        
        # end="" 表示不换行，连着打印
        # flush=True 表示强制立即显示，不要存缓存
        print(content, end="", flush=True)