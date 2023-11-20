class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# allow only one instance of a class, second try will raise an exception
class Onceton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            raise Exception(f"Only one instance of {cls} is allowed")
        else:
            cls._instances[cls] = super(Onceton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
