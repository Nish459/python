# PATTERN #1: SINGLETON PATTERN
## Complete Interview-Ready Guide

---

## 1. DEFINITION & INTENT

### What Problem Does It Solve?
- Need exactly ONE instance of a class throughout the application
- That instance must be globally accessible
- Must prevent accidental creation of multiple instances
- Should be lazy-initialized (created only when needed)

### Real-World Analogy
**Database connection pool**: Your application should have only ONE connection to the database, not multiple independent connections that waste resources.

### When TO Use
✓ Database connections
✓ Logger instances
✓ Configuration managers
✓ Thread pools
✓ Cache managers
✓ File systems
✓ Print spoolers

### When NOT to Use (Critical!)
✗ When you need multiple independent instances
✗ When testing (makes mocking difficult)
✗ When you want to scale horizontally
✗ When dealing with multiple threads without proper synchronization
✗ Just because "there should only be one" — use dependency injection instead!

---

## 2. STRUCTURE

### Components
1. **Private Constructor** - Prevents instantiation from outside
2. **Class Variable** - Holds the single instance
3. **Class Method** - Returns the single instance (gets_instance or getInstance)
4. **Private/Protected Attributes** - Internal state

### Relationships
```
Client
  ↓ (calls)
Singleton.get_instance()
  ↓ (returns)
Singleton instance (always same)
```

---

## 3. IMPLEMENTATION IN PYTHON (Production Approaches)

### Approach 1: Simple Class-Based (NOT Recommended for threading)
```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if self._initialized:
            return
        self._initialized = True
        self.connection = self._connect()
    
    def _connect(self):
        print("Creating database connection...")
        return "DB_CONNECTION_OBJECT"
    
    def execute_query(self, query):
        return f"Executing: {query}"

# Usage
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True - same instance
```

**Interview Evaluation**: Candidate understands __new__ and __init__, but this is NOT thread-safe.

---

### Approach 2: Thread-Safe Singleton (Recommended for Production)
```python
import threading

class Logger:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # Double-checked locking pattern
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        with self._lock:
            if self._initialized:
                return
            
            self._initialized = True
            self.logs = []
            print("Logger initialized")
    
    def log(self, message):
        with self._lock:
            self.logs.append(message)
            print(f"[LOG] {message}")
    
    def get_logs(self):
        return self.logs.copy()

# Usage
logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True
logger1.log("Error occurred")
print(logger2.get_logs())  # Can access from logger2
```

**Interview Evaluation**: Candidate understands thread safety, lock mechanisms, and double-checked locking. This is PRODUCTION-READY.

---

### Approach 3: Decorator-Based (Elegant Python Style)
```python
def singleton(cls):
    """
    Decorator to convert a class into a Singleton.
    Thread-safe implementation.
    """
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class ConfigurationManager:
    def __init__(self):
        self.config = {}
        print("ConfigManager initialized")
    
    def set_config(self, key, value):
        self.config[key] = value
    
    def get_config(self, key):
        return self.config.get(key)

# Usage
config1 = ConfigurationManager()
config2 = ConfigurationManager()
print(config1 is config2)  # True
config1.set_config("db_host", "localhost")
print(config2.get_config("db_host"))  # "localhost"
```

**Interview Evaluation**: Candidate shows advanced Python knowledge (decorators, closures). This is PYTHONIC and ELEGANT.

---

### Approach 4: Metaclass-Based (Most Powerful, Most Complex)
```python
import threading

class SingletonMeta(type):
    """
    Thread-safe metaclass for singleton pattern.
    Metaclass controls class creation itself.
    """
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class CacheManager(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}
        print("Cache initialized")
    
    def set(self, key, value):
        self.cache[key] = value
    
    def get(self, key):
        return self.cache.get(key)

# Usage
cache1 = CacheManager()
cache2 = CacheManager()
print(cache1 is cache2)  # True
```

**Interview Evaluation**: Candidate demonstrates deep Python knowledge (metaclasses). Advanced level.

---

## 4. INTERVIEW PERSPECTIVE

### Why Would Interviewer Ask This?

1. **Test OOP Understanding**
   - Constructors, class variables, instance variables
   - Python __new__ vs __init__

2. **Test Thread Safety Knowledge**
   - Race conditions
   - Synchronization primitives
   - Double-checked locking

3. **Test Real-World Thinking**
   - When to use vs alternatives
   - Tradeoffs of each approach

4. **Test Python-Specific Knowledge**
   - Decorators, metaclasses, __new__
   - Closures and scoping

### Common Follow-Up Questions

