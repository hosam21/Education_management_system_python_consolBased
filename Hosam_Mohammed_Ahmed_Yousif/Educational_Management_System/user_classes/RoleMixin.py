class RoleMixin:

    @classmethod
    def role_check(cls, allowed_roles):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if not any(isinstance(self, role) for role in allowed_roles):
                    raise PermissionError("Unauthorized access for this role")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
