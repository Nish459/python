# PATTERN #2: FACTORY PATTERN
## Complete Interview-Ready Guide

---

## 1. DEFINITION & INTENT

### What Problem Does It Solve?
- Need to create objects without specifying exact classes
- Want to decouple client code from concrete classes
- Creation logic is complex and should be centralized
- Want to switch implementations easily (e.g., different databases)

### Real-World Analogy (2-3 lines)
**Restaurant kitchen**: Instead of each customer making their own burger, you go to a window and ask "Give me a burger." The kitchen decides if it's a veggie burger or beef burger based on your order. The customer doesn't need to know HOW it's made or WHAT type it is.

### When TO Use
✓ Multiple related product types
✓ Creation logic is complex
✓ Want to hide implementation details
✓ Need runtime flexibility to switch implementations
✓ Following Open/Closed Principle

### When NOT to Use
✗ Creating single simple objects
✗ When object creation is trivial
✗ For just one product type (use Singleton instead)

---

## 2. REAL-WORLD EXAMPLES

### Example 1: Database Connection Factory (Production-Grade)
```python
# Scenario: Your application needs to support MySQL, PostgreSQL, and MongoDB
# You don't want your code hardcoded to one database

class DatabaseConnection:
    def connect(self):
        pass
    
    def execute_query(self, query):
        pass

class MySQLConnection(DatabaseConnection):
    def __init__(self, host, port=3306):
        self.host = host
        self.port = port
    
    def connect(self):
        return f"Connected to MySQL at {self.host}:{self.port}"
    
    def execute_query(self, query):
        return f"MySQL executing: {query}"

class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host, port=5432):
        self.host = host
        self.port = port
    
    def connect(self):
        return f"Connected to PostgreSQL at {self.host}:{self.port}"
    
    def execute_query(self, query):
        return f"PostgreSQL executing: {query}"

class MongoDBConnection(DatabaseConnection):
    def __init__(self, host, port=27017):
        self.host = host
        self.port = port
    
    def connect(self):
        return f"Connected to MongoDB at {self.host}:{self.port}"
    
    def execute_query(self, query):
        return f"MongoDB executing: {query}"

# Factory Class
class DatabaseFactory:
    _databases = {
        'mysql': MySQLConnection,
        'postgresql': PostgreSQLConnection,
        'mongodb': MongoDBConnection
    }
    
    @staticmethod
    def create_connection(db_type, host, port=None):
        """
        Factory method to create appropriate database connection
        
        Args:
            db_type: 'mysql', 'postgresql', 'mongodb'
            host: Database host
            port: Database port (optional, uses defaults)
        
        Returns:
            DatabaseConnection instance
        
        Raises:
            ValueError: If unsupported database type
        """
        if db_type not in DatabaseFactory._databases:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        db_class = DatabaseFactory._databases[db_type]
        
        if port is None:
            return db_class(host)
        return db_class(host, port)

# Usage
# Client code doesn't know about concrete classes!
db = DatabaseFactory.create_connection('postgresql', 'localhost', 5432)
print(db.connect())  # Connected to PostgreSQL at localhost:5432
print(db.execute_query("SELECT * FROM users"))

# Easy to switch - just change string!
db = DatabaseFactory.create_connection('mysql', 'localhost')
print(db.connect())  # Connected to MySQL at localhost:3306
```

**Where It's Used in FANG**:
- AWS SDKs (create different service clients)
- Django ORM (DatabaseWrapper factory for different databases)
- SQLAlchemy engine creation
- Kafka client factory for different brokers

---

