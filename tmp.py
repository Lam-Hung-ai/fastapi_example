from datetime import datetime, timezone, timedelta
ACCESS_TOKEN_EXPIRE_MINUTES= 30
# Lấy thời gian hiện tại theo UTC
current_time_utc = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
expire = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7))) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

print(current_time_utc)
print(expire)
