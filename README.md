# Jobryn — Professional Job Portal & Social Network

Jobryn is a production-ready Django platform that combines job search, recruiter management, social networking, and real-time messaging into a single, high-fidelity experience.

## 🚀 Key Features

- **Recruiter Dashboard**: Manage companies, jobs, applications, and analytics in a custom [Unfold Admin](https://github.com/unfoldadmin/django-unfold) interface.
- **Job Seeker Experience**: Build a portfolio with experiences, educations, skills, and certifications; apply for jobs, and track applications.
- **Social Networking**: Connect, follow, post updates, comment, like, and message in real-time.
- **Role-Based Access Control (RBAC)**: Strict API separation between `job_seeker` and `recruiter`.
- **Engagement Analytics**: Real-time KPI stats and data-vivid charts on the admin dashboard.
- **Payments Integration**: Support for NPR currency and Khalti payment tracking.

## 🏗 System Architecture

The project consists of 20 modular Django apps, organized as follows:

- **Users & Identity**: `account`, `profiles`, `experiences`, `educations`, `skills`, `certifications`, `projects`.
- **Recruitment**: `companies`, `jobs`, `applications`, `meetings`.
- **Social & Messaging**: `chat_messages`, `posts`, `connections`, `follows`, `notifications`.
- **Learning & Growth**: `learning` (Courses & Enrollments).
- **Billing & Communication**: `billing` (Invoices & Payroll), `newsletters`.

## 🔐 Roles & Permissions

This system implements strict **Owner-Only** filtering and **Role-Based** permissions:

### 💼 Recruiter
- Can create/manage their own Company.
- Can post Jobs and view Applicants for their own jobs.
- Can schedule Meetings and issue Invoices to hires.
- Access to the full Admin Dashboard.

### 👤 Job Seeker
- Can build their professional profile.
- Can apply for Jobs and view their own Application statuses.
- Can enroll in Courses and track Learning progress.
- Cannot access the Admin Dashboard.

## 🛠 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Virtual Environment (`venv`)

### 2. Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Database & Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Running the Project
```bash
python manage.py runserver
```
Visit the Admin at `http://127.0.0.1:8000/admin/`.

## 📂 Project Structure Highlights

- `jobrynbackend/dashboard.py`: Contains data aggregation logic for the admin charts.
- `jobrynbackend/settings.py`: Integrated with Unfold, DRF SimpleJWT, and custom RBAC settings.
- `account/permissions.py`: Global permission classes (`IsJobSeeker`, `IsRecruiter`).
- `account/models.py`: Custom User model with strict `role` choices.

---
*Built for production scale with Django 6.x and Django REST Framework.*
# jobryn
