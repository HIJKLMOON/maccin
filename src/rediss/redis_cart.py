import redis

WSL_REDIS_IP = "172.24.124.20"
# 连接Redis
r = redis.Redis(
    host=WSL_REDIS_IP,
    port=6379,
    # password="123456",
    decode_responses=True
)


def add_to_cart(user_id, product_id, quantity):
    """添加商品到购物车"""
    key = f"cart:{user_id}"
    # HSET会覆盖已存在的field，实现修改功能
    r.hset(key, product_id, quantity)
    print(f"商品{product_id}已添加到用户{user_id}的购物车，数量：{quantity}")


def update_cart(user_id, product_id, quantity):
    """修改购物车商品数量"""
    add_to_cart(user_id, product_id, quantity)  # 复用HSET的覆盖逻辑


def delete_from_cart(user_id, product_id):
    """删除购物车中的商品"""
    key = f"cart:{user_id}"
    r.hdel(key, product_id)
    print(f"商品{product_id}已从用户{user_id}的购物车中删除")


def get_cart(user_id):
    """查询用户购物车"""
    key = f"cart:{user_id}"
    cart = r.hgetall(key)
    # 将商品数量转为整数
    cart_dict = {product_id: int(quantity)
                 for product_id, quantity in cart.items()}
    print(f"用户{user_id}的购物车：{cart_dict}")
    return cart_dict


# 测试代码
if __name__ == "__main__":
    # 添加商品
    add_to_cart(2001, 1001, 2)
    add_to_cart(2001, 1002, 1)
    # 查询购物车
    get_cart(2001)
    # 修改商品数量
    update_cart(2001, 1001, 3)
    # 删除商品
    delete_from_cart(2001, 1002)
    # 再次查询购物车
    get_cart(2001)
