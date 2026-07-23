# PATTERN #4: OBSERVER PATTERN

## Complete Interview-Ready Guide

---

## 1. DEFINITION & INTENT

### What Problem Does It Solve?

- Multiple objects need to be notified when state changes
- Don't want tight coupling between subject and observers
- Need one-to-many relationship (one subject, many observers)
- Observers should react automatically to changes
- Want loose coupling and high cohesion

### Real-World Analogy (2-3 lines)

**Email subscription system**: When a blog publishes a new post, all subscribers automatically get notified via email. The blog (subject) doesn't need to know WHO the subscribers are. New subscribers can join anytime. The blog just publishes events.

### When TO Use

✓ One-to-many relationships
✓ Change in one object requires changing others
✓ Object shouldn't assume who will react to changes
✓ Need loose coupling
✓ Event-driven systems
✓ MVC architectures

### When NOT to Use

✗ Simple direct calls are sufficient
✗ Performance critical (observer adds overhead)
✗ Few objects involved (use direct calls)
✗ Observer logic is complex (becomes hard to debug)

---

## 2. REAL-WORLD EXAMPLES

### Example 1: Stock Price Monitoring System (Real-time Notifications)

```python
# Scenario: Stock exchange (like NSE) needs to notify multiple viewers
# when stock price changes. Viewers can be: Mobile App, Web Dashboard, 
# Email Alert Service, SMS Alert Service, Trading Bot

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

class Stock:
    """Subject - maintains state and notifies observers"""
    def __init__(self, symbol: str, name: str, price: float):
        self.symbol = symbol
        self.name = name
        self._price = price
        self._observers: List['StockObserver'] = []
    
    def attach(self, observer: 'StockObserver'):
        """Subscribe observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✓ {observer} subscribed to {self.symbol}")
    
    def detach(self, observer: 'StockObserver'):
        """Unsubscribe observer"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"✗ {observer} unsubscribed from {self.symbol}")
    
    def notify(self):
        """Notify all observers of state change"""
        for observer in self._observers:
            observer.update(self)
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        if new_price != self._price:
            old_price = self._price
            self._price = new_price
            change_percent = ((new_price - old_price) / old_price) * 100
            
            print(f"\n📊 {self.symbol} ({self.name}): ${old_price:.2f} → ${new_price:.2f} ({change_percent:+.2f}%)")
            self.notify()  # Auto-notify all observers

# Observer Interface
class StockObserver(ABC):
    @abstractmethod
    def update(self, stock: Stock):
        """Called when stock price changes"""
        pass

# Concrete Observers
class MobileAppObserver(StockObserver):
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def update(self, stock: Stock):
        print(f"  📱 Mobile App (User {self.user_id}): {stock.symbol} now at ${stock.price:.2f}")
    
    def __repr__(self):
        return f"MobileApp({self.user_id})"

class WebDashboardObserver(StockObserver):
    def __init__(self, dashboard_id: str):
        self.dashboard_id = dashboard_id
    
    def update(self, stock: Stock):
        print(f"  💻 Web Dashboard ({self.dashboard_id}): {stock.symbol} updated → ${stock.price:.2f}")
    
    def __repr__(self):
        return f"WebDashboard({self.dashboard_id})"

class EmailAlertObserver(StockObserver):
    def __init__(self, email: str, price_threshold: float = None):
        self.email = email
        self.price_threshold = price_threshold
    
    def update(self, stock: Stock):
        if self.price_threshold and stock.price < self.price_threshold:
            print(f"  📧 Email Alert: Sent to {self.email} - {stock.symbol} dropped below ${self.price_threshold:.2f}!")
        else:
            print(f"  📧 Email Alert: Sent to {self.email} - {stock.symbol} price update")
    
    def __repr__(self):
        return f"EmailAlert({self.email})"

class SMSAlertObserver(StockObserver):
    def __init__(self, phone: str, target_price: float = None):
        self.phone = phone
        self.target_price = target_price
    
    def update(self, stock: Stock):
        if self.target_price and stock.price >= self.target_price:
            print(f"  📱 SMS Alert: Sent to {self.phone} - {stock.symbol} reached ${self.target_price:.2f}!")
        else:
            print(f"  📱 SMS Alert: Sent to {self.phone} - {stock.symbol} price change")
    
    def __repr__(self):
        return f"SMSAlert({self.phone})"

class TradingBotObserver(StockObserver):
    def __init__(self, bot_id: str, buy_price: float, sell_price: float):
        self.bot_id = bot_id
        self.buy_price = buy_price
        self.sell_price = sell_price
    
    def update(self, stock: Stock):
        if stock.price <= self.buy_price:
            print(f"  🤖 Trading Bot ({self.bot_id}): AUTO BUY {stock.symbol} at ${stock.price:.2f}!")
        elif stock.price >= self.sell_price:
            print(f"  🤖 Trading Bot ({self.bot_id}): AUTO SELL {stock.symbol} at ${stock.price:.2f}!")
    
    def __repr__(self):
        return f"TradingBot({self.bot_id})"

# Usage
if __name__ == '__main__':
    # Create stocks (subjects)
    apple = Stock('AAPL', 'Apple Inc', 150.00)
    tesla = Stock('TSLA', 'Tesla Inc', 250.00)
    
    # Create observers
    mobile_user1 = MobileAppObserver('user_123')
    mobile_user2 = MobileAppObserver('user_456')
    dashboard = WebDashboardObserver('dashboard_1')
    email_alert = EmailAlertObserver('trader@example.com', price_threshold=145.00)
    sms_alert = SMSAlertObserver('+1234567890', target_price=160.00)
    bot = TradingBotObserver('bot_1', buy_price=145.00, sell_price=160.00)
    
    # Subscribe to Apple stock updates
    apple.attach(mobile_user1)
    apple.attach(mobile_user2)
    apple.attach(dashboard)
    apple.attach(email_alert)
    apple.attach(sms_alert)
    apple.attach(bot)
    
    # Price changes trigger notifications
    print("\n" + "="*60)
    apple.price = 148.50
    print("="*60)
    
    apple.price = 155.00
    print("="*60)
    
    apple.price = 144.00  # Below threshold - triggers email & bot
    print("="*60)
    
    # Unsubscribe
    apple.detach(mobile_user1)
    print("\n" + "="*60)
    apple.price = 152.00  # user1 won't get this
```

