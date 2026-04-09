# Class Diagram
## Hostel Room Allocation & Complaint Management System

```mermaid
classDiagram
    class CustomUser {
        +int id
        +String username
        +String email
        +String password
        +String first_name
        +String last_name
        +String role
        +String phone
        +String parent_phone
        +String address
        +String institution
        +DateTime date_joined
        +Boolean is_active
        +is_student() Boolean
        +is_hostel_admin() Boolean
        +is_warden() Boolean
        +get_full_name() String
    }

    class Room {
        +int id
        +String room_number
        +int floor
        +String room_type
        +int total_beds
        +Boolean is_ac
        +Decimal monthly_rent
        +String description
        +DateTime created_at
        +available_beds() int
        +occupied_beds() int
        +is_full() Boolean
        +occupancy_percentage() int
    }

    class Bed {
        +int id
        +Room room
        +String bed_label
        +String status
        +__str__() String
    }

    class Allocation {
        +int id
        +CustomUser student
        +Bed bed
        +Date start_date
        +Date end_date
        +Boolean is_active
        +CustomUser allocated_by
        +DateTime created_at
        +String notes
        +save() void
    }

    class FeeStructure {
        +int id
        +String room_type
        +Boolean is_ac
        +Decimal amount
        +String fee_period
        +String description
        +get_room_type_display() String
    }

    class Payment {
        +int id
        +CustomUser student
        +Decimal amount
        +String fee_month
        +DateTime payment_date
        +String transaction_id
        +String status
        +String receipt_number
        +String payment_method
        +String notes
        +save() void
    }

    class Complaint {
        +int id
        +CustomUser student
        +String category
        +String priority
        +String subject
        +String description
        +String status
        +String resolution_notes
        +CustomUser assigned_to
        +DateTime created_at
        +DateTime updated_at
        +DateTime resolved_at
        +is_open() Boolean
    }

    class VisitorEntry {
        +int id
        +CustomUser student
        +String visitor_name
        +String visitor_phone
        +String relation
        +String purpose
        +DateTime check_in
        +DateTime check_out
        +String id_proof
        +CustomUser logged_by
        +is_checked_out() Boolean
    }

    class StudentRegistrationForm {
        +save() CustomUser
    }

    class CustomLoginForm {
        +get_user() CustomUser
    }

    class ProfileUpdateForm {
        +save() CustomUser
    }

    class RoomForm {
        +save() Room
    }

    class AllocationForm {
        +save() Allocation
    }

    class ComplaintForm {
        +save() Complaint
    }

    class ComplaintUpdateForm {
        +save() Complaint
    }

    class VisitorEntryForm {
        +save() VisitorEntry
    }

    Room "1" --o "1..*" Bed : contains
    Bed "1" --o "0..1" Allocation : allocated_to
    CustomUser "1" --o "0..*" Allocation : has
    CustomUser "1" --o "0..*" Payment : makes
    CustomUser "1" --o "0..*" Complaint : submits
    CustomUser "1" --o "0..*" VisitorEntry : receives
    CustomUser "1" --o "0..*" Allocation : allocates
    CustomUser "1" --o "0..*" Complaint : assigned_to

    StudentRegistrationForm ..> CustomUser : creates
    RoomForm ..> Room : creates
    AllocationForm ..> Allocation : creates
    ComplaintForm ..> Complaint : creates
    VisitorEntryForm ..> VisitorEntry : creates
```

## Module-wise Class Organization

### accounts (Authentication Module)
- `CustomUser` — extends Django AbstractUser
- `StudentRegistrationForm`, `CustomLoginForm`, `ProfileUpdateForm`

### rooms (Room & Allocation Module)
- `Room`, `Bed`, `Allocation`
- `RoomForm`, `BedForm`, `AllocationForm`

### fees (Fee Management Module)
- `FeeStructure`, `Payment`

### complaints (Complaint Module)
- `Complaint`
- `ComplaintForm`, `ComplaintUpdateForm`

### visitors (Visitor Log Module)
- `VisitorEntry`
- `VisitorEntryForm`

### dashboard (Dashboard Module)
- No models (uses aggregation across all apps)
