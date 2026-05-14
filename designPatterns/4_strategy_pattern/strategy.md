# PATTERN #3: STRATEGY PATTERN
## Complete Interview-Ready Guide

---

## 1. DEFINITION & INTENT

### What Problem Does It Solve?
- Multiple algorithms for same task with different tradeoffs
- Algorithm should be selected at runtime based on conditions
- Want to avoid long if-else chains or switch statements
- Need to swap algorithms without modifying client code

### Real-World Analogy (2-3 lines)
**Different routes to reach destination**: Google Maps has multiple algorithms (Fastest, Shortest, Avoid Highways). You choose one at runtime. The navigation logic stays same, only the route-finding strategy changes. Your car doesn't care which strategy is used—it just drives.

### When TO Use
✓ Multiple algorithms for same problem
✓ Algorithm selection based on runtime conditions
✓ Avoiding long conditional chains
✓ Need to switch behavior dynamically
✓ Each algorithm should be independent

### When NOT to Use
✗ Single, fixed algorithm
✗ Simple if-else condition (overhead not worth it)
✗ Algorithm is unlikely to change
✗ Very few possible strategies (2-3)

---

## 2. REAL-WORLD EXAMPLES

### Example 1: Sorting Strategies in E-commerce (Product Listing)
```python
# Scenario: Flipkart/Amazon product listing needs different sorting strategies
# Price ascending/descending, Popularity, Ratings, Newest, Discount percentage

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    rating: float
    popularity_score: int
    discount_percent: float
    date_added: str
    
    def __repr__(self):
        return f"{self.name}(${self.price}, ⭐{self.rating}, {self.discount_percent}% off)"

# Abstract Strategy
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, products: List[Product]) -> List[Product]:
        """Sort and return products"""
        pass
    
    def get_sort_key(self, product: Product):
        """Get the key to sort by - override in subclass"""
        pass

# Concrete Strategies
class PriceAscendingStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.price)

class PriceDescendingStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.price, reverse=True)

class RatingStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.rating, reverse=True)

class PopularityStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.popularity_score, reverse=True)

class DiscountStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.discount_percent, reverse=True)

class NewestStrategy(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda p: p.date_added, reverse=True)

# Context - Uses Strategy
class ProductListing:
    def __init__(self, products: List[Product], strategy: SortingStrategy = None):
        self.products = products
        self.strategy = strategy or PriceAscendingStrategy()
    
    def set_sorting_strategy(self, strategy: SortingStrategy):
        """Change strategy at runtime"""
        self.strategy = strategy
    
    def get_sorted_products(self) -> List[Product]:
        """Get products sorted by current strategy"""
        return self.strategy.sort(self.products)
    
    def display(self):
        """Display sorted products"""
        for product in self.get_sorted_products():
            print(product)

# Factory for strategies
class SortingStrategyFactory:
    _strategies = {
        'price_asc': PriceAscendingStrategy,
        'price_desc': PriceDescendingStrategy,
        'rating': RatingStrategy,
        'popularity': PopularityStrategy,
        'discount': DiscountStrategy,
        'newest': NewestStrategy
    }
    
    @staticmethod
    def create(sort_type: str) -> SortingStrategy:
        if sort_type not in SortingStrategyFactory._strategies:
            raise ValueError(f"Unknown sorting strategy: {sort_type}")
        return SortingStrategyFactory._strategies[sort_type]()

# Usage
if __name__ == '__main__':
    products = [
        Product("Laptop", 1000, 4.5, 100, 15, "2024-01-01"),
        Product("Phone", 500, 4.8, 200, 20, "2024-01-05"),
        Product("Tablet", 300, 4.2, 50, 30, "2024-01-03"),
        Product("Headphones", 100, 4.9, 150, 10, "2024-01-02"),
    ]
    
    listing = ProductListing(products)
    
    # User chooses sorting from dropdown
    print("=== Price Ascending ===")
    listing.set_sorting_strategy(SortingStrategyFactory.create('price_asc'))
    listing.display()
    
    print("\n=== Best Ratings ===")
    listing.set_sorting_strategy(SortingStrategyFactory.create('rating'))
    listing.display()
    
    print("\n=== Maximum Discount ===")
    listing.set_sorting_strategy(SortingStrategyFactory.create('discount'))
    listing.display()
    
    print("\n=== Most Popular ===")
    listing.set_sorting_strategy(SortingStrategyFactory.create('popularity'))
    listing.display()
```

