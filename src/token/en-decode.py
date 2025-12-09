# JWT 签发与验证
from jose import jwt, exceptions
import time

#  payload：JWT 中包含的信息（自定义字段+标准字段）
payload = {
    "sub": "1234567890",  # 标准字段：主题（用户ID等）
    "name": "John Doe",   # 自定义字段
    "iat": time.time(),   # 标准字段：签发时间（Unix时间戳）
    "exp": time.time() + 5  # 标准字段：过期时间（1小时后）
}

# 密钥（对称加密，需妥善保管）
secret = "my-secret-key"

# 生成 JWT（算法指定为 HS256）
token = jwt.encode(payload, secret, algorithm="HS256")
print("生成的JWT:", token)
# time.sleep(6)

try:
    # 验证 JWT（指定算法和密钥）
    decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
    print("解码的payload:", decoded_payload)
except exceptions.ExpiredSignatureError as e:
    print("签名过期错误:", e)
