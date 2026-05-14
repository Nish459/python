'''
Dependency Inversion Principle (DIP)

Concept -
High-level modules must not depend on low-level modules. Both should depend on abstractions.
Abstractions should not depend on details. Details should depend on abstractions.

Key distinction:
- Dependency INJECTION = passing dependencies from outside (a technique)
- Dependency INVERSION  = depending on abstractions, not concretions (a principle)
  Injection without abstractions is NOT inversion.
'''
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    customer_id: int
    amount: float
    status: str


# ──────────────────────────────────────────────
# BAD: High-level module depends on concrete low-level modules
# ──────────────────────────────────────────────

class MySQLOrderRepository:
    def get_order(self, order_id: int) -> Order:
        return Order(order_id=order_id, customer_id=1, amount=100.0, status="pending")


class SMTPEmailService:
    def send_email(self, customer_id: int, message: str) -> None:
        print(f"[SMTP] Sending to customer {customer_id}: {message}")


class OrderServiceBad:
    """Violates DIP: tightly coupled to MySQL and SMTP implementations."""

    def __init__(self):
        self.repo = MySQLOrderRepository()          # hardcoded concrete class
        self.notifier = SMTPEmailService()           # hardcoded concrete class

    def process_order(self, order_id: int) -> Order:
        order = self.repo.get_order(order_id)
        self.notifier.send_email(order.customer_id, f"Order {order.order_id} confirmed")
        return order


# ──────────────────────────────────────────────
# GOOD: Both high-level and low-level modules depend on abstractions
# ──────────────────────────────────────────────

class OrderRepositoryABC(ABC):
    """Abstraction for order persistence."""

    @abstractmethod
    def get_order(self, order_id: int) -> Order: ...


class NotificationServiceABC(ABC):
    """Abstraction for sending notifications (email, SMS, push, etc.)."""

    @abstractmethod
    def notify(self, customer_id: int, message: str) -> None: ...


# --- Low-level modules implement the abstractions ---

class PostgresOrderRepository(OrderRepositoryABC):
    def get_order(self, order_id: int) -> Order:
        return Order(order_id=order_id, customer_id=1, amount=250.0, status="pending")


class SendGridEmailService(NotificationServiceABC):
    def notify(self, customer_id: int, message: str) -> None:
        print(f"[SendGrid] Email to customer {customer_id}: {message}")


class TwilioSMSService(NotificationServiceABC):
    def notify(self, customer_id: int, message: str) -> None:
        print(f"[Twilio] SMS to customer {customer_id}: {message}")


# --- High-level module depends ONLY on abstractions ---

class OrderService:
    """Follows DIP: depends on abstractions, not concrete implementations."""

    def __init__(self, repo: OrderRepositoryABC, notifier: NotificationServiceABC):
        self.repo = repo
        self.notifier = notifier

    def process_order(self, order_id: int) -> Order:
        order = self.repo.get_order(order_id)
        self.notifier.notify(order.customer_id, f"Order {order.order_id} confirmed")
        return order


if __name__ == "__main__":
    print("=== BAD (violates DIP) ===")
    bad_service = OrderServiceBad()
    print(bad_service.process_order(1))

    print("\n=== GOOD (follows DIP) — with email ===")
    email_service = OrderService(PostgresOrderRepository(), SendGridEmailService())
    print(email_service.process_order(2))

    print("\n=== GOOD (follows DIP) — swapped to SMS, zero code changes ===")
    sms_service = OrderService(PostgresOrderRepository(), TwilioSMSService())
    print(sms_service.process_order(3))
