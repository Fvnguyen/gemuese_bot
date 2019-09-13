import os
import pickle
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))

def admin_stats():
    filename = 'bot_stats'
    data = pickle.loads(r.get(filename))
    return data

print(admin_stats())
