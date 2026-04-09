# Hostel/PG Management System — Implementation Plan

## 1. Overview

Build a full-stack web application for managing hostel/PG operations including student registration, room allocation, fee tracking with mock payments, complaint/maintenance requests, visitor logging, and an admin dashboard with reports.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12 + Django 5.x |
| **Frontend** | HTML5, CSS3, Bootstrap 5, vanilla JS |
| **Database** | MySQL 8 (via `mysqlclient`) |
| **Auth** | Django built-in auth (custom User model) |
| **PDF/Receipts** | `xhtml2pdf` for fee receipts |
| **Charts** | Chart.js (CDN) for admin dashboard |

> [!IMPORTANT]
> **MySQL Setup Required**: You must have MySQL 8 installed and running locally. We will need a database name, username, and password from you before we can run migrations.

---

## 3. Project Structure

```
c:\6th sem\Software engg\PROJECT\
├── hostel_mgmt/                  # Django project root
│   ├── manage.py
│   ├── config/                   # Project settings & URLs
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/             # Student Registration & Login
│   │   │   ├── models.py         # CustomUser (extends AbstractUser)
│   │   │   ├── forms.py          # Registration, Login, Profile forms
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── templates/accounts/
│   │   ├── rooms/                # Room/Bed Availability & Allocation
│   │   │   ├── models.py         # Room, Bed, Allocation
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── templates/rooms/
│   │   ├── fees/                 # Fee Management & Receipts
│   │   │   ├── models.py         # FeeStructure, Payment
│   │   │   ├── views.py          # Mock payment flow, PDF receipt
│   │   │   ├── urls.py
│   │   │   └── templates/fees/
│   │   ├── complaints/           # Complaint / Maintenance Requests
│   │   │   ├── models.py         # Complaint (status workflow)
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── templates/complaints/
│   │   ├── visitors/             # Visitor Log (Optional module)
│   │   │   ├── models.py         # VisitorEntry
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── templates/visitors/
│   │   └── dashboard/            # Admin Dashboard & Reports
│   │       ├── views.py          # Aggregated stats, charts
│   │       ├── urls.py
│   │       └── templates/dashboard/
│   ├── static/                   # CSS, JS, images
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   └── templates/                # Base templates & shared partials
│       ├── base.html
│       ├── navbar.html
│       └── footer.html
├── docs/                         # Client deliverables
│   ├── SRS.md
│   ├── ER_Diagram.md
│   ├── Class_Diagram.md
│   ├── Test_Cases.md
│   └── Maintenance_Strategy.md
└── requirements.txt
```

---

## 4. Database Design (ER Summary)

### Core Entities

| Entity | Key Fields |
|---|---|
| **CustomUser** | `id`, `username`, `email`, `password`, `role` (student/admin/warden), `phone`, `parent_phone`, `address`, `date_joined` |
| **Room** | `id`, `room_number`, `floor`, `room_type` (single/double/triple), `total_beds`, `is_ac`, `monthly_rent` |
| **Bed** | `id`, `room_fk`, `bed_label` (A/B/C), `status` (available/occupied/maintenance) |
| **Allocation** | `id`, `student_fk`, `bed_fk`, `start_date`, `end_date`, `is_active` |
| **FeeStructure** | `id`, `room_type`, `amount`, `fee_period` (monthly/quarterly/yearly) |
| **Payment** | `id`, `student_fk`, `amount`, `fee_month`, `payment_date`, `transaction_id`, `status` (pending/paid/failed), `receipt_number` |
| **Complaint** | `id`, `student_fk`, `room_fk`, `category` (plumbing/electrical/cleaning/other), `description`, `status` (open/in-progress/resolved/closed), `created_at`, `resolved_at` |
| **VisitorEntry** | `id`, `student_fk`, `visitor_name`, `visitor_phone`, `relation`, `check_in`, `check_out`, `purpose` |

### Key Relationships
- `Room` 1 → N `Bed`
- `Bed` 1 → 0..1 `Allocation` (active)
- `CustomUser(student)` 1 → N `Payment`
- `CustomUser(student)` 1 → N `Complaint`
- `CustomUser(student)` 1 → N `VisitorEntry`

---

## 5. Module Details

### Module 1 — Student Registration & Login (`accounts`)
- Custom User model extending `AbstractUser` with role field
- Registration form with validation (email, phone, etc.)
- Login / Logout using Django auth
- Profile page (view & edit)
- Role-based access: **Student** vs **Admin/Warden**

### Module 2 — Room/Bed Availability & Allocation (`rooms`)
- Admin can CRUD rooms and beds
- Students see a room availability grid (color-coded: green=available, red=occupied)
- Admin allocates a bed to a student → creates `Allocation` record
- Automatic bed status toggle on allocation/deallocation
- Room search with filters (floor, type, AC/non-AC)