### Example 2: Payment Gateway Factory (E-commerce System)
```python
# Scenario: Flipkart-like e-commerce needs multiple payment methods
# PayPal, Stripe, RazorPay, Google Pay, Apple Pay

from abc import ABC, abstractmethod
from enum import Enum
from decimal import Decimal

class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: Decimal, user_id: str) -> dict:
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str) -> dict:
        pass
    
    @abstractmethod
    def verify(self, token: str) -> bool:
        pass

class RazorPayGateway(PaymentGateway):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.name = "RazorPay"
    
    def charge(self, amount: Decimal, user_id: str) -> dict:
        # In reality: call RazorPay API
        return {
            'status': PaymentStatus.SUCCESS,
            'gateway': self.name,
            'transaction_id': f'rpay_{user_id}_{amount}',
            'amount': amount
        }
    
    def refund(self, transaction_id: str) -> dict:
        return {'status': PaymentStatus.SUCCESS, 'transaction_id': transaction_id}
    
    def verify(self, token: str) -> bool:
        return token.startswith('rpay_')

class StripeGateway(PaymentGateway):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.name = "Stripe"
    
    def charge(self, amount: Decimal, user_id: str) -> dict:
        return {
            'status': PaymentStatus.SUCCESS,
            'gateway': self.name,
            'transaction_id': f'stripe_{user_id}_{amount}',
            'amount': amount
        }
    
    def refund(self, transaction_id: str) -> dict:
        return {'status': PaymentStatus.SUCCESS, 'transaction_id': transaction_id}
    
    def verify(self, token: str) -> bool:
        return token.startswith('stripe_')

class GooglePayGateway(PaymentGateway):
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id
        self.name = "GooglePay"
    
    def charge(self, amount: Decimal, user_id: str) -> dict:
        return {
            'status': PaymentStatus.SUCCESS,
            'gateway': self.name,
            'transaction_id': f'gpay_{user_id}_{amount}',
            'amount': amount
        }
    
    def refund(self, transaction_id: str) -> dict:
        return {'status': PaymentStatus.SUCCESS, 'transaction_id': transaction_id}
    
    def verify(self, token: str) -> bool:
        return token.startswith('gpay_')

# Factory
class PaymentGatewayFactory:
    _gateways = {
        'razorpay': RazorPayGateway,
        'stripe': StripeGateway,
        'googlepay': GooglePayGateway
    }
    
    @staticmethod
    def create(gateway_type: str, **kwargs) -> PaymentGateway:
        """
        Create payment gateway instance
        
        Args:
            gateway_type: 'razorpay', 'stripe', 'googlepay'
            **kwargs: Gateway-specific credentials
        
        Returns:
            PaymentGateway instance
        """
        if gateway_type not in PaymentGatewayFactory._gateways:
            raise ValueError(f"Unsupported gateway: {gateway_type}")
        
        gateway_class = PaymentGatewayFactory._gateways[gateway_type]
        return gateway_class(**kwargs)

# Usage in Order Service
class OrderService:
    def __init__(self, payment_gateway: PaymentGateway):
        self.payment_gateway = payment_gateway
    
    def process_payment(self, order_id: str, amount: Decimal, user_id: str) -> bool:
        try:
            result = self.payment_gateway.charge(amount, user_id)
            if result['status'] == PaymentStatus.SUCCESS:
                print(f"Order {order_id} paid via {result['gateway']}")
                return True
            return False
        except Exception as e:
            print(f"Payment failed: {e}")
            return False

# Client Code
config = {
    'razorpay': {'api_key': 'key_123', 'api_secret': 'secret_123'},
    'stripe': {'api_key': 'sk_live_123'},
    'googlepay': {'merchant_id': 'flipkart_123'}
}

# Scenario 1: Use RazorPay for Indian users
gateway = PaymentGatewayFactory.create('razorpay', **config['razorpay'])
order_service = OrderService(gateway)
order_service.process_payment('ORD123', Decimal('1000'), 'user_1')
# Output: Order ORD123 paid via RazorPay

# Scenario 2: Use Stripe for international users
gateway = PaymentGatewayFactory.create('stripe', **config['stripe'])
order_service = OrderService(gateway)
order_service.process_payment('ORD124', Decimal('50'), 'user_2')
# Output: Order ORD124 paid via Stripe

# Scenario 3: Use GooglePay for mobile users
gateway = PaymentGatewayFactory.create('googlepay', **config['googlepay'])
order_service = OrderService(gateway)
order_service.process_payment('ORD125', Decimal('500'), 'user_3')
# Output: Order ORD125 paid via GooglePay
```