**Output**:
```
=== Price Ascending ===
Headphones($100, ⭐4.9, 10% off)
Tablet($300, ⭐4.2, 30% off)
Phone($500, ⭐4.8, 20% off)
Laptop($1000, ⭐4.5, 15% off)

=== Best Ratings ===
Headphones($100, ⭐4.9, 10% off)
Phone($500, ⭐4.8, 20% off)
Laptop($1000, ⭐4.5, 15% off)
Tablet($300, ⭐4.2, 30% off)

=== Maximum Discount ===
Tablet($300, ⭐4.2, 30% off)
Phone($500, ⭐4.8, 20% off)
Laptop($1000, ⭐4.5, 15% off)
Headphones($100, ⭐4.9, 10% off)

=== Most Popular ===
Phone($500, ⭐4.8, 20% off)
Headphones($100, ⭐4.9, 10% off)
Laptop($1000, ⭐4.5, 15% off)
Tablet($300, ⭐4.2, 30% off)
```

**Where It's Used**:
- E-commerce: Sorting/filtering products
- Analytics: Different aggregation strategies
- Recommendations: Different recommendation algorithms

---

### Example 2: Compression Strategies (File Upload/Storage)
```python
# Scenario: Cloud storage system (like AWS S3) needs different compression
# Store files as is, compress with GZIP, BROTLI, or ZSTD based on settings

import gzip
import io
from abc import ABC, abstractmethod
from enum import Enum

class CompressionLevel(Enum):
    FAST = 1
    BALANCED = 6
    BEST = 9

class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass
    
    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        pass
    
    @abstractmethod
    def get_compression_ratio(self) -> str:
        pass

class NoCompressionStrategy(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return data
    
    def decompress(self, data: bytes) -> bytes:
        return data
    
    def get_compression_ratio(self) -> str:
        return "No compression"

class GZIPCompressionStrategy(CompressionStrategy):
    def __init__(self, level: CompressionLevel = CompressionLevel.BALANCED):
        self.level = level.value
    
    def compress(self, data: bytes) -> bytes:
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=self.level) as f:
            f.write(data)
        return buf.getvalue()
    
    def decompress(self, data: bytes) -> bytes:
        buf = io.BytesIO(data)
        with gzip.GzipFile(fileobj=buf, mode='rb') as f:
            return f.read()
    
    def get_compression_ratio(self) -> str:
        return f"GZIP (level {self.level})"

class BrotliCompressionStrategy(CompressionStrategy):
    """In production, would use brotli library"""
    def compress(self, data: bytes) -> bytes:
        # Simulated - real code would use brotli library
        return b'BROTLI_COMPRESSED:' + data[:20]  # Simulated
    
    def decompress(self, data: bytes) -> bytes:
        return data[18:]  # Simulated
    
    def get_compression_ratio(self) -> str:
        return "Brotli (best compression)"

class StorageManager:
    def __init__(self, compression_strategy: CompressionStrategy = None):
        self.strategy = compression_strategy or NoCompressionStrategy()
    
    def set_compression_strategy(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def upload_file(self, filename: str, data: bytes) -> dict:
        original_size = len(data)
        compressed_data = self.strategy.compress(data)
        compressed_size = len(compressed_data)
        
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        return {
            'filename': filename,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression': self.strategy.get_compression_ratio(),
            'savings': f"{compression_ratio:.1f}%",
            'data': compressed_data
        }
    
    def download_file(self, file_data: bytes) -> bytes:
        return self.strategy.decompress(file_data)

# Usage
if __name__ == '__main__':
    large_text = "Lorem ipsum dolor sit amet, " * 100
    data = large_text.encode('utf-8')
    
    storage = StorageManager()
    
    print("=== No Compression ===")
    result = storage.upload_file('file.txt', data)
    print(f"Size: {result['original_size']} → {result['compressed_size']} bytes")
    print(f"Compression: {result['compression']}")
    print(f"Savings: {result['savings']}")
    
    print("\n=== GZIP Compression (Balanced) ===")
    storage.set_compression_strategy(GZIPCompressionStrategy(CompressionLevel.BALANCED))
    result = storage.upload_file('file.txt', data)
    print(f"Size: {result['original_size']} → {result['compressed_size']} bytes")
    print(f"Compression: {result['compression']}")
    print(f"Savings: {result['savings']}")
    
    print("\n=== GZIP Compression (Best) ===")
    storage.set_compression_strategy(GZIPCompressionStrategy(CompressionLevel.BEST))
    result = storage.upload_file('file.txt', data)
    print(f"Size: {result['original_size']} → {result['compressed_size']} bytes")
    print(f"Compression: {result['compression']}")
    print(f"Savings: {result['savings']}")
```

**Where It's Used**:
- AWS S3: Different compression algorithms
- Google Cloud Storage: Compression strategies
- CDNs: HTTP compression selection

---

## 3. STRUCTURE