**Output**:

```
✓ MobileApp(user_123) subscribed to AAPL
✓ MobileApp(user_456) subscribed to AAPL
✓ WebDashboard(dashboard_1) subscribed to AAPL
✓ EmailAlert(trader@example.com) subscribed to AAPL
✓ SMSAlert(+1234567890) subscribed to AAPL
✓ TradingBot(bot_1) subscribed to AAPL

============================================================
📊 AAPL (Apple Inc): $150.00 → $148.50 (-0.67%)
  📱 Mobile App (User user_123): AAPL now at $148.50
  📱 Mobile App (User user_456): AAPL now at $148.50
  💻 Web Dashboard (dashboard_1): AAPL updated → $148.50
  📧 Email Alert: Sent to trader@example.com - AAPL price update
  📱 SMS Alert: Sent to +1234567890 - AAPL price change
  🤖 Trading Bot (bot_1): AUTO BUY AAPL at $148.50!
============================================================
...
```

**Where It's Used**:

- Stock exchanges (NSE, BSE)
- Real-time notification systems
- Event streaming (Kafka, Redis)
- React/Vue.js (state management)

---

### Example 2: Order Status Notifications (E-commerce)

```python
# Scenario: Flipkart/Amazon order status changes
# Notify: Customer, Seller, Warehouse, Logistics Partner, Analytics

from enum import Enum
from typing import List

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PACKED = "packed"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order:
    """Subject - maintains order state"""
    def __init__(self, order_id: str, customer_id: str, amount: float):
        self.order_id = order_id
        self.customer_id = customer_id
        self.amount = amount
        self._status = OrderStatus.PENDING
        self._observers: List['OrderObserver'] = []
    
    def attach(self, observer: 'OrderObserver'):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: 'OrderObserver'):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status: OrderStatus):
        if new_status != self._status:
            self._status = new_status
            print(f"\n[ORDER {self.order_id}] Status: {self._status.value.upper()}")
            self.notify()

# Observers
class CustomerObserver:
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
    
    def update(self, order: Order):
        status_messages = {
            OrderStatus.CONFIRMED: "Your order is confirmed!",
            OrderStatus.PACKED: "Your order has been packed and will ship soon.",
            OrderStatus.SHIPPED: "Your order is on the way!",
            OrderStatus.DELIVERED: "Your order has been delivered. Enjoy!",
            OrderStatus.CANCELLED: "Your order has been cancelled."
        }
        message = status_messages.get(order.status, "Order status updated")
        print(f"  📧 Customer ({self.customer_id}): {message}")

class SellerObserver:
    def __init__(self, seller_id: str):
        self.seller_id = seller_id
    
    def update(self, order: Order):
        if order.status == OrderStatus.CONFIRMED:
            print(f"  🏪 Seller ({self.seller_id}): Prepare item for order {order.order_id}")
        elif order.status == OrderStatus.SHIPPED:
            print(f"  🏪 Seller ({self.seller_id}): Item shipped for order {order.order_id}")

class WarehouseObserver:
    def __init__(self, warehouse_id: str):
        self.warehouse_id = warehouse_id
    
    def update(self, order: Order):
        if order.status == OrderStatus.CONFIRMED:
            print(f"  📦 Warehouse ({self.warehouse_id}): Pick and pack order {order.order_id}")
        elif order.status == OrderStatus.PACKED:
            print(f"  📦 Warehouse ({self.warehouse_id}): Order {order.order_id} ready for shipment")

class LogisticsObserver:
    def __init__(self, logistics_id: str):
        self.logistics_id = logistics_id
    
    def update(self, order: Order):
        if order.status == OrderStatus.SHIPPED:
            print(f"  🚚 Logistics ({self.logistics_id}): Picked up order {order.order_id}")
        elif order.status == OrderStatus.IN_TRANSIT:
            print(f"  🚚 Logistics ({self.logistics_id}): Order {order.order_id} in transit")

class AnalyticsObserver:
    def __init__(self):
        self.order_count = 0
        self.status_counts = {status: 0 for status in OrderStatus}
    
    def update(self, order: Order):
        self.status_counts[order.status] += 1
        print(f"  📊 Analytics: Order {order.order_id} → {order.status.value} (Total: {sum(self.status_counts.values())})")

# Usage
if __name__ == '__main__':
    order = Order('ORD-123456', 'CUST-789', 2999.99)
    
    # Attach observers
    customer = CustomerObserver('CUST-789')
    seller = SellerObserver('SELL-001')
    warehouse = WarehouseObserver('WH-001')
    logistics = LogisticsObserver('LOG-001')
    analytics = AnalyticsObserver()
    
    order.attach(customer)
    order.attach(seller)
    order.attach(warehouse)
    order.attach(logistics)
    order.attach(analytics)
    
    # Simulate order lifecycle
    order.status = OrderStatus.CONFIRMED
    order.status = OrderStatus.PACKED
    order.status = OrderStatus.SHIPPED
    order.status = OrderStatus.IN_TRANSIT
    order.status = OrderStatus.DELIVERED
```

