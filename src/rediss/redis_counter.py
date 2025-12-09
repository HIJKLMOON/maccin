import redis

WSL_REDIS_IP = "172.24.124.20"
# 连接Redis
r = redis.Redis(
    host=WSL_REDIS_IP,
    port=6379,
    # password="123456",
    decode_responses=True
)


def incr_read_count(article_id):
    """文章阅读量+1"""
    key = f"article:read_count:{article_id}"
    # 若key不存在，INCR会自动初始化为0再+1
    count = r.incr(key)
    print(f"文章{article_id}当前阅读量：{count}")
    return count


def get_read_count(article_id):
    """查询文章阅读量"""
    key = f"article:read_count:{article_id}"
    count = r.get(key)
    return int(count) if count else 0


def reset_read_count(article_id):
    """重置阅读量为0"""
    key = f"article:read_count:{article_id}"
    r.set(key, 0)
    print(f"文章{article_id}阅读量已重置为0")


# 测试代码
if __name__ == "__main__":
    # 模拟5次文章访问
    for _ in range(5):
        incr_read_count(101)
    # 查询阅读量
    print("最终阅读量：", get_read_count(101))
    # 重置阅读量
    reset_read_count(101)