**Q1: "Is this thread-safe?"**
- Answer: "Approach 1 (basic __new__) is NOT thread-safe. If two threads call __new__ simultaneously, they might create two instances. Approaches 2-4 use locks for thread safety."
- Code to show race condition:
```python
import concurrent.futures

# With non-thread-safe singleton
results = set()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(lambda: id(DatabaseConnection())) for _ in range(10)]
    results = {f.result() for f in futures}

print(f"Number of instances: {len(results)}")  # Will show >1 without locks!
```

**Q2: "How would you test this?"**
- Answer:
```python
# Testing Singleton
import unittest
from unittest.mock import patch

class TestSingleton(unittest.TestCase):
    def tearDown(self):
        # Reset singleton for each test
        Logger._instance = None
    
    def test_singleton_instance(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertIs(logger1, logger2)
    
    def test_log_functionality(self):
        logger = Logger()
        logger.log("Test message")
        self.assertEqual(len(logger.get_logs()), 1)
```

**Q3: "What about memory? Can we clear the singleton?"**
- Answer: "In production, you usually don't. But if needed, add a reset method (rarely used):"
```python
@classmethod
def reset(cls):
    """Reset singleton - use only in testing"""
    with cls._lock:
        cls._instance = None
```

**Q4: "Why not just use a global variable?"**
- Answer: 
  - Global variables can be reassigned anywhere
  - Singleton enforces that it's the only instance
  - Lazy initialization (only created when needed)
  - Better testing (can inject/mock)
  - Clear intent in code

**Q5: "How would you pass this to other components?"**
- Answer: "Dependency Injection is BETTER than Singleton!"
```python
# Better approach: Dependency Injection
class UserService:
    def __init__(self, logger: Logger, db: DatabaseConnection):
        self.logger = logger
        self.db = db
    
    def create_user(self, user_data):
        self.logger.log(f"Creating user: {user_data}")
        return self.db.execute_query(f"INSERT USER {user_data}")

# Usage
logger = Logger()
db = DatabaseConnection()
user_service = UserService(logger, db)
user_service.create_user({"name": "John"})
```

---

## 5. REAL-WORLD USAGE

### In Open Source

**Python Logging Module**:
```python
import logging

# getLogger returns the same logger instance for same name
logger1 = logging.getLogger("myapp")
logger2 = logging.getLogger("myapp")
# logger1 is logger2 → True (Singleton pattern!)
```

**Django Settings**:
```python
from django.conf import settings
# settings is effectively a singleton
```

**SQLAlchemy Engine**:
```python
from sqlalchemy import create_engine

# Best practice: keep engine as singleton
engine = create_engine('postgresql://...')
# Reuse same engine (connection pooling)
```

### At Google (Real Examples)
- Protocol Buffer registry (single instance)
- Metrics collector (single instance across service)
- Service discovery client (single instance)

### At Amazon
- AWS SDK clients (singleton pattern for credentials)
- Lambda context (singleton per invocation)

---

## 6. VARIANTS & RELATED PATTERNS

### Singleton vs Service Locator
```python
# Service Locator (related but different)
class ServiceLocator:
    _services = {}
    
    @classmethod
    def register(cls, service_name, service):
        cls._services[service_name] = service
    
    @classmethod
    def get(cls, service_name):
        return cls._services[service_name]

# Difference: Service Locator can have multiple services,
# Singleton is specifically for one instance
```

### Singleton vs Module-Level Variable
```python
# Module-level singleton (simpler for non-threaded code)
# database.py
_db = None

def get_db():
    global _db
    if _db is None:
        _db = DatabaseConnection()
    return _db

# Better: Just use the module itself as singleton
# This is how Python's logging module works
```

### Related Patterns
- **Factory Pattern**: Creates instances (Singleton is also a factory)
- **Monostate Pattern**: All instances share same state (different approach)
- **Borg Pattern**: All instances appear as one (Python alternative)

---

## 7. PRACTICE QUESTIONS

### Question 1: Design a Thread-Safe Logger Singleton
**Problem**: Create a logger that:
- Has only one instance
- Is thread-safe
- Buffers logs and flushes every 100 logs or on shutdown
- Allows setting log level

