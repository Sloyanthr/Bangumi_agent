# main.py
import json
from openai import OpenAI
import config
import utils
import tools  # 导入所有的工具

# 初始化客户端
client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

def run_agent():
    print("✨ --- Bangumi Agent (模块化版) --- ✨")
    
    system_prompt = "你是一个二次元专家助手..."
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("\n>> 用户: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        messages.append({"role": "user", "content": user_input})
        
        # --- 第一轮 ---
        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                tools=tools.TOOLS_SCHEMA, # 直接从 tools 文件拿
                stream=False
            )
        except Exception as e:
            print(f"❌ 错误: {e}")
            continue

        msg = response.choices[0].message
        
        if msg.tool_calls:
            messages.append(msg)
            
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                # 使用 utils 里的解析器
                args = utils.parse_arguments(tool_call.function.arguments)
                
                print(f"🔍 [调试] 调用: {func_name} | 参数: {args}")

                # 🔥【超级优化】不再写一大堆 if/elif
                # 直接从字典里查函数并运行！
                if func_name in tools.AVAILABLE_FUNCTIONS:
                    function_to_run = tools.AVAILABLE_FUNCTIONS[func_name]
                    
                    # 这里要做个简单的参数解包适配
                    # 简单起见，我们根据函数名手动分配参数，或者统一你的函数参数风格
                    tool_result = "{}"
                    
                    if func_name == "search_anime":
                        tool_result = function_to_run(args.get("keyword") or args.get("name"))
                    elif func_name == "analyze_cv_data":
                        tool_result = function_to_run(int(args.get("subject_id") or args.get("id")))
                    elif func_name == "search_seiyu":
                        tool_result = function_to_run(args.get("name") or args.get("keyword"))
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                else:
                    print(f"⚠️ 找不到工具: {func_name}")

            # --- 第二轮 ---
            final_res = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages
            )
            print(f"\n🤖 Agent: {final_res.choices[0].message.content}")
            messages.append(final_res.choices[0].message)
        else:
            print(f"\n🤖 Agent: {msg.content}")
            messages.append(msg)

if __name__ == "__main__":
    run_agent()