**Where It's Used**:

- E-commerce (order tracking)
- Notification systems
- Workflow automation
- Event sourcing

---

## 3. STRUCTURE

```
Subject (Stock, Order)
  ↓ notify()
  ↓ attach(observer)
  ↓ detach(observer)
  
Observer Interface
  ↑ implements
  
ConcreteObserverA (Mobile, Email, SMS)
ConcreteObserverB (Web, Bot)
ConcreteObserverC (Analytics)
```

---

## 4. PRODUCTION IMPLEMENTATION WITH ERROR HANDLING

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from threading import Lock
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherStation:
    """Subject - manages weather data"""
    def __init__(self, location: str):
        self.location = location
        self._observers: List['WeatherObserver'] = []
        self._lock = Lock()
        self._temperature = 0
        self._humidity = 0
        self._wind_speed = 0
    
    def attach(self, observer: 'WeatherObserver') -> bool:
        """Thread-safe attach"""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
                logger.info(f"Observer attached: {observer}")
                return True
            return False
    
    def detach(self, observer: 'WeatherObserver') -> bool:
        """Thread-safe detach"""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                logger.info(f"Observer detached: {observer}")
                return True
            return False
    
    def notify_observers(self):
        """Thread-safe notify"""
        with self._lock:
            observers_copy = self._observers.copy()
        
        for observer in observers_copy:
            try:
                observer.update(self.get_state())
            except Exception as e:
                logger.error(f"Error notifying observer {observer}: {e}")
    
    def set_weather_data(self, temp: float, humidity: float, wind: float):
        """Update weather data and notify"""
        self._temperature = temp
        self._humidity = humidity
        self._wind_speed = wind
        self.notify_observers()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return {
            'location': self.location,
            'temperature': self._temperature,
            'humidity': self._humidity,
            'wind_speed': self._wind_speed
        }

class WeatherObserver(ABC):
    @abstractmethod
    def update(self, state: Dict[str, Any]):
        pass

class DisplayObserver(WeatherObserver):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, state: Dict[str, Any]):
        print(f"[{self.name}] {state['location']}: "
              f"{state['temperature']}°C, {state['humidity']}% humidity")