```
Client/Context
    ↓ (uses)
Strategy Interface
    ↑ (implements)
ConcreteStrategyA
ConcreteStrategyB
ConcreteStrategyC

Context delegates to Strategy - can switch at runtime
```

---

## 4. COMPLETE PRODUCTION IMPLEMENTATION

```python
from abc import ABC, abstractmethod
from typing import List, Dict
from enum import Enum

# PaymentFraud Detection Strategies
class FraudDetectionStrategy(ABC):
    @abstractmethod
    def detect_fraud(self, transaction: Dict) -> bool:
        pass
    
    @abstractmethod
    def get_risk_score(self, transaction: Dict) -> float:
        """Returns 0.0 to 1.0 risk score"""
        pass

class RulesBasedStrategy(FraudDetectionStrategy):
    """Traditional rule-based fraud detection"""
    def __init__(self):
        self.rules = [
            ('amount_threshold', 10000),
            ('velocity_limit', 5),  # transactions per minute
            ('country_restrictions', ['NK', 'IR', 'SY'])
        ]
    
    def detect_fraud(self, transaction: Dict) -> bool:
        # Rule 1: Check amount
        if transaction['amount'] > self.rules[0][1]:
            return True
        
        # Rule 2: Check velocity
        if transaction.get('velocity', 0) > self.rules[1][1]:
            return True
        
        # Rule 3: Check country
        if transaction['country'] in self.rules[2][1]:
            return True
        
        return False
    
    def get_risk_score(self, transaction: Dict) -> float:
        score = 0.0
        
        # Amount score
        if transaction['amount'] > 5000:
            score += 0.3
        
        # Velocity score
        if transaction.get('velocity', 0) > 3:
            score += 0.2
        
        # Country score
        if transaction['country'] in ['NK', 'IR']:
            score += 0.5
        
        return min(score, 1.0)

class MachineLearningStrategy(FraudDetectionStrategy):
    """ML-based fraud detection"""
    def __init__(self):
        # Simulate ML model
        self.model = None  # In real code: load actual ML model
    
    def detect_fraud(self, transaction: Dict) -> bool:
        risk_score = self.get_risk_score(transaction)
        return risk_score > 0.7
    
    def get_risk_score(self, transaction: Dict) -> float:
        # Simulated ML prediction
        features = [
            transaction['amount'],
            transaction.get('velocity', 0),
            self.country_risk_score(transaction['country']),
            transaction.get('device_age', 100)  # days
        ]
        
        # Simple simulation - real code uses actual model
        normalized_amount = transaction['amount'] / 10000
        velocity_score = transaction.get('velocity', 0) / 10
        device_score = 0.1 if transaction.get('device_age', 100) < 7 else 0.0
        
        return (normalized_amount * 0.5 + velocity_score * 0.3 + device_score * 0.2)
    
    @staticmethod
    def country_risk_score(country: str) -> float:
        high_risk = {'NK': 0.9, 'IR': 0.8, 'SY': 0.8}
        return high_risk.get(country, 0.1)

class HybridStrategy(FraudDetectionStrategy):
    """Combination of rules and ML"""
    def __init__(self, rules_strategy: RulesBasedStrategy, ml_strategy: MachineLearningStrategy):
        self.rules = rules_strategy
        self.ml = ml_strategy
    
    def detect_fraud(self, transaction: Dict) -> bool:
        # If rules catch it, report fraud
        if self.rules.detect_fraud(transaction):
            return True
        
        # Also check ML score
        ml_score = self.ml.get_risk_score(transaction)
        return ml_score > 0.6
    
    def get_risk_score(self, transaction: Dict) -> float:
        rules_score = self.rules.get_risk_score(transaction)
        ml_score = self.ml.get_risk_score(transaction)
        
        # Weighted average
        return rules_score * 0.4 + ml_score * 0.6

# Context
class PaymentProcessor:
    def __init__(self, fraud_strategy: FraudDetectionStrategy):
        self.fraud_strategy = fraud_strategy
        self.transactions = []
    
    def set_fraud_strategy(self, strategy: FraudDetectionStrategy):
        """Switch strategy at runtime"""
        self.fraud_strategy = strategy
    
    def process_payment(self, transaction: Dict) -> Dict:
        # Detect fraud
        is_fraud = self.fraud_strategy.detect_fraud(transaction)
        risk_score = self.fraud_strategy.get_risk_score(transaction)
        
        status = 'REJECTED' if is_fraud else 'APPROVED'
        
        result = {
            'transaction_id': transaction['id'],
            'status': status,
            'risk_score': risk_score,
            'amount': transaction['amount'],
            'timestamp': transaction.get('timestamp', 'N/A')
        }
        
        self.transactions.append(result)
        return result
    
    def get_statistics(self):
        """Get fraud detection statistics"""
        rejected = sum(1 for t in self.transactions if t['status'] == 'REJECTED')
        total = len(self.transactions)
        
        return {
            'total_transactions': total,
            'rejected': rejected,
            'fraud_rate': f"{(rejected/total*100):.1f}%" if total > 0 else "0%"
        }

# Usage Example
if __name__ == '__main__':
    test_transactions = [
        {'id': 'T1', 'amount': 100, 'country': 'US', 'velocity': 1, 'device_age': 30},
        {'id': 'T2', 'amount': 50000, 'country': 'US', 'velocity': 2, 'device_age': 1},
        {'id': 'T3', 'amount': 200, 'country': 'NK', 'velocity': 1, 'device_age': 15},
        {'id': 'T4', 'amount': 5000, 'country': 'IN', 'velocity': 10, 'device_age': 5},
    ]
    
    processor = PaymentProcessor(RulesBasedStrategy())
    
    print("=== Rules-Based Strategy ===")
    for txn in test_transactions:
        result = processor.process_payment(txn)
        print(f"TXN {result['transaction_id']}: ${result['amount']} → {result['status']} (Risk: {result['risk_score']:.2f})")
    
    print(f"\n{processor.get_statistics()}")
    
    # Switch strategy at runtime
    print("\n=== Machine Learning Strategy ===")
    processor.transactions = []  # Reset
    processor.set_fraud_strategy(MachineLearningStrategy())
    
    for txn in test_transactions:
        result = processor.process_payment(txn)
        print(f"TXN {result['transaction_id']}: ${result['amount']} → {result['status']} (Risk: {result['risk_score']:.2f})")
    
    print(f"\n{processor.get_statistics()}")
```

