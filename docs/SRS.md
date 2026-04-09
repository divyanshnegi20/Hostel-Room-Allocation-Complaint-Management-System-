# Software Requirements Specification (SRS)
## Hostel Room Allocation & Complaint Management System

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the **HostelHub** — a web-based Hostel Room Allocation & Complaint Management System designed to streamline hostel/PG operations including student registration, room allocation, fee tracking, complaint management, and visitor logging.

### 1.2 Scope
The system covers:
- Student Registration & Authentication
- Room/Bed Availability & Allocation
- Fee Management with Mock Payment Gateway
- Complaint / Maintenance Request Tracking
- Visitor Log
- Admin Dashboard & Reports

### 1.3 Definitions & Acronyms
| Term | Definition |
|------|-----------|
| PG | Paying Guest |
| CRUD | Create, Read, Update, Delete |
| Admin | System administrator with full access |
| Warden | Hostel warden with management rights |

### 1.4 Technology Stack
| Component | Technology |
|-----------|-----------|
| Backend | Python 3.13, Django 6.x |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite (development) / MySQL (production) |
| PDF Generation | xhtml2pdf |
| Charts | Chart.js |

---

## 2. Overall Description

### 2.1 Product Perspective
HostelHub is a standalone web application accessible through any modern web browser. It replaces manual processes for hostel room management, fee collection, and complaint handling.

### 2.2 User Classes
| User Role | Description |
|-----------|-------------|
| **Student** | Can register, view room allocation, pay fees, submit complaints, log visitors |
| **Warden** | Can manage rooms, allocate beds, update complaint status, view reports |
| **Admin** | Full system access including user management, data export, and analytics |

### 2.3 Operating Environment
- Server: Any machine running Python 3.10+
- Client: Modern web browser (Chrome, Firefox, Edge, Safari)
- Responsive design supports desktop, tablet, and mobile

---

## 3. Functional Requirements

### FR-01: Student Registration & Authentication
| ID | Requirement |
|----|-------------|
| FR-01.1 | System shall allow students to self-register with username, email, phone, and password |
| FR-01.2 | System shall validate email format and password strength |
| FR-01.3 | System shall support login/logout functionality |
| FR-01.4 | System shall maintain user profiles with editable fields |
| FR-01.5 | System shall support three roles: Student, Warden, Admin |

### FR-02: Room/Bed Management
| ID | Requirement |
|----|-------------|
| FR-02.1 | Admin shall be able to create rooms with type, floor, beds, AC status, and rent |
| FR-02.2 | System shall auto-create bed records when a room is created |
| FR-02.3 | Students shall see room availability as a color-coded grid |
| FR-02.4 | Admin shall allocate/deallocate beds to/from students |
| FR-02.5 | Bed status shall auto-update on allocation/deallocation |
| FR-02.6 | Students shall view their current room, bed, and roommate details |
| FR-02.7 | System shall support room filtering by floor, type, and availability |

### FR-03: Fee Management
| ID | Requirement |
|----|-------------|
| FR-03.1 | System shall define fee structures per room type and AC status |
| FR-03.2 | Students shall view their dues and payment history |
| FR-03.3 | System shall provide a mock payment gateway with simulated success/failure |
| FR-03.4 | System shall generate unique receipt and transaction IDs |
| FR-03.5 | Students shall download PDF receipts for paid transactions |
| FR-03.6 | Admin shall view all payments with search and filter options |

### FR-04: Complaint / Maintenance Request
| ID | Requirement |
|----|-------------|
| FR-04.1 | Students shall submit complaints with category, priority, subject, and description |
| FR-04.2 | System shall track complaint status: Open → In Progress → Resolved → Closed |
| FR-04.3 | Admin/Warden shall update complaint status and add resolution notes |
| FR-04.4 | Students shall view their complaint history with timestamps |
| FR-04.5 | System shall support filtering by status and category |

### FR-05: Visitor Log
| ID | Requirement |
|----|-------------|
| FR-05.1 | System shall log visitor entries with name, phone, relation, and purpose |
| FR-05.2 | System shall record check-in and check-out timestamps |
| FR-05.3 | Admin shall search and view all visitor records |

### FR-06: Admin Dashboard & Reports
| ID | Requirement |
|----|-------------|
| FR-06.1 | Dashboard shall display summary cards (students, rooms, occupancy, fees, complaints) |
| FR-06.2 | Dashboard shall render interactive charts (complaint categories, status overview) |
| FR-06.3 | Admin shall export data as CSV (students, payments, complaints) |
| FR-06.4 | Dashboard shall show recent activity (allocations, complaints, visitors) |

---

## 4. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | **Performance**: Pages shall load within 3 seconds on standard connections |
| NFR-02 | **Security**: Passwords shall be hashed; CSRF protection on all forms |
| NFR-03 | **Usability**: Responsive design for mobile, tablet, and desktop |
| NFR-04 | **Reliability**: System shall handle concurrent users without data corruption |
| NFR-05 | **Maintainability**: Modular Django app architecture with separate apps per feature |
| NFR-06 | **Scalability**: Database-agnostic ORM supports migration to MySQL/PostgreSQL |

---

## 5. System Architecture

```
┌─────────────────────────────────────────────┐
│                  Client (Browser)             │
│         HTML5 / CSS3 / Bootstrap 5            │
│              JavaScript / Chart.js            │
└──────────────────┬──────────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────────┐
│              Django Web Server                │
│  ┌─────────┬──────────┬────────────────┐     │
│  │Accounts │  Rooms   │    Fees       │     │
│  ├─────────┼──────────┼────────────────┤     │
│  │Complaints│ Visitors │  Dashboard    │     │
│  └─────────┴──────────┴────────────────┘     │
│              Django ORM                       │
└──────────────────┬──────────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────────┐
│          SQLite / MySQL Database              │
└─────────────────────────────────────────────┘
```

---

## 6. Constraints
- Payment is simulated (mock gateway) — no real payment integration
- No email notification system
- Single-tenant design (single hostel/PG)

---

## 7. Approval
| Role | Name | Date |
|------|------|------|
| Student Developer | | |
| Faculty Advisor | | |
