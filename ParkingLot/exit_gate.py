from ticket import Ticket
from fee_calculator import FeeCalculator
from gate import Gate
from datetime import datetime
from common_enum import PaymentStatus, PaymentMethod
from payment_processor import PaymentProcessorFactory

class ExitGate(Gate):

    def exit(self, ticket: Ticket, payment_method: PaymentMethod, fee_calculator: FeeCalculator) -> bool:
        if ticket.status != PaymentStatus.PENDING:
            raise Exception("Ticket is not pending")

        ticket.exit_time = datetime.now()
        duration = datetime.now() - ticket.entry_time
        fee = fee_calculator.calculate_fee(duration.total_seconds() / 3600)
        payment_processor = PaymentProcessorFactory().get_payment_processor(payment_method)
        success = payment_processor.process_payment(fee)
        if success:
            ticket.status = PaymentStatus.PAID
            return True
        else:
            ticket.status = PaymentStatus.FAILED
            raise Exception("Payment failed")
