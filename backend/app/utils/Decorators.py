from functools import wraps
from flask_jwt_extended import get_jwt
from flask import abort

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in [r.value for r in roles]:
                abort(403, description="Permission denied")
            return fn(*args, **kwargs)
        return decorated
    return wrapper
