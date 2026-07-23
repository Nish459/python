Functional Requirements - 
- System must process the entry of the vehicle properly:
    - It is suppose to search the available empty spot as per the category.
    - genreate the ticket for the vehicle
    - mark the spot as occupied.
- System must process the exit in the following steps:
    - ticket must be validated.
    - fee must be calculated as per the pricing strategy
    - payment must be processed before exit
    - system must make sure there are no double payemnts
    - spot must be marked as available as soon as the exit is completed

Non-Functional Requirements - 
- Performance: system must be capable of handling multiple requests with minimal latency.
- Concurrency: two vehicles must not be assigned a single spot.
- Extensibility: adding new pricing or payment methods must not require to change the existing classes
- Scalability: system must be able to handle multiple floors and spot efficiently
- Security: unauthorized spot releases must be prevented, transaction data must be secured

Add ons -
- Concurrency, multiple floors, vehicle must move to wait queue if no spot available


For concurreny - 
    - Apply locks on the components that reads then write.
    - In the real system the locks will be applied on the data layer not the application layer
    as in case of horizontal scaling application layer locks doesn't work.
    - so we will use the row locking on the database.
    