'''
Strategy pattern is a behaviourl pattern that decides which behaviour to execute at the runtime.
If we need to perform different operations or apply different algorithms based on the situation, we can use the strategy pattern.

Factory and strategy pattern can go hand in hand

Example:
- Sorting algorithm
- Payment gateway
- Shipping method
- Authentication method
- etc.
'''

class NotifificationStrategy:
    def send_notification(self, message):
        pass

class EmailNotificationStrategy(NotifificationStrategy):
    def send_notification(self, message):
        print(f"Sending email notification: {message}")

class SMSNotificationStrategy(NotifificationStrategy):
    def send_notification(self, message):
        print(f"Sending SMS notification: {message}")

class PushNotificationStrategy(NotifificationStrategy):
    def send_notification(self, message):
        print(f"Sending push notification: {message}")

class NotificationFactory:
    def get_strategy(self, strategy_type):
        if(strategy_type == "email"):
            return EmailNotificationStrategy()
        elif(strategy_type == "sms"):
            return SMSNotificationStrategy()
        elif(strategy_type == "push"):
            return PushNotificationStrategy()
        else:
            raise ValueError(f"Invalid strategy type: {strategy_type}")

class NotificationService:
    def __init__(self, strategy: NotifificationStrategy) -> None:
        self.strategy = strategy

    def send_notification(self, message):
        self.strategy.send_notification(message)


if __name__ == "__main__":
    strategy = NotificationFactory().get_strategy("email")
    notification_service = NotificationService(strategy)
    notification_service.send_notification("Hello, how are you?")
        
