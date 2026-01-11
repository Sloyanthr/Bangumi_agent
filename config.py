# config.py
import urllib3
import os
from dotenv import load_dotenv

# 1. 加载 .env 文件
load_dotenv()

# =====================================================
# 🔥 核心修复：强制清除系统代理设置
# 这能防止 OpenAI 库自动使用你的 VPN/加速器，
# 从而解决连接 SiliconFlow (国内服务器) 时的 Connection error
# =====================================================
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# 2. 禁用 SSL 警告 (如果你之后要抓包调试的话有用，平时没影响)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 3. API 配置
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"

# 4. Bangumi 网络配置
# (由于上面已经清空了环境变量，这里的 proxies 其实可以传空字典，
# 但为了保险起见，保持原样给 requests 库显式指定也不错)
NO_PROXY = {"http": None, "https": None}

HEADERS = {
    "User-Agent": "Sloya/my-private-project (contact: tianheng2171@163.com)", 
    "Content-Type": "application/json"
}