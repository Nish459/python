"""
Singletom Pattern

It ensures that there is a single instance of a singleton class throughout the application.
And the object has global access to it.

It is useful when creating multiple instances of a class can cause inconsistency or memory issues.
Examples: Database connection, logging, cache handling

If different parts of application creates different instances than it can create debugging difficult

Solution:
Instead of creating a new object everytime validate if an object is already created and if not create a new one.
"""


class SingletonBad:
    def __init__(self) -> None:
        self.instance = None

class Singleton:
    
    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    
if __name__ == "__main__":
    print("----BAD: Singleton Pattern----")
    singleton = SingletonBad()
    singleton_bad2 = SingletonBad()
    print(singleton is singleton_bad2)
    print(singleton == singleton_bad2)
    print(singleton.instance is singleton_bad2.instance)
    print(singleton.instance == singleton_bad2.instance)

    print("----GOOD: Singleton Pattern----")
    singleton2 = Singleton()
    singleton3 = Singleton()
    print(singleton2 is singleton3)
    print(singleton2 == singleton3)
    print(singleton2._instance is singleton3._instance)
    print(singleton2._instance == singleton3._instance)
