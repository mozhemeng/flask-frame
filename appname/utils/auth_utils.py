from appname.extentions import redis_store


def merge_jit_key(identity, jti):
    return f"user:{identity}.auth:{jti}"


def revoke_all_key(identity):
    pattern = f"user:{identity}.*"
    keys = redis_store.keys(pattern=pattern)
    redis_store.delete(*keys)