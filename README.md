
# 🛠️ Dynamic SQL Query Automation

A Python-based terminal application to perform real-time **CRUD operations** on a MySQL database using custom-built logic and clean modular design. Ideal for beginners learning SQL and developers seeking automation in basic database tasks.

---

## 🚀 Features

- 🔄 **CRUD Operations**: Insert, fetch, update, and delete users via terminal.
- 🧱 **Object-Oriented Structure**: Modular `DBHelper` class to abstract SQL logic.
- 🔐 **Error Handling**: Graceful input validation and exception messages.
- ⚙️ **MySQL Integration**: Connects directly to MySQL with Python `mysql.connector`.

---

## 📂 Project Structure

```
├── main.py           # CLI interface for user inputs and operations
├── myproject.py      # Contains DBHelper class for database methods
```

---

## 🔧 Setup & Run

1. ✅ **Install MySQL Connector**  
   ```bash
   pip install mysql-connector-python
   ```

2. ✅ **Configure MySQL Database**
   - Create a database named `pythontest`
   - Replace credentials in `myproject.py`:
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
   python main.py
   ```

---

## 📸 Sample Output

```
************WELCOME*********

PRESS 1 to insert new user
PRESS 2 to display all user
PRESS 3 to delete user
PRESS 4 to update user
PRESS 5 to exit program
```

---

## 🧠 Tech Stack

- Python
- MySQL
- OOP Concepts
- Command-Line Interface

---

## 🙌 Author

**Archit Aggarwal**  
🔗 [GitHub](https://github.com/architaggarwal24) • [LinkedIn](https://linkedin.com/in/architaggarwal24)

---

## ⭐ Star This Repo

If you find it helpful or learned something new, give it a ⭐ to support the project!
