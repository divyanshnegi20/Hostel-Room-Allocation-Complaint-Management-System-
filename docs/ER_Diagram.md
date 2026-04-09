# ER Diagram
## Hostel Room Allocation & Complaint Management System

```mermaid
erDiagram
    CUSTOMUSER {
        int id PK
        string username UK
        string email
        string password
        string first_name
        string last_name
        string role "student/admin/warden"
        string phone
        string parent_phone
        string address
        string institution
        datetime date_joined
        boolean is_active
    }

    ROOM {
        int id PK
        string room_number UK
        int floor
        string room_type "single/double/triple/dormitory"
        int total_beds
        boolean is_ac
        decimal monthly_rent
        string description
        datetime created_at
    }

    BED {
        int id PK
        int room_id FK
        string bed_label "A/B/C"
        string status "available/occupied/maintenance"
    }

    ALLOCATION {
        int id PK
        int student_id FK
        int bed_id FK
        date start_date
        date end_date
        boolean is_active
        int allocated_by_id FK
        datetime created_at
        string notes
    }

    FEE_STRUCTURE {
        int id PK
        string room_type
        boolean is_ac
        decimal amount
        string fee_period "monthly/quarterly/yearly"
        string description
    }

    PAYMENT {
        int id PK
        int student_id FK
        decimal amount
        string fee_month
        datetime payment_date
        string transaction_id UK
        string status "pending/paid/failed"
        string receipt_number UK
        string payment_method
        string notes
    }

    COMPLAINT {
        int id PK
        int student_id FK
        string category "plumbing/electrical/cleaning/furniture/internet/security/noise/other"
        string priority "low/medium/high/urgent"
        string subject
        text description
        string status "open/in_progress/resolved/closed"
        text resolution_notes
        int assigned_to_id FK
        datetime created_at
        datetime updated_at
        datetime resolved_at
    }

    VISITOR_ENTRY {
        int id PK
        int student_id FK
        string visitor_name
        string visitor_phone
        string relation "parent/guardian/sibling/friend/relative/other"
        string purpose
        datetime check_in
        datetime check_out
        string id_proof
        int logged_by_id FK
    }

    CUSTOMUSER ||--o{ ALLOCATION : "is allocated"
    CUSTOMUSER ||--o{ PAYMENT : "makes"
    CUSTOMUSER ||--o{ COMPLAINT : "submits"
    CUSTOMUSER ||--o{ VISITOR_ENTRY : "receives"
    CUSTOMUSER ||--o{ ALLOCATION : "allocates (as admin)"
    CUSTOMUSER ||--o{ COMPLAINT : "is assigned"
    CUSTOMUSER ||--o{ VISITOR_ENTRY : "logs"
    ROOM ||--|{ BED : "contains"
    BED ||--o{ ALLOCATION : "is allocated"
```

## Relationships Summary

| Relationship | Cardinality | Description |
|---|---|---|
| Room → Bed | 1 : N | Each room contains one or more beds |
| Bed → Allocation | 1 : 0..1 (active) | Each bed can have at most one active allocation |
| Student → Allocation | 1 : N | A student can have multiple allocations over time |
| Student → Payment | 1 : N | A student can make multiple payments |
| Student → Complaint | 1 : N | A student can submit multiple complaints |
| Student → VisitorEntry | 1 : N | A student can have multiple visitors |
| Admin → Allocation | 1 : N | An admin allocates beds |
| Warden → Complaint | 1 : N | A warden can be assigned to multiple complaints |
