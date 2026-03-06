import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession # 1. 新增导入
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, REDIS_URL
from database.engine import init_db
from utils.redis_client import RedisPointManager
from handlers import points, admin, scheduler as sch_handlers

# 日志配置
logging.basicConfig(level=logging.INFO)

# --- 关键配置：替换为你自己的代理地址 ---
# 如果你的梯子端口是 7890，就保持不变
# 如果是 10809，就改成 http://127.0.0.1:10809
PROXY_URL = "http://127.0.0.1:10809"  

async def main():
    # 1. 初始化基础组件
    redis_mgr = RedisPointManager(REDIS_URL)
    await init_db()
    
    # 2. 配置代理 Session (修复网络错误的关键)
    session = AiohttpSession(proxy=PROXY_URL)
    
    # 3. 初始化 Bot 时传入 session
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    # 4. 依赖注入
    dp["redis_mgr"] = redis_mgr

    # 5. 注册路由
    dp.include_router(admin.router)
    dp.include_router(points.router)

    # 6. 配置并启动定时任务
    scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(sch_handlers.task_daily_report, 'cron', hour=9, minute=0, args=[bot])
    # 每天 00:00 检查周期结算
    scheduler.add_job(sch_handlers.task_cycle_settlement, 'cron', hour=0, minute=0, args=[bot])
    scheduler.start()

    print("🤖 Bot is running... (Proxy enabled)")
    try:
        await dp.start_polling(bot)
    finally:
        await redis_mgr.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())