# 非对称加密生成 JWT
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwt, exceptions
import time

# 生成私钥
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode("utf-8")

# 从私钥导出公钥
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode("utf-8")

payload = {
    "sub": "123456",
    "name": "Tom",
    "iat": time.time(),
    "exp": time.time() + 5
}

token = jwt.encode(payload, private_pem, algorithm="RS256")
print("生成的JWT:", token)

try:
    payload = jwt.decode(token, public_pem, algorithms=["RS256"])
    print("解析结果:", payload)
except Exception as e:
    print("解析失败:", e)