**Where It's Used in FANG**:
- Flipkart: Multiple payment methods (RazorPay, PayU, Stripe, GooglePay, Apple Pay)
- Amazon: Different shipping providers factory
- Meta: Different ad network factories
- Google Cloud: Different storage backend factories (GCS, BigTable, Datastore)

---

## 3. FACTORY PATTERN VARIANTS

### Simple Factory (Static Method)
```python
class LoggerFactory:
    @staticmethod
    def create_logger(log_type: str):
        if log_type == 'file':
            return FileLogger()
        elif log_type == 'console':
            return ConsoleLogger()
        else:
            return NullLogger()
```

### Abstract Factory (Multiple Product Families)
```python
# When you need related products
class UIComponentFactory(ABC):
    @abstractmethod
    def create_button(self): pass
    @abstractmethod
    def create_textbox(self): pass

class WindowsUIFactory(UIComponentFactory):
    def create_button(self): return WindowsButton()
    def create_textbox(self): return WindowsTextbox()

class MacUIFactory(UIComponentFactory):
    def create_button(self): return MacButton()
    def create_textbox(self): return MacTextbox()
```

---

## 4. STRUCTURE

```
Client
   ↓ (uses)
Factory
   ├─→ (creates) ConcreteProductA
   ├─→ (creates) ConcreteProductB
   └─→ (creates) ConcreteProductC

All products implement → Product Interface
```

---

## 5. COMPLETE PRODUCTION IMPLEMENTATION

```python
from abc import ABC, abstractmethod
from typing import Dict, Type
import logging

# Abstract Product
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: str) -> str:
        pass
    
    @abstractmethod
    def validate(self, data: str) -> bool:
        pass

# Concrete Products
class CSVProcessor(DataProcessor):
    def process(self, data: str) -> str:
        lines = data.split('\n')
        return f"Processed {len(lines)} CSV lines"
    
    def validate(self, data: str) -> bool:
        return len(data.split(',')) > 0

class JSONProcessor(DataProcessor):
    def process(self, data: str) -> str:
        import json
        try:
            obj = json.loads(data)
            return f"Processed JSON with {len(obj)} keys"
        except:
            return "Invalid JSON"
    
    def validate(self, data: str) -> bool:
        import json
        try:
            json.loads(data)
            return True
        except:
            return False

class XMLProcessor(DataProcessor):
    def process(self, data: str) -> str:
        from xml.etree import ElementTree as ET
        try:
            root = ET.fromstring(data)
            return f"Processed XML with root tag: {root.tag}"
        except:
            return "Invalid XML"
    
    def validate(self, data: str) -> bool:
        from xml.etree import ElementTree as ET
        try:
            ET.fromstring(data)
            return True
        except:
            return False

# Factory with Registry Pattern
class DataProcessorFactory:
    _processors: Dict[str, Type[DataProcessor]] = {
        'csv': CSVProcessor,
        'json': JSONProcessor,
        'xml': XMLProcessor
    }
    
    @classmethod
    def register(cls, file_type: str, processor_class: Type[DataProcessor]):
        """Register new processor type dynamically"""
        cls._processors[file_type] = processor_class
    
    @classmethod
    def create(cls, file_type: str) -> DataProcessor:
        """Create processor instance"""
        if file_type not in cls._processors:
            raise ValueError(f"Unsupported type: {file_type}. Supported: {list(cls._processors.keys())}")
        
        return cls._processors[file_type]()
    
    @classmethod
    def supported_types(cls) -> list:
        """Get list of supported types"""
        return list(cls._processors.keys())

# Client Code
class DataPipeline:
    def __init__(self, file_type: str):
        self.processor = DataProcessorFactory.create(file_type)
        self.file_type = file_type
    
    def execute(self, data: str) -> dict:
        if not self.processor.validate(data):
            return {'success': False, 'error': f'Invalid {self.file_type} data'}
        
        result = self.processor.process(data)
        return {'success': True, 'result': result, 'type': self.file_type}

# Usage
if __name__ == '__main__':
    # CSV Processing
    csv_data = "name,age,city\nJohn,25,Delhi\nJane,30,Mumbai"
    pipeline = DataPipeline('csv')
    print(pipeline.execute(csv_data))
    # {'success': True, 'result': 'Processed 3 CSV lines', 'type': 'csv'}
    
    # JSON Processing
    json_data = '{"name": "John", "age": 25}'
    pipeline = DataPipeline('json')
    print(pipeline.execute(json_data))
    # {'success': True, 'result': 'Processed JSON with 2 keys', 'type': 'json'}
    
    # Register custom processor dynamically
    class YAMLProcessor(DataProcessor):
        def process(self, data: str) -> str:
            return "Processed YAML"
        def validate(self, data: str) -> bool:
            return True
    
    DataProcessorFactory.register('yaml', YAMLProcessor)
    print(DataProcessorFactory.supported_types())
    # ['csv', 'json', 'xml', 'yaml']
```