**Expected Answer Structure**:
```python
import threading
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    ERROR = 3

class Logger:
    _instance = None
    _lock = threading.Lock()
    _buffer_lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        with self._lock:
            if self._initialized:
                return
            
            self._initialized = True
            self.log_buffer = []
            self.log_level = LogLevel.INFO
            self.buffer_size = 100
    
    def set_level(self, level: LogLevel):
        self.log_level = level
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        if level.value < self.log_level.value:
            return
        
        with self._buffer_lock:
            timestamp = datetime.now().isoformat()
            log_entry = f"[{timestamp}] [{level.name}] {message}"
            self.log_buffer.append(log_entry)
            
            if len(self.log_buffer) >= self.buffer_size:
                self._flush()
    
    def _flush(self):
        # Write to file or remote service
        for entry in self.log_buffer:
            print(entry)  # In real code: write to file
        self.log_buffer.clear()
    
    def shutdown(self):
        with self._buffer_lock:
            self._flush()
```

**Interview Evaluation**:
- ✓ Understands __new__ and __init__
- ✓ Implements proper locking
- ✓ Considers buffer management
- ✓ Adds practical features (log level, flushing)

---

### Question 2: Refactor This to Not Use Singleton
**Problem Code**:
```python
# BAD: Singleton in domain logic
class UserRepository:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = DatabaseConnection()
        return cls._instance
```

**Expected Refactored Answer**:
```python
# GOOD: Dependency Injection
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection

# Usage
db = DatabaseConnection()  # Keep as singleton if needed
user_repo = UserRepository(db)

# Testing becomes easy
class MockDB:
    pass

test_repo = UserRepository(MockDB())
```

**Interview Evaluation**:
- ✓ Understands when NOT to use Singleton
- ✓ Prefers dependency injection
- ✓ Thinks about testability

---

### Question 3: Identify the Bug
```python
class Counter:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1

# What happens here?
c1 = Counter()
c1.increment()
print(c1.count)  # 1

c2 = Counter()
print(c2.count)  # 0 <- BUG!
```

**Expected Answer**:
- `__init__` is called every time, resetting count to 0
- Fix: Add `_initialized` flag or move logic to `__new__`

---

## 8. COMMON INTERVIEW MISTAKES

### Mistake 1: Forgetting __init__ is Called Every Time
```python
# WRONG
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.data = {}  # BUG: Gets reset every time!

# Consequence:
c1 = Config()
c1.data['key'] = 'value'
c2 = Config()
print(c2.data)  # {} <- Empty!
```

**Fix**:
```python
def __init__(self):
    if hasattr(self, '_initialized'):
        return
    self._initialized = True
    self.data = {}
```

---

### Mistake 2: Forgetting Thread Safety
```python
# WRONG for multithreaded environment
class DB:
    _instance = None
    def __new__(cls):
        if cls._instance is None:  # Race condition here!
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Race Condition Timeline**:
```
Thread 1: Check _instance (None) → enter if
Thread 2: Check _instance (None) → enter if
Thread 1: Create instance
Thread 2: Create instance  ← Two instances!
```

**Fix**: Use locks

---

### Mistake 3: Over-Using Singleton
```python
# WRONG: Using singleton just because "there should be only one"
class UserValidator:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Better: Just use dependency injection
class UserValidator:
    pass

# Pass it where needed
validator = UserValidator()
service = UserService(validator)
```

---

### Mistake 4: Not Considering Testability
```python
# HARD TO TEST
class OrderService:
    def __init__(self):
        self.db = DatabaseConnection()  # Singleton, can't mock
    
    def process_order(self, order):
        self.db.save(order)

# Better:
class OrderService:
    def __init__(self, db):
        self.db = db

# Now testable:
mock_db = MockDB()
service = OrderService(mock_db)
```

---

### Mistake 5: Confusing Singleton With Global Variable
```python
# They're NOT the same
_global_logger = None  # Global variable (can be reassigned)

logger_instance = Logger()  # Singleton (can't be reassigned via __new__)
```

---

## 9. WHAT TO MEMORIZE FOR INTERVIEW

**30-Second Explanation**:
> "Singleton pattern ensures a class has only one instance and provides a global point of access to it. It's useful for resources like loggers, database connections, or configuration managers that should exist exactly once. The key is controlling instantiation through a private constructor and providing a static method to get the instance. In Python, you can implement it using __new__, decorators, or metaclasses. For multithreaded environments, you must use double-checked locking with locks to prevent race conditions."

**Key Code Snippet (Thread-Safe)**:
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**3 Key Points**:
1. Private constructor via __new__
2. Thread-safe with double-checked locking
3. When NOT to use: Prefer dependency injection instead

---

## 10. NEXT PATTERN (Preview)

Once you master Singleton, move to **Factory Pattern** because:
- Factory also controls object creation
- Often used WITH Singleton
- More interview questions on Factory
- More practical applications