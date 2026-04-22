def bootstrap_resource(path: str):
    def decorator(cls):
        cls.resource_path = path
        return cls

    return decorator
