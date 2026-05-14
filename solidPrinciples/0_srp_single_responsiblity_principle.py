"""
Single Responsibility Principle (SRP)

A class should have only single responsibility, that is it should have only one reason to change.
If a class has more than one responsibility, it should be split into multiple classes.
"""

# --- BAD: Violates SRP ---
# This User class has THREE reasons to change:
# 1. User data changes  2. DB logic changes  3. Email logic changes

class UserBad:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def get_user_details(self) -> str:
        return f"Name: {self.name}, Age: {self.age}"

    def save_user_to_database(self) -> None:
        print(f"Saving user {self.name} to database")

    def send_welcome_email(self) -> None:
        print(f"Sending welcome email to {self.name}")


# --- GOOD: Follows SRP ---
# Each class has exactly ONE reason to change.

class User:
    """Only responsible for holding user data."""
    def __init__(self, name: str, age: int, email: str) -> None:
        self.name = name
        self.age = age
        self.email = email

    def get_user_details(self) -> str:
        return f"Name: {self.name}, Age: {self.age}, Email: {self.email}"


class EmailService:
    """Only responsible for sending emails."""
    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"Sending email to {to} with subject '{subject}' and body '{body}'")


class DatabaseService:
    """Only responsible for database operations."""
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def connect(self) -> None:
        print(f"Connecting to database {self.connection_string}")

    def disconnect(self) -> None:
        print(f"Disconnecting from database {self.connection_string}")

    def execute_query(self, query: str) -> None:
        print(f"Executing query: {query}")


class UserService:
    """Orchestrates user creation by delegating to the right services."""
    def __init__(self, email_service: EmailService, database_service: DatabaseService) -> None:
        self.email_service = email_service
        self.database_service = database_service

    def create_user(self, user: User) -> None:
        self.database_service.execute_query(
            f"INSERT INTO users (name, age) VALUES ('{user.name}', {user.age})"
        )
        self.email_service.send_email(
            user.email, "Welcome!", f"Hi {user.name}, welcome to the platform"
        )


if __name__ == "__main__":
    print("=== BAD: SRP Violation ===")
    bad_user = UserBad("John Doe", 25)
    bad_user.save_user_to_database()
    bad_user.send_welcome_email()

    print("\n=== GOOD: Following SRP ===")
    user = User("John Doe", 25, "john.doe@example.com")
    email_service = EmailService()
    database_service = DatabaseService("sqlite:////tmp/test.db")
    user_service = UserService(email_service, database_service)
    user_service.create_user(user)