class AlertObserver(WeatherObserver):
    def __init__(self, alert_threshold: float = 35):
        self.threshold = alert_threshold
    
    def update(self, state: Dict[str, Any]):
        if state['temperature'] > self.threshold:
            print(f"⚠️  HEAT ALERT: {state['location']} is {state['temperature']}°C")

# Usage
station = WeatherStation('Delhi')
display1 = DisplayObserver('Dashboard')
display2 = DisplayObserver('Mobile App')
alert = AlertObserver(35)

station.attach(display1)
station.attach(display2)
station.attach(alert)

station.set_weather_data(38.5, 65, 15)
```

---

## 5. INTERVIEW QUESTIONS

### Q1: "Observer vs Pub/Sub - What's the difference?"

**Answer**:

```python
# Observer: Direct coupling (Subject knows Observers)
class Subject:
    def __init__(self):
        self.observers = []  # Stores references
    
    def notify(self):
        for obs in self.observers:  # Direct calls
            obs.update()

# Pub/Sub: Decoupled via Message Broker
class Publisher:
    def publish(self, event):
        message_broker.publish('stock_price_changed', event)

class Subscriber:
    def __init__(self):
        message_broker.subscribe('stock_price_changed', self.handle)

# Difference:
# Observer: Tight coupling, fast, works well for small systems
# Pub/Sub: Loose coupling, asynchronous, scales better, needs message broker
```

---

### Q2: "How do you handle observer exceptions?"

**Answer**:

```python
def notify_observers(self):
    for observer in self.observers:
        try:
            observer.update(self)
        except Exception as e:
            logger.error(f"Observer {observer} failed: {e}")
            # Decide: Remove observer or continue?
            # Usually: Log and continue
            pass
```

---

### Q3: "Design a real-time notification system"

**Expected Answer**:

```python
class NotificationCenter:
    """Manages subscriptions and notifications"""
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)
    
    def post(self, event_type: str, data: Any):
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    logger.error(f"Handler failed: {e}")

# Usage
center = NotificationCenter()
center.subscribe('user_login', lambda data: print(f"User {data['id']} logged in"))
center.post('user_login', {'id': '123', 'timestamp': datetime.now()})
```

---

## 6. OBSERVER vs STRATEGY (Comparison)


| Aspect           | Observer                  | Strategy                 |
| ---------------- | ------------------------- | ------------------------ |
| **Purpose**      | Notify many objects       | Select one algorithm     |
| **When**         | State changes             | Behavior selection       |
| **Relationship** | One-to-many               | One object uses one      |
| **Change**       | Subject state → notify    | Client switches behavior |
| **Example**      | Stock price → all viewers | Sort algorithm selection |


---

## 7. COMMON MISTAKES

### Mistake 1: Observer holding reference to Subject (circular)

```python
# WRONG: Observer holds Subject
class BadObserver:
    def __init__(self, subject):
        self.subject = subject  # Circular reference!

# RIGHT: Observer accesses Subject via update() parameter
class GoodObserver:
    def update(self, subject):
        print(subject.state)
```

---

### Mistake 2: Not handling exceptions in notify loop

```python
# WRONG: One exception breaks all notifications
def notify(self):
    for obs in self.observers:
        obs.update()  # Exception here stops others

# RIGHT: Continue despite failures
def notify(self):
    for obs in self.observers:
        try:
            obs.update()
        except Exception as e:
            logger.error(f"Observer failed: {e}")
```

---

### Mistake 3: Observer modifying Subject during notification

```python
# WRONG: Causes issues
def update(self, subject):
    subject.attach(NewObserver())  # Modifying while iterating!

# RIGHT: Queue changes
def update(self, subject):
    # Just read state, don't modify subject
    print(subject.state)
```

---

## 8. KEY POINTS TO REMEMBER

**Definition** (30 seconds):

> "Observer pattern defines a one-to-many dependency where when one object changes state, all dependents are notified automatically. It decouples the subject from observers, allowing dynamic subscription/unsubscription. Observers don't need to know about each other."

**When to use**:

- Multiple objects need state change notifications
- Want loose coupling
- Objects don't know how many observers exist
- Event-driven systems

**Real-world**: Stock prices, email subscriptions, UI updates, event systems

---

## 9. NEXT PATTERN

Once you master Observer, move to **Decorator Pattern** because:

- Decorator adds behavior like Observer notifies
- Different approach: modification vs notification
- Very practical in real systems
- Common interview pattern