---

## 5. INTERVIEW QUESTIONS

### Q1: "When would you use Strategy vs Template Method?"

**Answer**:
```python
# Strategy: Behavior selection at RUNTIME
strategy = PaymentGatewayFactory.create(user_country)
processor.set_strategy(strategy)

# Template Method: Algorithm STRUCTURE defined, steps customized
class DataProcessor:
    def process(self):  # Template
        self.validate()
        self.transform()  # Subclasses override
        self.save()

# Strategy is more flexible, Template Method is for defining process flow
```

---

### Q2: "Design a caching strategy selector"

**Expected Answer**:
```python
class CachingStrategy(ABC):
    @abstractmethod
    def get(self, key: str): pass
    @abstractmethod
    def set(self, key: str, value): pass

class LRUCacheStrategy(CachingStrategy):
    # Least Recently Used
    pass

class LFUCacheStrategy(CachingStrategy):
    # Least Frequently Used
    pass

class FIFOCacheStrategy(CachingStrategy):
    # First In First Out
    pass

class Cache:
    def __init__(self, strategy: CachingStrategy):
        self.strategy = strategy
    
    def switch_strategy(self, strategy: CachingStrategy):
        self.strategy = strategy
```

---

## 6. KEY COMPARISON: STRATEGY vs FACTORY

| Aspect | Strategy | Factory |
|--------|----------|---------|
| **Focus** | Behavior/Algorithm | Object Creation |
| **When** | Runtime algorithm swap | Create right type |
| **Selection** | Usually config/condition | Type determines it |
| **Example** | Sort algorithm | DB connection type |
| **Inheritance** | Strategies share interface | Products may be unrelated |

---

## 7. COMMON MISTAKES

### Mistake 1: Creating strategies unnecessarily
```python
# WRONG: Strategy for simple if-else
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price): pass

class StudentDiscount(DiscountStrategy):
    def apply(self, price): return price * 0.9

# RIGHT: Just use if-else for simple cases
if user_type == 'student':
    price *= 0.9
```

---

### Mistake 2: Not making strategies stateless
```python
# WRONG: Mutable strategy
class Strategy:
    def __init__(self):
        self.state = None  # Shared across calls!

# RIGHT: Stateless strategy
class Strategy:
    def execute(self, context):
        # No instance variables
        pass
```

---

## 8. KEY POINTS TO REMEMBER

**Definition** (30 seconds):
> "Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it. Use when you have multiple algorithms for same task and want to switch them at runtime without modifying client code."

**When to use**:
- Multiple algorithms
- Switch at runtime
- Avoid long if-else chains

**Real-world usage**: Sorting, Compression, Payment processing, Fraud detection

---

## 9. NEXT PATTERN

Once you master Strategy, move to **Observer Pattern** because:
- Observer is about notification when state changes
- Strategy is about behavior selection
- Both are very common in real systems
- Often used together (strategy pattern with observer pattern)