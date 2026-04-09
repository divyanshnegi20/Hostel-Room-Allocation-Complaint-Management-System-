# 🏠 HostelHub — Hostel Room Allocation & Complaint Management System

A web-based system to manage hostel/PG room allocation, fee records, and student complaints.

**Tech Stack:** Python, Django, HTML, CSS, Bootstrap 5, SQLite, Chart.js

---

## 📋 How to Run This Project (Step-by-Step)

### Step 1: Make sure Python is installed
Open **Command Prompt** (search "cmd" in Start Menu) and type:
```
python --version
```
If you see something like `Python 3.x.x`, you're good. If not, download Python from https://www.python.org/downloads/ and install it (tick "Add to PATH" during installation).

### Step 2: Open the project folder in Command Prompt
```
cd "c:\6th sem\Software engg\PROJECT"
```

### Step 3: Install required packages
```
pip install django xhtml2pdf
```

### Step 4: Run database setup (only first time)
```
python manage.py migrate
```

### Step 5: Load sample data (only first time)
```
python manage.py seed_data
```

### Step 6: Start the server
```
python manage.py runserver
```

You will see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 7: Open in browser
Open **Google Chrome** and go to:
```
http://127.0.0.1:8000/
```

### Step 8: Login
Use these credentials:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Warden | warden | warden123 |
| Student | rahul | student123 |
| Student | priya | student123 |

### Step 9: To stop the server
Press `Ctrl + C` in the Command Prompt.

---

## 🌐 How to Access from Other Devices (Same WiFi)

### Step 1: Find your computer's IP address
Open Command Prompt and type:
```
ipconfig
```
Look for **IPv4 Address** under your WiFi adapter. It will look like `192.168.1.105`.

### Step 2: Start server with your IP
```
python manage.py runserver 0.0.0.0:8000
```

### Step 3: Open on phone/other laptop
On the **other device** (connected to the same WiFi), open a browser and type:
```
http://192.168.1.105:8000/
```
(Replace `192.168.1.105` with YOUR IP address from Step 1)

> ⚠️ Both devices must be on the **same WiFi network**.

---

## 📁 Project Structure

```
PROJECT/
├── manage.py              ← Main file to run the server
├── config/                ← Django settings & URLs
├── apps/
│   ├── accounts/          ← Student Registration & Login
│   ├── rooms/             ← Room/Bed Management & Allocation
│   ├── fees/              ← Fee Management & Receipts
│   ├── complaints/        ← Complaint Tracking
│   ├── visitors/          ← Visitor Log
│   └── dashboard/         ← Admin Dashboard & Reports
├── templates/             ← All HTML pages
├── static/                ← CSS, JavaScript, Images
├── docs/                  ← SRS, ER Diagram, Class Diagram, Test Cases, Maintenance
├── db.sqlite3             ← Database file (auto-created)
└── requirements.txt       ← Python packages needed
```

---

## 🔑 Login Credentials

| Role | Username | Password | What they can do |
|------|----------|----------|------------------|
| Admin | admin | admin123 | Everything — manage rooms, allocate beds, view reports, export data |
| Warden | warden | warden123 | Manage rooms, update complaints, view reports |
| Student | rahul | student123 | View room, pay fees, submit complaints, log visitors |
| Student | priya | student123 | Same as above |
| Student | amit | student123 | Same as above |
| Student | neha | student123 | Same as above |
| Student | vikram | student123 | Same as above |
| Student | ananya | student123 | Same as above |

---

## 📦 Modules

1. **Student Registration & Login** — Register, login, profile management
2. **Room/Bed Allocation** — Add rooms, allocate beds, view availability
3. **Fee Management** — Mock payment, download PDF receipts
4. **Complaint Tracking** — Submit complaints, track status
5. **Visitor Log** — Log visitor check-in/check-out
6. **Admin Dashboard** — Charts, stats, CSV export reports
"# Hostel-Room-Allocation-Complaint-Management-System-" 
