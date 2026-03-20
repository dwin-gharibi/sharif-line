# Sharif-Line Survey System

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-✔️-blue.svg)](https://www.postgresql.org/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) <!-- Replace with real CI badge if available -->
[![Responsive](https://img.shields.io/badge/ui-responsive-important)](#)

Sharif Line Survey System is a full-featured and responsive web application for building, distributing, and analyzing online surveys. The project is inspired by [porsline.ir](https://porsline.ir), a leading Persian survey platform, and aims to provide a powerful, open-source alternative. With a drag-and-drop survey builder, modern user experience, and detailed analytics, it is designed to cover the major needs of users and organizations looking to gather feedback and conduct research.

![shairfline demo](./docs/images/sharifline1.png)
![shairfline demo](./docs/images/sharifline2.png)
![shairfline demo](./docs/images/sharifline3.png)


---

## 🚀 Features

- **Drag-and-Drop Survey Builder:** Easily create custom surveys with a dynamic, intuitive interface.
- **User Registration & Authentication:** Secure user management with profile support.
- **Multiple Question Types:** Add text (open/closed), single-choice, multi-choice, rating, and numeric questions.
- **Survey Templates:** Start from scratch or use ready-made survey templates (customizable).
- **Dynamic Editing:** Real-time editing and previewing of surveys before publishing.
- **Easy Distribution:** Share surveys with a unique URL; supports public or invitation-only responses.
- **Anonymous Response Collection:** Option to collect responses anonymously to maximize honesty.
- **Live Analytics:** Instantly view participation stats with interactive charts and tables (powered by Chart.js).
- **Responsive UI:** Mobile-first design using Bootstrap 5 RTL, fully supports Right-to-Left (RTL) languages.
- **Role Management:** Regular users and administrators/superusers with control over survey visibility and management.
- **Media Support:** Option to add images to questions and answers.
- **Export Data:** Download survey results as CSV/Excel for advanced offline analysis.
- **Notifications:** Built-in notification system for survey responses and results updates.
- **Inspiration:** Project modeled after porsline.ir, integrating similar workflows for familiarity.

![shairfline demo](./docs/images/sharifline4.png)
![shairfline demo](./docs/images/sharifline5.png)
![shairfline demo](./docs/images/sharifline6.png)


---

## 🌐 Inspiration

> **This project draws direct inspiration from [porsline.ir](https://porsline.ir), a popular online survey service in Iran.**  
> While not affiliated with Porsline, the app reimagines its robust survey-building and analytics tools, aiming to bring similar capabilities as an open-source project for educational and research purposes.

![shairfline demo](./docs/images/sharifline7.png)


---

## 🛠️ Technologies Used

- **Backend:** Django 4.x (Python 3.8+)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Styling:** Bootstrap 5 RTL
- **Drag-and-Drop:** Custom JavaScript (no third-party drag-and-drop libraries)
- **Charts:** Chart.js
- **Database:** PostgreSQL
- **.env Management:** python-dotenv
- **Virtual Environment/Dependencies:** pip, virtualenv

![shairfline demo](./docs/images/sharifline8.png)

![shairfline demo](./docs/images/sharifline9.png)

---

## 📁 Project Structure

- `sharifline/` — Django project settings & WSGI/ASGI configs
- `accounts/` — User authentication, registration, and profile management
- `surveys/` — Survey models, builder, questions, responses & analytics
- `templates/` — Modular, reusable HTML templates for all views
- `static/` — CSS, JS, images (including custom scripts for drag-and-drop)
- `media/` — User-uploaded files and images

---

## 🏁 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/dwin-gharibi/sharif-line.git
cd sharif-line
```

### 2. Setup a Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory, with:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://username:password@localhost:5432/survey_db
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin Superuser

```bash
python manage.py createsuperuser
```

### 6. Launch the Development Server

```bash
python manage.py runserver
```

Go to [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📝 Example Workflow

**1. Register & Log In**  
Create your account and sign in via the authentication interface.

**2. Create a New Survey**  
Access the dashboard and click “Create Survey”. Use the drag-and-drop builder to add, reorder, or remove questions. Choose question types and set validation.

**3. Edit & Preview**  
Dynamically edit questions and preview your survey to ensure the flow is user-friendly.

**4. Distribute Your Survey**  
Publish your survey and share the supplied URL. You can limit access by invitation or allow all users to participate.

**5. Track Responses**  
Monitor live analytics as responses arrive. View answer distributions, respondent counts, and summary statistics with interactive charts.

![shairfline demo](./docs/images/sharifline10.png)

![shairfline demo](./docs/images/sharifline11.png)


**6. Export or Analyze Data**  
Download results in CSV/Excel format for detailed offline analysis or reporting.

![shairfline demo](./docs/images/sharifline12.png)
![shairfline demo](./docs/images/sharifline13.png)

---

## 💡 Customization & Extensions

- **RTL Support:** All interfaces support Persian/RTL environments out-of-the-box.
- **Custom Templates:** Easily build custom survey templates by editing examples in the `surveys/` application.
- **Extendable:** Modular project structure allows easy addition of new features, such as integrations with third-party analytics or SSO.

---

## 👥 Contributors

This project was developed as part of an Advanced Programming course at Sharif University of Technology.

---

## 📖 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgment

Special thanks to [porsline.ir](https://porsline.ir) for providing inspiration and setting a high standard for online survey tools in the Persian-speaking world.

---

**Sharif Line Survey System – Modern, Flexible,**
