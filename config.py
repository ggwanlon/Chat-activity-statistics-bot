import os
import hashlib

# Bot 设置
BOT_TOKEN = "8685627246:AAGn_Tc54mCLiP69BFgoDnDtQ4vlffTSwkY"  # 替换为你的 Token

# 数据库设置 (默认使用 SQLite，可换 PostgreSQL)
DB_URL = "sqlite+aiosqlite:///./bot_database.db"
REDIS_URL = "redis://localhost:6379/0"

# 管理员设置
SUPER_ADMIN_IDS = [8789960462,39499550,'@ggvernon','@Lisa_bella05']  # 替换为实际管理员 ID
# 密码哈希 (示例密码: 123456)
ADMIN_PASSWORD_HASH = hashlib.sha256("marscat888888".encode()).hexdigest()

# 积分规则
DAILY_LIMIT = 50
POINTS_PER_MSG = 1
COOLDOWN_SECONDS = 60
MIN_TEXT_LENGTH = 5
CYCLE_DAYS = 30