
# 🛠️ Dynamic SQL Query Automation

Dynamic SQL Query Automation is a Flask-based web application that automates real-time **CRUD OPERATIONS** on a MySQL database. It combines a modular Python backend with a responsive web frontend, making database management faster, scalable, and user-friendly. 


---

## 🚀 Features

- 🔄 **CRUD Operations**: Insert, fetch, update, and delete users via a web application.
- 🧱 **Modular Backend Structure**: `DBHelper` class to abstract and manage SQL logic cleanly.
- 🔐 **Validation & Logging**: Integrated error handling and logging system for better reliability.
- 🌐 **Flask-Powered Web UI**: Dynamic HTML templates for seamless user experience.

---

## 📂 Project Structure

```
├── app.py            # Flask application routes
├── db_helper.py      # DBHelper class for database operations
├── templates/
│   ├── index.html    # Home page to view all users
│   ├── insert.html   # Form to insert a new user
│   └── update.html   # Form to update existing user
└── logs/
    └── app.log       # File for backend logging
```

---

## 🔧 Setup & Run

1. ✅ **Install Python Packages**
   ```bash
   pip install flask mysql-connector-python
   ```

2. ✅ **Configure MySQL Database**
   - Create a database named `pythontest`.
   - Update credentials in `db_helper.py`:
     ```python
     self.con = connector.connect(
         host="localhost",
         user="your_username",
         password="your_password",
         database="pythontest"
     )
     ```

3. ▶️ **Run the Application**
   ```bash
   python app.py
   ```

4. 🌐 **Access the Web App**
   Open `http://127.0.0.1:5000/` in your browser.

---

## 🧠 Tech Stack

- Python
- Flask
- MySQL
- HTML/CSS
- Object-Oriented Programming (OOP)

---

## 🙌 Author

**Archit Aggarwal**  
🔗 [GitHub](https://github.com/architaggarwal24) • 🔗 [LinkedIn](https://linkedin.com/in/architaggarwal24)

---

## ⭐ Star This Repo

If you found this project helpful, give it a ⭐ and support the repository!
