# config.py
import urllib3
import os
from dotenv import load_dotenv
load_dotenv()

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API 配置
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"

# Bangumi 网络配置
NO_PROXY = {"http": None, "https": None}
HEADERS = {
    "User-Agent": "bgm_agent_pro/2.0 (contact: your_email@example.com)", 
    "Content-Type": "application/json"
}