---

## 6. INTERVIEW QUESTIONS

### Q1: "What's the difference between Factory and Abstract Factory?"

**Answer with Code**:
```python
# Simple Factory: Creates ONE product
class ShapeFactory:
    @staticmethod
    def create(shape_type):
        if shape_type == 'circle':
            return Circle()
        return Square()

# Abstract Factory: Creates FAMILIES of related products
class UIFactory(ABC):
    @abstractmethod
    def create_button(self): pass
    @abstractmethod
    def create_textbox(self): pass

# Use Simple Factory when: Single product type
# Use Abstract Factory when: Multiple related products that go together
```

**Interview Evaluation**: Candidate understands when to use each variant.

---

### Q2: "How do you add a new product without modifying factory?"

**Answer with Code**:
```python
# BAD: Modifying factory for each new type (violates Open/Closed Principle)
def create(db_type):
    if db_type == 'mysql':
        return MySQLConnection()
    elif db_type == 'postgresql':
        return PostgreSQLConnection()
    elif db_type == 'mongodb':  # Modified!
        return MongoDBConnection()

# GOOD: Register pattern (Open/Closed compliant)
class DatabaseFactory:
    _drivers = {}
    
    @classmethod
    def register(cls, name: str, driver_class):
        cls._drivers[name] = driver_class
    
    @classmethod
    def create(cls, name: str):
        return cls._drivers[name]()

# Add new driver without modifying factory
DatabaseFactory.register('mongodb', MongoDBConnection)
DatabaseFactory.register('cassandra', CassandraConnection)
```

**Interview Evaluation**: Candidate follows Open/Closed Principle.

---

### Q3: "When would you use Factory vs Dependency Injection?"

**Answer**:
```python
# Use Factory when: Type is determined at runtime based on configuration
config = load_config()
db = DatabaseFactory.create(config['database_type'])

# Use Dependency Injection when: Type is known at startup
app = Flask(__name__)
db = PostgreSQLConnection(host='localhost')
app.db = db

# They complement each other!
# Factory determines TYPE, DI injects INSTANCE
gateway_type = user.region == 'India' ? 'razorpay' : 'stripe'
gateway = PaymentGatewayFactory.create(gateway_type)
service = OrderService(gateway)  # DI
```

**Interview Evaluation**: Candidate understands complementary patterns.

---

### Q4: "Design a notification system that supports Email, SMS, and Push notifications"

