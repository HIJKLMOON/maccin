import json

# 原始的JSON数组数据（可以是字符串形式，也可以从文件读取）
original_json_str = '''
[
  {
    "user_id": "U5814",
    "user_name": "乐致",
    "product_id": "P92279",
    "product_name": "台灯",
    "product_category": "家居",
    "unit_price": 694.13,
    "purchase_time": "2024-09-27 15:52:35",
    "purchase_quantity": 4,
    "total_amount": 2776.52,
    "user_city": "苏州",
    "user_gender": "女",
    "user_age": 54
  },
  {
    "user_id": "U6495",
    "user_name": "柳刚克",
    "product_id": "P87143",
    "product_name": "桌游",
    "product_category": "玩具",
    "unit_price": 222.8,
    "purchase_time": "2024-06-16 06:46:19",
    "purchase_quantity": 3,
    "total_amount": 668.4,
    "user_city": "苏州",
    "user_gender": "女",
    "user_age": 25
  }
]
'''

def convert_json_array_to_jsonl(json_str, output_file="output.jsonl"):
    """
    将JSON数组转换为JSONL格式（每行一个JSON对象）
    :param json_str: 原始JSON数组字符串
    :param output_file: 输出的JSONL文件路径
    """
    try:
        # 1. 解析JSON数组字符串为Python列表
        data_list = json.loads(json_str)
        
        # 2. 打开输出文件，逐行写入每个JSON对象
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data_list:
                # 将单个对象序列化为JSON字符串，ensure_ascii=False保证中文正常显示
                json_line = json.dumps(item, ensure_ascii=False, separators=(',', ':'))
                f.write(json_line + '\n')  # 每行一个JSON对象，换行分隔
        
        print(f"转换完成！结果已保存到 {output_file}")
        return True
    
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}")
        return False
    except Exception as e:
        print(f"转换失败：{e}")
        return False

# 额外：如果你的数据是从文件读取的，可使用以下代码
with open("pdd.json", 'r', encoding='utf-8') as f:
    original_json_str = f.read()
convert_json_array_to_jsonl(original_json_str, "pdd1.json")