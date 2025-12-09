import requests
from base64 import b64encode
from hashlib import sha1

# 生成 WebSocket 握手必需的 Sec-WebSocket-Key
key = b64encode(sha1(b"random-string").digest()).decode()
headers = {
    "Connection": "Upgrade",  # 必须是 Upgrade
    "Upgrade": "websocket",   # 必须是 websocket
    "Sec-WebSocket-Version": "13",  # 固定值 13
    "Sec-WebSocket-Key": key
}

# 发送握手请求（注意用 GET 方法）
response = requests.get("ws://localhost:8765", headers=headers)