**Expected Answer**:
```python
from abc import ABC, abstractmethod
from typing import List

class Notification(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        # Call SMTP service
        return True

class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        # Call Twilio API
        return True

class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        # Call FCM/APNS
        return True

class NotificationFactory:
    _notifications = {
        'email': EmailNotification,
        'sms': SMSNotification,
        'push': PushNotification
    }
    
    @staticmethod
    def create(notification_type: str) -> Notification:
        if notification_type not in NotificationFactory._notifications:
            raise ValueError(f"Unknown type: {notification_type}")
        return NotificationFactory._notifications[notification_type]()

class NotificationService:
    def __init__(self):
        self.notifications: List[Notification] = []
    
    def add_notification(self, notification_type: str):
        notification = NotificationFactory.create(notification_type)
        self.notifications.append(notification)
    
    def notify_user(self, user_id: str, message: str) -> int:
        """Send notification through all registered channels"""
        success_count = 0
        for notification in self.notifications:
            if notification.send(user_id, message):
                success_count += 1
        return success_count

# Usage
service = NotificationService()
service.add_notification('email')
service.add_notification('sms')
service.notify_user('user@example.com', 'Order confirmed!')
```

---

## 7. COMMON MISTAKES

### Mistake 1: Over-Engineering Simple Cases
```python
# WRONG: Factory for single type
class UserFactory:
    @staticmethod
    def create():
        return User()

# RIGHT: Just instantiate directly
user = User()
```

---

### Mistake 2: Factory Tightly Coupled to Implementations
```python
# WRONG: Hardcoded class references
def create(db_type):
    if db_type == 'mysql':
        return __import__('mysql_module').MySQLConnection()

# RIGHT: Registry pattern
class Factory:
    _registry = {}
    
    @classmethod
    def register(cls, name, clazz):
        cls._registry[name] = clazz
    
    @classmethod
    def create(cls, name):
        return cls._registry[name]()
```

---

### Mistake 3: Forgetting About Configuration
```python
# WRONG: Magic strings everywhere
gateway = PaymentGatewayFactory.create('stripe')

# RIGHT: Configuration-driven
gateway_type = config['payment_gateway']
gateway = PaymentGatewayFactory.create(gateway_type)
```

---

### Mistake 4: Factory Creating Singleton Instead of New Instances
```python
# WRONG: Should you cache or create fresh?
# Depends on use case!

# Database: Cache (expensive resource)
class DatabaseFactory:
    _connections = {}
    
    @classmethod
    def get(cls, db_type):
        if db_type not in cls._connections:
            cls._connections[db_type] = cls._create(db_type)
        return cls._connections[db_type]

# Notification: Create fresh (lightweight)
class NotificationFactory:
    @staticmethod
    def create(notification_type):
        return _types[notification_type]()  # Always new
```

---

## 8. KEY POINTS TO REMEMBER

**Quick Definition** (30 seconds):
> "Factory pattern encapsulates object creation logic, allowing clients to create objects without knowing concrete classes. It decouples client code from implementations and makes it easy to add new types without modifying existing code. Use it when you have multiple related types and want runtime flexibility."

**When to use**:
- Multiple product types
- Creation logic is complex
- Types determined at runtime
- Want to follow Open/Closed Principle

**Three variants**:
1. **Simple Factory**: Static method creating one type
2. **Factory Method**: Abstract class with subclasses implementing creation
3. **Abstract Factory**: Multiple related products

---

## 9. COMPARISON TABLE

| Aspect | Singleton | Factory |
|--------|-----------|---------|
| **Purpose** | One instance globally | Create objects decoupled from client |
| **Control** | Limits instantiation | Encapsulates creation |
| **Flexibility** | Low (single type) | High (multiple types) |
| **Thread Safety** | Must handle manually | Depends on implementation |
| **Testing** | Hard (global state) | Easy (pass different types) |
| **Use Case** | Logger, Config | Multiple DB types, Gateways |

---

## 10. NEXT PATTERN

Once you master Factory, move to **Strategy Pattern** because:
- Strategy is about behavior, Factory is about creation
- Often used together (Factory creates strategies)
- Very common in real systems
- More interview questions