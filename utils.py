# utils.py
import json

def parse_arguments(arguments_str):
    """强力解析器：处理 JSON 字符串及双重转义"""
    try:
        if isinstance(arguments_str, dict):
            return arguments_str
        parsed = json.loads(arguments_str)
        if isinstance(parsed, str):
            try:
                parsed_again = json.loads(parsed)
                if isinstance(parsed_again, dict):
                    return parsed_again
            except json.JSONDecodeError:
                pass
        return parsed
    except Exception:
        return None