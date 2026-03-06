import redis.asyncio as redis
from datetime import datetime, timedelta

class RedisPointManager:
    def __init__(self, redis_url):
        self.pool = redis.ConnectionPool.from_url(redis_url, decode_responses=True)
        self.redis = redis.Redis(connection_pool=self.pool)

    async def check_cooling_and_lock(self, group_id: int, user_id: int, cooldown: int) -> bool:
        """检查冷却时间，如果在冷却中返回 False，否则锁定并返回 True"""
        key = f"cool:{group_id}:{user_id}"
        # set nx=True 只有键不存在时才设置成功
        return bool(await self.redis.set(key, "1", ex=cooldown, nx=True))

    async def check_and_incr_daily(self, group_id: int, user_id: int, limit: int) -> bool:
        """增加每日计数，如果超过上限返回 False"""
        date_str = datetime.now().strftime("%Y%m%d")
        key = f"daily:{group_id}:{user_id}:{date_str}"
        
        current = await self.redis.incr(key)
        if current == 1:
            # 首次设置，过期时间设为当晚 23:59:59
            end_of_day = datetime.now().replace(hour=23, minute=59, second=59)
            await self.redis.expireat(key, int(end_of_day.timestamp()))
            
        return current <= limit

    async def verify_admin_session(self, user_id: int) -> bool:
        return await self.redis.exists(f"admin_session:{user_id}")

    async def create_admin_session(self, user_id: int):
        await self.redis.set(f"admin_session:{user_id}", "1", ex=1800) # 30分钟

    async def close(self):
        await self.redis.aclose()
        await self.pool.disconnect()