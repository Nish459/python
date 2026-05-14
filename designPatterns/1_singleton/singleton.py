import threading
from functools import wraps
from typing import Any

class ThreadSafeSingleton:
    """ Thread safe singleton pattern """
    # Best for simple, single-threaded applications
    # Used when class is supposed to control it's own behavior and not rely on external factors
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init(self):
        if self._initialized:
            return
        self._initialized = True
        self.logs = []
        print("Logger initialized")

    def get_instance(cls):
        return cls._instance


def singleton(cls: type) -> type:
    """ Decorator to convert a class into a Singleton """
    # good for converting existing class into a singleton
    instances = {}
    lock = threading.Lock()

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> type:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:
    def __init__(self):
        self.logs = []
        print("Logger initialized")



class SingletonMeta(type):
    """ Metaclass to create a singleton """
    # Best for reusable, thread-safe singletons
    # Used when multiple classes has same singleton behavior
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        __call__ is a special method that makes an object "callable" (usable like a function with ()). 
        When you write MyClass(), Python is actually calling __call__() on the metaclass.
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []
        print("Logger initialized")



class SingletonModule:
    """ 
    Module-level singleton:-
    Using the conecept that module is imported only once per process.
    After that each module is imported from sys.modules as python caches imported modules.
    So we can use the module itself as a singleton.

    Example:
    ```python
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized")
    ```
    This will return the same logger instance for each module.
    Best for logger, caching, config etc.
    """
    def __init__(self):
        self.logs = []
        print("Logger initialized")

    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")

    def get_logs(self):
        return self.logs.copy()

logger = SingletonModule()