# Exercise 2: Logger with Log Levels

import threading
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class Logger:
    # TODO: Implement as singleton (thread-safe)
    # - Single instance across application
    # - Support DEBUG, INFO, WARN, ERROR log levels
    # - Write to both console and file (app.log)
    # - Thread-safe logging from multiple threads
    
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

        self._initialized = True
        self.log_level = LogLevel.INFO
        self.log_buffer = []
        self.file_handle = open("app.log", "a")
        self.buffer_size = 100

    def set_level(self, level: LogLevel):
        self.log_level = level

    def debug(self, message):
        self._log(LogLevel.DEBUG, message)
    

    def info(self, message):
        self._log(LogLevel.INFO, message)

    def warn(self, message):
        self._log(LogLevel.WARN, message)

    def error(self, message):
        self._log(LogLevel.ERROR, message)

    def _log(self, level, message):
        if level.value < self.log_level.value:
            return
        with self._buffer_lock:
            log_entry = f"[{datetime.now().isoformat()}] [{level.name}] {message}"
            self.log_buffer.append(log_entry)
            print(log_entry)
            if len(self.log_buffer) >= self.buffer_size:
                self._flush()

    def _flush(self):
        with self._buffer_lock:
            for entry in self.log_buffer:
                self.file_handle.write(entry + "\n")
            self.log_buffer.clear()

    def shutdown(self):
        with self._buffer_lock:
            self._flush()
            if self.file_handle:
                self.file_handle.close()

    def __del__(self):
        self.shutdown()

if __name__ == "__main__":
    # Test 1: Verify singleton
    logger1 = Logger()
    logger2 = Logger()
    print(f"Same instance: {logger1 is logger2}")  # Expected: True
    
    # Test 2: Set log level and test filtering
    logger1.set_level(LogLevel.INFO)
    logger1.debug("Debug message")  # Should NOT appear
    logger1.info("Info message")    # Should appear
    logger1.warn("Warn message")    # Should appear
    logger1.error("Error message")  # Should appear
    
    # Test 3: Verify logs written to file
    print("Check app.log for file output")
    
    # Test 4: Thread safety
    print("\nTesting concurrent logging:")
    
    def worker(thread_id):
        for i in range(3):
            logger1.info(f"Thread {thread_id} - Message {i}")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("All threads completed")
    
    # Expected Output:
    # Same instance: True
    # [2024-04-29 10:30:45.123] INFO - Info message
    # [2024-04-29 10:30:45.124] WARN - Warn message
    # [2024-04-29 10:30:45.125] ERROR - Error message
    # Testing concurrent logging:
    # [2024-04-29 10:30:45.126] INFO - Thread 0 - Message 0
    # [2024-04-29 10:30:45.127] INFO - Thread 1 - Message 0
    # [2024-04-29 10:30:45.128] INFO - Thread 2 - Message 0
    # ... (more messages from concurrent threads)
    # All threads completed