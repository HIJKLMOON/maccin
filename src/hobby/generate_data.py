import random
import datetime

# 1. 定义基础数据池（保证数据真实性）
# 商品品类列表
categories = [
    "电子产品", "服装鞋帽", "食品生鲜", "家居用品", "美妆护肤",
    "母婴用品", "图书音像", "运动户外", "家用电器", "数码配件",
    "酒水饮料", "宠物用品", "汽车用品", "办公用品", "箱包配饰"
]

# 省份列表（31个省级行政区）
provinces = [
    "北京市", "上海市", "广东省", "江苏省", "浙江省", "山东省", "四川省",
    "湖北省", "河南省", "湖南省", "河北省", "安徽省", "福建省", "陕西省",
    "辽宁省", "云南省", "黑龙江省", "江西省", "广西壮族自治区", "山西省",
    "贵州省", "重庆市", "吉林省", "甘肃省", "内蒙古自治区", "新疆维吾尔自治区",
    "海南省", "宁夏回族自治区", "青海省", "西藏自治区", "天津市"
]

# 2. 生成随机日期函数（范围：2023-01-01 至 2024-12-31）
def generate_random_date():
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)
    # 生成两个日期之间的随机天数差
    random_days = random.randint(0, (end_date - start_date).days)
    # 计算随机日期并转为YYYY-MM-DD格式
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

# 3. 生成1000行数据并写入文件
def generate_order_data():
    # 输出文件路径（Linux可改为/opt/hadoop/order_data.csv，Windows可改为D:\order_data.csv）
    output_file = "D:\\GameDocuments\\Documents\\CITODE\\maccin\\src\\hobby\\order_data.csv"
    
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入表头
        f.write("订单ID,商品品类,省份,销售额,下单时间\n")
        
        # 循环生成1000行数据
        for i in range(1, 1000):
            # 订单ID：ORDER2025 + 4位补零数字（如ORDER20250001）
            order_id = f"{i:03d}"
            # 随机选商品品类
            category = random.choice(categories)
            # 随机选省份
            province = random.choice(provinces)
            # 随机销售额（10.00 ~ 9999.99，保留2位小数）
            sales = int(round(random.uniform(10, 9999), 0))
            # 随机下单时间
            order_time = generate_random_date()
            
            # 拼接一行数据（注意CSV格式，字段无额外逗号）
            line = f"{order_id},{category},{province},{sales},{order_time}\n"
            f.write(line)
    
    print(f"✅ 1000行订单数据已生成，保存至：{output_file}")

# 4. 执行生成函数
if __name__ == "__main__":
    generate_order_data()