# KinoSelect

**KinoSelect** is a simple Flask-based web application for online cinema ticket booking.  
It allows users to register, log in, browse movies, reserve seats, view booking history, and manage reservations.

---

##  Live Demo

Deployed on [Render](https://kinoselect.onrender.com/)  
 **Link:** [https://kinoselect.onrender.com/](https://kinoselect.onrender.com/)  
> Make sure to set `SECRET_KEY` in Render's environment settings.

---

##  Technologies Used

- **Python 3.12**
- **Flask** – Web framework
- **Flask-Login** – Authentication
- **Flask-SQLAlchemy** – ORM
- **SQLite** – Local development database
- **Jinja2** – HTML templating
- **HTML/CSS** – Frontend
- **Gunicorn** – WSGI server for production deployment

---

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/kinoselect.git
cd kinoselect

### 2. Install dependencies
pip install -r requirements.txt
