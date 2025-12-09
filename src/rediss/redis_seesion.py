import redis
import uuid
import json

WSL_REDIS_IP = "172.24.124.20"
# 连接Redis（密码为启动容器时设置的123456，本地地址localhost，端口6379）
rediss = redis.Redis(
    host=WSL_REDIS_IP,
    port=6379,
    decode_responses=True  # 自动将返回值转为字符串，避免字节流处理
)


def login(user_id, username):
    """用户登录，生成session并存储"""
    # 生成唯一session_id
    session_id = str(uuid.uuid4())
    # 构造用户信息
    user_info = {
        "user_id": user_id,
        "username": username,
        "role": "user"
    }
    # 存储到Redis，设置30分钟过期
    rediss.set(f"session:{session_id}", json.dumps(user_info), ex=1800)
    print(f"登录成功，session_id：{session_id}")
    return session_id


def check_login(session_id):
    """验证登录状态"""
    user_info = rediss.get(f"session:{session_id}")
    if user_info:
        return json.loads(user_info)
    else:
        return "登录状态已失效"


def del_session(session_id):
    """删除session"""
    rediss.delete(f"session:{session_id}")
    print(f"已删除session_id：{session_id}")


# 测试代码
if __name__ == "__main__":
    # 模拟用户登录
    # session_id = login(1001, "zhangsan")
    # 验证登录状态
    session_id = "7194ef00-1164-4053-b720-6a2381741079"
    print("登录信息：", check_login(session_id))
    del_session(session_id)
    # 查看剩余有效期
    print("剩余有效期（秒）：", rediss.ttl(f"session:{session_id}"))
