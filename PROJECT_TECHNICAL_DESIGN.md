\# Service Booking Application — Technical Design



\## 1. Project Overview



The Service Booking Application is a backend system for connecting customers with service providers.



Customers can register, manage their profile, view services, create bookings, and cancel bookings.



Service providers can manage their services and process customer bookings.



The backend is developed using Django and Django REST Framework.



\---



\## 2. User Roles



\### Customer



A customer can:



\* Register and login

\* Manage their profile

\* View available services

\* Create bookings

\* View their bookings

\* Update booking information

\* Cancel eligible bookings



\### Service Provider



A service provider can:



\* Manage their provider profile

\* Create and manage services

\* View bookings for their services

\* Confirm bookings

\* Complete confirmed bookings



\### Admin



The administrator is responsible for managing and monitoring the application.



\---



\## 3. Main Modules



```text

Authentication

User Profile

Service Provider

Services

Search

Booking

Payment

Notifications

Chat

Admin

```



Current implementation includes:



```text

Authentication

User Profile

Service Provider

Services

Booking

```



Other modules will be implemented in later stages.



\---



\## 4. Technology Stack



\### Backend



\* Python

\* Django

\* Django REST Framework



\### Authentication



\* JWT Authentication



\### Database



\* SQLite during development

\* PostgreSQL planned for production



\### API



\* REST API

\* JSON request and response format



\---



\## 5. Application Architecture



```text

Mobile Application

&#x20;       |

&#x20;       | REST API

&#x20;       ↓

Django REST Framework

&#x20;       |

&#x20;       ├── Authentication

&#x20;       ├── Profiles

&#x20;       ├── Providers

&#x20;       ├── Services

&#x20;       └── Bookings

&#x20;       |

&#x20;       ↓

Database

```



\---



\## 6. Database Relationships



```text

User

&#x20;|

&#x20;├── Profile

&#x20;|

&#x20;└── Provider

&#x20;      |

&#x20;      └── Service

&#x20;            |

&#x20;            └── Booking

&#x20;                   |

&#x20;                   └── Customer

```



Important relationships:



\* One User has one Profile.

\* One User can have one Provider profile.

\* One Provider can have many Services.

\* One Customer can have many Bookings.

\* One Service can have many Bookings.



\---



\## 7. Authentication Flow



```text

Customer

&#x20;   |

&#x20;   ↓

Register

&#x20;   |

&#x20;   ↓

Login

&#x20;   |

&#x20;   ↓

JWT Access Token

&#x20;   |

&#x20;   ↓

Protected API

```



Protected API requests use:



```http

Authorization: Bearer <access\_token>

```



\---



\## 8. Booking Lifecycle



A booking starts as:



```text

PENDING

```



A provider can confirm it:



```text

PENDING → CONFIRMED

```



A provider can complete it:



```text

CONFIRMED → COMPLETED

```



A customer can cancel an eligible booking:



```text

PENDING → CANCELLED

CONFIRMED → CANCELLED

```



Invalid transitions are rejected.



\---



\## 9. Current API Endpoints



\### Authentication



```text

POST /api/v1/auth/register/

POST /api/v1/auth/login/

POST /api/v1/auth/refresh/

```



\### Profile



```text

GET   /api/v1/auth/profile/

PATCH /api/v1/auth/profile/

```



\### Services



```text

GET /api/v1/services/

```



\### Bookings



```text

POST  /api/v1/bookings/

GET   /api/v1/bookings/

GET   /api/v1/bookings/{id}/

PATCH /api/v1/bookings/{id}/



POST /api/v1/bookings/{id}/cancel/

POST /api/v1/bookings/{id}/confirm/

POST /api/v1/bookings/{id}/complete/

```



\---



\## 10. Security



The application uses:



\* JWT authentication

\* Authenticated API access

\* Role-based business rules

\* User-specific booking access

\* Provider ownership validation

\* Protected booking status transitions



Customers can only access their own bookings.



Providers can only confirm or complete bookings belonging to their services.



\---



\## 11. Project Structure



```text

service-booking/

│

├── apps/

│   ├── accounts/

│   ├── providers/

│   ├── services/

│   ├── bookings/

│   ├── payments/

│   ├── notifications/

│   ├── chat/

│   └── admin\_panel/

│

├── config/

├── manage.py

├── requirements.txt

└── PROJECT\_TECHNICAL\_DESIGN.md

```



\---



\## 12. Future Modules



The following modules will be implemented next:



```text

Payment

Notifications

Chat

Search

Admin

```



These modules will expose additional REST APIs and integrate with the existing booking workflow.



\---



\## 13. Development Workflow



```text

Requirement Analysis

&#x20;       ↓

Database Design

&#x20;       ↓

API Design

&#x20;       ↓

Django Models

&#x20;       ↓

Serializers

&#x20;       ↓

Views

&#x20;       ↓

URLs

&#x20;       ↓

API Testing

&#x20;       ↓

Business Rules

```



\---



\## 14. Current Project Status



```text

Authentication       ✅

User Profile         ✅

Service Provider     ✅

Services             ✅

Booking              ✅

Payment              ⏳

Notifications        ⏳

Chat                 ⏳

Search               ⏳

Admin                ⏳

```



The core authentication, profile, provider, service, and booking functionality has been implemented and tested.



