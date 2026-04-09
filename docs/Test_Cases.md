# Test Cases
## Hostel Room Allocation & Complaint Management System

---

## Module 1: Student Registration & Login

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-01 | Student registration with valid data | Valid username, email, phone, password | Account created, redirect to dashboard | ☐ |
| TC-02 | Registration with duplicate username | Existing username | Error: "A user with that username already exists" | ☐ |
| TC-03 | Registration with weak password | Password "123" | Error: Password too short / too common | ☐ |
| TC-04 | Registration with mismatched passwords | password1 ≠ password2 | Error: "Passwords don't match" | ☐ |
| TC-05 | Login with valid credentials | admin / admin123 | Redirect to dashboard, welcome message | ☐ |
| TC-06 | Login with invalid credentials | wrong / wrong | Error: "Invalid username or password" | ☐ |
| TC-07 | Logout | Click logout | Redirect to login page, session ended | ☐ |
| TC-08 | Profile update | Changed phone number | Profile updated successfully message | ☐ |
| TC-09 | Access protected page without login | Navigate to /rooms/ | Redirect to login page | ☐ |
| TC-10 | Role-based display | Login as student | Student dashboard shown (not admin) | ☐ |

---

## Module 2: Room/Bed Management

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-11 | Create room (admin) | Room 401, Floor 4, Double, 2 beds | Room created with 2 beds (A, B) | ☐ |
| TC-12 | Create room (student) | Navigate to /rooms/create/ | Access denied, redirect to dashboard | ☐ |
| TC-13 | View room list | Navigate to /rooms/ | All rooms displayed in grid | ☐ |
| TC-14 | Filter rooms by floor | Select Floor 1 | Only Floor 1 rooms shown | ☐ |
| TC-15 | Filter rooms by type | Select "Single" | Only single rooms shown | ☐ |
| TC-16 | Filter rooms by availability | Select "Available" | Only rooms with free beds shown | ☐ |
| TC-17 | View room detail | Click on Room 101 | Room details, beds, allocations shown | ☐ |
| TC-18 | Allocate bed to student | Select student, set start date | Allocation created, bed status → occupied | ☐ |
| TC-19 | Allocate already occupied bed | Try to allocate occupied bed | Error: "Bed not available" | ☐ |
| TC-20 | Deallocate bed | Confirm deallocation | Allocation ended, bed status → available | ☐ |
| TC-21 | Edit room | Change monthly rent | Room updated successfully | ☐ |
| TC-22 | Delete room | Confirm delete | Room and all beds deleted | ☐ |
| TC-23 | Student views my room | Login as allocated student | Current room, bed, roommate details shown | ☐ |
| TC-24 | Unallocated student views my room | Login as unallocated student | "No room allocated" message shown | ☐ |
| TC-25 | Room color coding | Room with full beds | Red indicator (full) | ☐ |

---

## Module 3: Fee Management

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-26 | View fee dashboard | Login as student | Fee info, payment history shown | ☐ |
| TC-27 | Make mock payment (success) | Click Pay Now, select month | Payment recorded as "Paid", receipt generated | ☐ |
| TC-28 | Make mock payment (failure) | Payment simulation fails | Payment recorded as "Failed", error message | ☐ |
| TC-29 | Pay without allocation | Unallocated student clicks Pay | Error: "No room allocation" | ☐ |
| TC-30 | Download PDF receipt | Click download for paid payment | PDF file downloaded with correct details | ☐ |
| TC-31 | Download receipt for failed payment | Click download for failed payment | Error: "Receipt not available" | ☐ |
| TC-32 | Admin views all payments | Navigate to /fees/all/ | All payments listed with filters | ☐ |
| TC-33 | Filter payments by status | Select "Paid" | Only paid payments shown | ☐ |
| TC-34 | Search payments | Search by student name | Matching payments shown | ☐ |
| TC-35 | Unique receipt/transaction IDs | Make two payments | Different receipt and transaction IDs | ☐ |

---

## Module 4: Complaint / Maintenance Request

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-36 | Submit complaint | Category: Plumbing, Priority: High, Subject, Description | Complaint created, status = Open | ☐ |
| TC-37 | Submit complaint with empty fields | Missing subject or description | Form validation error | ☐ |
| TC-38 | View complaint list (student) | Login as student | Only own complaints shown | ☐ |
| TC-39 | View complaint list (admin) | Login as admin | All complaints shown | ☐ |
| TC-40 | View complaint detail | Click on complaint | Full detail with status, timestamps | ☐ |
| TC-41 | Update complaint status (admin) | Change to "In Progress" | Status updated, message shown | ☐ |
| TC-42 | Resolve complaint | Status → Resolved, add notes | resolved_at timestamp set, notes saved | ☐ |
| TC-43 | Filter by status | Select "Open" | Only open complaints shown | ☐ |
| TC-44 | Filter by category | Select "Electrical" | Only electrical complaints shown | ☐ |
| TC-45 | Student cannot update complaint | Navigate to /complaints/1/update/ | Access denied message | ☐ |

---

## Module 5: Visitor Log

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-46 | Log visitor entry | Name, phone, relation, purpose | Visitor logged with check-in timestamp | ☐ |
| TC-47 | Checkout visitor | Click checkout button | check_out timestamp recorded | ☐ |
| TC-48 | Search visitors | Search by visitor name | Matching records shown | ☐ |
| TC-49 | Student sees own visitors | Login as student | Only own visitor entries shown | ☐ |
| TC-50 | Admin sees all visitors | Login as admin | All visitor entries shown | ☐ |

---

## Module 6: Admin Dashboard

| Test ID | Test Case | Input | Expected Output | Status |
|---------|-----------|-------|-----------------|--------|
| TC-51 | Dashboard stat cards | Login as admin | Correct totals for students, rooms, occupancy, fees | ☐ |
| TC-52 | Complaint category chart | Dashboard loads | Doughnut chart with category distribution | ☐ |
| TC-53 | Complaint status chart | Dashboard loads | Bar chart with status counts | ☐ |
| TC-54 | Recent allocations table | Dashboard loads | Latest 5 allocations shown | ☐ |
| TC-55 | Export students CSV | Click Export Students | CSV file downloaded with student data | ☐ |
| TC-56 | Export payments CSV | Click Export Payments | CSV file downloaded with payment data | ☐ |
| TC-57 | Student dashboard | Login as student | Student-specific stats and quick actions | ☐ |
| TC-58 | Admin-only access | Student visits /chart-data/ | 403 Forbidden response | ☐ |

---

## Non-Functional Test Cases

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| TC-NF-01 | Mobile responsiveness | All pages render correctly at 375px width | ☐ |
| TC-NF-02 | CSRF protection | All POST forms include CSRF token | ☐ |
| TC-NF-03 | Password hashing | Passwords stored as hash in database | ☐ |
| TC-NF-04 | Page load time | Pages load within 3 seconds | ☐ |
| TC-NF-05 | Browser compatibility | Works on Chrome, Firefox, Edge | ☐ |
