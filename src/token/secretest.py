from dotenv import load_dotenv
import os

load_dotenv()  # 加载.env文件到环境变量
# 读取密钥（仅在内存中使用，用完不缓存）
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# 读取私钥文件（文件本身权限限制为仅当前用户可读）
with open(os.getenv("JWT_PRIVATE_KEY_PATH"), "r") as f:
    PRIVATE_KEY = f.read()

print(PRIVATE_KEY, SECRET_KEY)
