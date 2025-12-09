import asyncio
import logging
from websockets import serve, exceptions
from websockets.datastructures import Headers

# 配置日志（方便调试）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 维护所有活跃的 WebSocket 连接（用于广播消息）
active_connections = set()

async def validate_websocket_request(path: str, request_headers: Headers) -> tuple | None:
    """
    自定义请求校验：过滤非 WebSocket 握手请求，避免 InvalidUpgrade 错误
    返回 None 表示校验通过，返回 (状态码, 响应头, 响应体) 表示拒绝请求
    """
    # 统一转小写避免大小写问题
    connection_header = request_headers.get("connection", "").lower()
    upgrade_header = request_headers.get("upgrade", "").lower()

    # 校验 Connection 和 Upgrade 头
    if "upgrade" not in connection_header:
        logger.warning(f"无效请求：Connection 头不是 Upgrade，实际值：{connection_header}")
        return (400, [], b"Error: Connection header must be 'Upgrade'")
    if upgrade_header != "websocket":
        logger.warning(f"无效请求：Upgrade 头不是 websocket，实际值：{upgrade_header}")
        return (400, [], b"Error: Upgrade header must be 'websocket'")
    
    # 校验 WebSocket 版本（必须是 13）
    ws_version = request_headers.get("sec-websocket-version", "")
    if ws_version != "13":
        logger.warning(f"无效请求：WebSocket 版本不是 13，实际值：{ws_version}")
        return (400, [], b"Error: Sec-WebSocket-Version must be 13")
    
    logger.info(f"WebSocket 握手校验通过，路径：{path}")
    return None

async def handle_client_connection(websocket):
    """处理单个客户端的连接、消息收发、断开"""
    # 将新连接加入活跃列表
    active_connections.add(websocket)
    client_address = websocket.remote_address
    logger.info(f"客户端已连接：{client_address}，当前在线数：{len(active_connections)}")

    try:
        # 持续接收客户端消息
        async for message in websocket:
            logger.info(f"收到客户端 {client_address} 消息：{message}")
            # 广播消息给所有在线客户端
            broadcast_msg = f"[{client_address[0]}:{client_address[1]}] {message}"
            await broadcast_message(broadcast_msg, exclude_self=False)

    except exceptions.ConnectionClosedError:
        logger.info(f"客户端 {client_address} 主动断开连接")
    except Exception as e:
        logger.error(f"客户端 {client_address} 连接异常：{str(e)}", exc_info=True)
    finally:
        # 连接断开后移除活跃列表
        active_connections.discard(websocket)
        logger.info(f"客户端 {client_address} 已断开，当前在线数：{len(active_connections)}")

async def broadcast_message(message: str, exclude_self: bool = False):
    """广播消息给所有活跃客户端"""
    if not active_connections:
        logger.warning("无在线客户端，跳过广播")
        return
    
    # 复制连接列表避免迭代时修改
    connections = list(active_connections)
    for conn in connections:
        if exclude_self and conn == asyncio.current_task().get_extra_info("websocket"):
            continue
        try:
            await conn.send(message)
        except Exception as e:
            logger.error(f"广播消息给 {conn.remote_address} 失败：{str(e)}")

async def main():
    """启动 WebSocket 服务"""
    server = await serve(
        handle_client_connection,
        host="0.0.0.0",       # 监听所有网卡
        port=8765,            # 服务端口
        process_request=validate_websocket_request  # 绑定请求校验函数
    )
    logger.info(f"WebSocket 服务已启动：ws://0.0.0.0:8765")
    
    # 保持服务运行（直到手动终止）
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务被手动终止")
    except Exception as e:
        logger.error("服务启动失败：{str(e)}", exc_info=True)