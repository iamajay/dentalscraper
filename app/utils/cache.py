from aiocache import caches

caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'ttl': 3600,  # 1 hour
    }
})

cache = caches.get('default')