'''
Interface Segregation Principle (ISP)

Concept - 
It states that instead of having a one fat client interface we must have multiple small interfaces.
We should not force a client to implement the functionality it does not need.

It resolves the issue of having a one fat client interface that forces a client to implement the functionality it does not need.

Real-world example?
In a payment system, don't have one PaymentProcessor interface with chargeCard(), sendInvoice(), 
processRefund(). A refund-only service shouldn't need to know about invoicing. 
Split them into Chargeable, Invoiceable, Refundable.

first explain the concept, then problem then fix and then real-world example.
'''

from abc import abstractmethod, ABC


class PrinterBad(ABC):
    @abstractmethod
    def print(self, document: str) -> None:
        pass
    @abstractmethod
    def scan(self, document: str) -> None:
        pass
    @abstractmethod
    def fax(self, document:str) -> None:
        pass

class ScannerBad(PrinterBad):
    def print(self, document: str) -> None:
        raise NotImplementedError("Printer cannot scan")
    def fax(self, document: str) -> None:
        raise NotImplementedError("Printer cannot fax")
    def scan(self, document: str) -> str:
        return "Scanner can scan"

class Printer(ABC):
    @abstractmethod
    def print(self, document: str) -> None:
        pass

class Scanner(ABC):
    @abstractmethod
    def scan(self, document: str) -> None:
        pass

class Fax(ABC):
    @abstractmethod
    def fax(self, document: str) -> None:
        pass

class PrinterScanner(Printer, Scanner):
    def print(self, document: str) -> None:
        pass
    def scan(self, document: str) -> None:
        pass

class PrinterFax(Printer, Fax):
    def print(self, document: str) -> None:
        pass
    def fax(self, document: str) -> None:
        pass

class ScannerFax(Scanner, Fax):
    def scan(self, document: str) -> None:
        pass
    def fax(self, document: str) -> None:
        pass


if __name__ == "__main__":
    printer_scanner = PrinterScanner()
    printer_fax = PrinterFax()
    scanner_fax = ScannerFax()
    printer_scanner.print("Hello, world!")
    printer_scanner.scan("Hello, world!")
    printer_fax.print("Hello, world!")
    printer_fax.fax("Hello, world!")