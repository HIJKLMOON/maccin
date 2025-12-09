import redis
from redis.exceptions import RedisError

# 初始化Redis连接池
WSL_REDIS_IP = "172.24.124.20"
pool = redis.ConnectionPool(
    host=WSL_REDIS_IP,
    port=6379,
    db=0,
    decode_responses=True
)
r = redis.Redis(connection_pool=pool)

# 秒杀Lua脚本
SECKILL_LUA = """
local goods_id = KEYS[1]
local user_id = ARGV[1]
local stock_key = 'seckill:stock:' .. goods_id
local users_key = 'seckill:users:' .. goods_id

-- 1. 检查库存
local stock = tonumber(redis.call('GET', stock_key))
if not stock or stock <= 0 then
    return 0  -- 库存不足
end

-- 2. 检查用户是否已下单
if redis.call('SISMEMBER', users_key, user_id) == 1 then
    return 2  -- 重复下单
end

-- 3. 扣减库存 + 记录用户
redis.call('DECR', stock_key)
redis.call('SADD', users_key, user_id)
return 1  -- 秒杀成功
"""


def init_seckill(goods_id: str, stock: int):
    """初始化秒杀商品库存"""
    r.set(f'seckill:stock:{goods_id}', stock)
    r.delete(f'seckill:users:{goods_id}')  # 清空历史下单用户


def seckill(goods_id: str, user_id: str) -> int:
    """执行秒杀"""
    try:
        # 执行Lua脚本
        result = r.eval(SECKILL_LUA, 1, goods_id, user_id)
        return result
    except RedisError as e:
        print(f"秒杀失败：{e}")
        return -1


# 测试
if __name__ == '__main__':
    goods_id = "iphone15"
    init_seckill(goods_id, 10)  # 初始化10个库存

    # 模拟多用户秒杀（可多线程测试）
    print(seckill(goods_id, "user_001"))  # 1（成功）
    print(seckill(goods_id, "user_001"))  # 2（重复）
    print(seckill(goods_id, "user_002"))  # 1（成功）
    print(r.get(f'seckill:stock:{goods_id}'))  # 8（库存剩余）
