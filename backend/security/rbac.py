from flask_jwt_extended import get_jwt

def role_required(allowed_roles):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return {"msg": "Unauthorized"}, 403

            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper