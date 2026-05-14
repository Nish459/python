# Adapter Pattern

class OldPaymentGateway():
    def make_payment(self, amount):
        pass

class Adapter():
    def __init__(self, old_payment_gateway):
        self.old_payment_gateway = old_payment_gateway

    def pay(self, amount):
        self.old_payment_gateway.make_payment(amount)

# Usage - 
adapter = Adapter(OldPaymentGateway())
adapter.pay(500)
