from framework.bootstraps.bootstrap import Bootstrap


class Utils:

    @staticmethod
    def mutable_op(func):
        def wrap(cls, *args, **kwargs):
            if not cls._mutable_lock:
                raise Exception("mutable lock is off")
            return func(cls, *args, **kwargs)

        return wrap


class Context:
    _mutable_lock = True
    _bootstraps = []
    _storage = {}

    @classmethod
    def add(cls, key, value):
        cls._storage[key] = value

    @classmethod
    def get(cls, key):
        return cls._storage[key]

    @classmethod
    @Utils.mutable_op
    def add_bootstrap(cls, bootstrap: Bootstrap):
        print("add_bootstrap")
        cls._bootstraps.append(bootstrap)

    @classmethod
    def run_context(cls):
        print("run_context")
        cls._mutable_lock = False
        for bootstrap in cls._bootstraps:
            bootstrap.awake()