### Module 3 — Fee Management & Receipts (`fees`)
- Fee structure table per room type
- Student sees dues and payment history
- **Mock payment flow**: student clicks "Pay Now" → simulated gateway page → random success/failure → saves `Payment`
- PDF receipt generation (downloadable) using `xhtml2pdf`
- Admin can view all payments, filter by month/student/status

### Module 4 — Complaint / Maintenance Requests (`complaints`)
- Student submits complaint with category & description
- Status workflow: Open → In-Progress → Resolved → Closed
- Admin/Warden can update status and add resolution notes
- Student sees own complaint history with timestamps

### Module 5 — Visitor Log (`visitors`) *(Optional)*
- Student or admin logs a visitor entry (name, phone, relation, purpose)
- Check-in / Check-out timestamps
- Admin can view & search all visitor logs

### Module 6 — Admin Dashboard (`dashboard`)
- Summary cards: Total students, Rooms, Occupancy %, Pending fees, Open complaints
- Charts (Chart.js): Occupancy trend, Fee collection bar chart, Complaint category pie chart
- Quick links to each management section
- Export reports (CSV)

---

## 6. UI / UX Approach

- **Bootstrap 5** responsive layout with a **sidebar navigation** for admin, **top navbar** for students
- **Color Palette**: Dark navy sidebar (`#1a1a2e`), teal accents (`#16213e`, `#0f3460`), vibrant highlight (`#e94560`)
- **Google Font**: Inter for clean, modern typography
- **Cards with subtle shadows** for data display
- **Micro-animations**: fade-in on page load, hover lift on cards, smooth accordion for complaint details
- **Mobile-responsive** grid for room availability
- **Toast notifications** for actions (allocation, payment, complaint submission)

---

## 7. Proposed Changes

### Phase 1 — Project Skeleton & Auth (accounts)

#### [NEW] `requirements.txt`
Django, mysqlclient, xhtml2pdf, python-dotenv

#### [NEW] `hostel_mgmt/config/settings.py`
Django settings configured for MySQL, custom user model, static files, Bootstrap CDN, template dirs

#### [NEW] `hostel_mgmt/apps/accounts/`
Custom User model, registration/login views, templates with Bootstrap forms

---

### Phase 2 — Room & Bed Management (rooms)

#### [NEW] `hostel_mgmt/apps/rooms/`
Room/Bed/Allocation models, admin CRUD views, student availability grid, allocation workflow

---

### Phase 3 — Fee Management (fees)

#### [NEW] `hostel_mgmt/apps/fees/`
FeeStructure/Payment models, mock payment flow, PDF receipt generation, admin fee listing

---

### Phase 4 — Complaints (complaints)

#### [NEW] `hostel_mgmt/apps/complaints/`
Complaint model with status workflow, student submission form, admin status update, resolution tracking

---

### Phase 5 — Visitor Log (visitors)

#### [NEW] `hostel_mgmt/apps/visitors/`
VisitorEntry model, check-in/check-out views, admin search & listing

---

### Phase 6 — Admin Dashboard (dashboard)

#### [NEW] `hostel_mgmt/apps/dashboard/`
Aggregation views, Chart.js integration, summary cards, CSV export

---

### Phase 7 — Documentation Deliverables

#### [NEW] `docs/SRS.md`
Software Requirements Specification document

#### [NEW] `docs/ER_Diagram.md`
ER diagram in Mermaid format

#### [NEW] `docs/Class_Diagram.md`
Class diagram in Mermaid format

#### [NEW] `docs/Test_Cases.md`
Comprehensive test cases for all modules

#### [NEW] `docs/Maintenance_Strategy.md`
Maintenance strategy document

---

## 8. Open Questions

> [!IMPORTANT]
> **MySQL Credentials**: What are your MySQL database name, username, and password? (We can also use SQLite initially and switch to MySQL later if you prefer.)

> [!IMPORTANT]
> **Python Version**: Do you have Python 3.10+ installed? Please confirm so we can set up the virtual environment.

> [!NOTE]
> **Visitor Log**: You marked this as optional. Should we include it in the initial build or skip it for now?

> [!NOTE]
> **Deployment**: Is this for local development only, or do you need deployment instructions (e.g., PythonAnywhere, Railway)?

---

## 9. Verification Plan

### Automated Tests
- Django `TestCase` for each app's models and views
- Form validation tests for registration, complaints, payments
- URL resolution tests
- Run with: `python manage.py test`

### Manual / Browser Verification
- Walk through complete student flow: Register → Login → View Rooms → Mock Payment → Submit Complaint → View Receipt
- Walk through admin flow: Login → Dashboard → Allocate Room → Process Complaint → View Reports
- Responsive testing at mobile, tablet, desktop breakpoints
- PDF receipt download verification

### Build Verification
- `python manage.py check` — system checks
- `python manage.py makemigrations --check` — migration consistency
- `python manage.py collectstatic` — static files
