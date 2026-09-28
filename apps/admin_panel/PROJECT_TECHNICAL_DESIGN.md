
# Project Technical Design

## 1. Database Design

### Entities

1. User
2. Profile
3. Service
4. Booking
5. Payment
6. Notification
7. Conversation
8. Message

### User

- id
- email
- password
- role
- is_active
- created_at
- updated_at

### Profile

- id
- user
- full_name
- phone
- address
- city
- profile_image
- created_at
- updated_at

### Service

- id
- provider
- name
- description
- price
- duration
- is_available
- created_at
- updated_at

### Booking

- id
- customer
- service
- provider
- booking_date
- booking_time
- status
- total_amount
- created_at
- updated_at

### Payment

- id
- booking
- amount
- payment_method
- transaction_id
- status
- paid_at
- created_at

### Notification

- id
- user
- title
- message
- notification_type
- is_read
- created_at

### Conversation

- id
- customer
- provider
- booking
- created_at
- updated_at

### Message

- id
- conversation
- sender
- message
- is_read
- created_at
