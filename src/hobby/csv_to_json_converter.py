import pandas as pd
import json
import os
from datetime import datetime

def csv_to_json_with_english_columns(csv_file_path, json_file_path=None):
    """
    将CSV文件转换为JSON文件，并将中文列名替换为对应的英文列名
    
    Args:
        csv_file_path (str): 输入CSV文件路径
        json_file_path (str, optional): 输出JSON文件路径。如果为None，将在同一目录生成同名JSON文件
    
    Returns:
        dict: 转换后的数据字典（列表形式）
    """
    
    # 检查CSV文件是否存在
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV文件不存在: {csv_file_path}")
    
    # 设置默认的JSON输出路径
    if json_file_path is None:
        file_dir = os.path.dirname(csv_file_path)
        file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        json_file_path = os.path.join(file_dir, f"{file_name}.json")
    
    # 1. 读取CSV文件
    print(f"正在读取CSV文件: {csv_file_path}")
    try:
        # 尝试使用utf-8编码读取
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # 如果utf-8失败，尝试gbk编码
        df = pd.read_csv(csv_file_path, encoding='gbk')
    
    print(f"成功读取数据: {df.shape[0]} 行, {df.shape[1]} 列")
    
    # 2. 定义中文列名到英文列名的映射
    column_mapping = {
        '用户ID': 'user_id',
        '用户姓名': 'user_name',
        '商品ID': 'product_id',
        '商品名称': 'product_name',
        '商品类别': 'product_category',
        '单价': 'unit_price',
        '购买时间': 'purchase_time',
        '购买数量': 'purchase_quantity',
        '消费金额': 'total_amount',
        '用户城市': 'user_city',
        '用户性别': 'user_gender',
        '用户年龄': 'user_age'
    }
    
    # 3. 检查CSV文件的列名是否与映射匹配
    missing_columns = [col for col in df.columns if col not in column_mapping]
    if missing_columns:
        raise ValueError(f"CSV文件中存在未定义映射的列名: {', '.join(missing_columns)}")
    
    # 4. 重命名列名为英文
    df_english = df.rename(columns=column_mapping)
    print("已将中文列名转换为英文列名")
    
    # 5. 数据预处理（可选）
    # 转换购买时间为标准格式
    if 'purchase_time' in df_english.columns:
        df_english['purchase_time'] = pd.to_datetime(df_english['purchase_time'], errors='coerce')
        # 将datetime格式转换为字符串，便于JSON序列化
        df_english['purchase_time'] = df_english['purchase_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 处理可能的NaN值
    df_english = df_english.fillna({
        'user_name': 'Unknown',
        'product_name': 'Unknown',
        'product_category': 'Unknown',
        'user_city': 'Unknown',
        'user_gender': 'Unknown'
    })
    
    # 6. 转换为JSON格式
    print(f"正在将数据转换为JSON格式...")
    # 将DataFrame转换为字典列表
    data_dict = df_english.to_dict('records')
    
    # 7. 保存为JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)
    
    print(f"JSON文件已保存: {json_file_path}")
    print(f"转换完成！共处理 {len(data_dict)} 条记录")
    
    return data_dict

def main():
    """
    主函数 - 示例用法
    """
    # 配置文件路径
    # 请根据实际情况修改输入CSV文件路径
    input_csv_path = "src/hobby/ecommerce_data.csv"  # 输入CSV文件路径
    output_json_path = "ED.json"  # 输出JSON文件路径
    
    try:
        # 执行转换
        start_time = datetime.now()
        print(f"开始转换 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        converted_data = csv_to_json_with_english_columns(input_csv_path, output_json_path)
        
        # 显示转换结果摘要
        print("\n转换结果摘要:")
        print(f"- 总记录数: {len(converted_data)}")
        if converted_data:
            print(f"- 列名（英文）: {list(converted_data[0].keys())}")
            print(f"- 第一条记录示例:")
            for key, value in list(converted_data[0].items())[:5]:  # 只显示前5个字段
                print(f"  {key}: {value}")
        
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        print(f"\n转换完成 - 耗时: {elapsed_time:.2f} 秒")
        
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        print("请检查文件路径和格式后重试")

if __name__ == "__main__":
    main()
