# **TaskMaster Pro**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.2-brightgreen.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)

## **Table of Contents**

1. [Introduction](#introduction)
2. [About](#about)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Database Design](#database-design)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Usage](#usage)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)
12. [Contact](#contact)

---

## **Introduction**

**TaskMaster Pro** is a comprehensive task management web application designed to streamline workflow within organizations. It facilitates seamless communication between managers and employees, efficient task assignment, progress tracking, and intuitive calendar integration for optimal scheduling and visualization.

---

## **About**

TaskMaster Pro is the successor and upgraded version of my previous project, **Chai the People**, developed during a hackathon. Building upon the foundations of Chai the People, TaskMaster Pro introduces enhanced features, improved user interface, and robust backend functionalities to better serve organizational needs.

🔗 **Chai the People Repository:** [Chai the People](https://github.com/RitikDutta/chai_the_people)

---

## **Features**

### **User Roles and Permissions**

- **Manager**
  - Assign tasks to employees with optional start and end dates/times.
  - View and manage all tasks and employee calendars.
  - Communicate with employees via messages.
  - Approve or deny holiday requests.
  - Monitor employee login logs.

- **Employee**
  - View assigned tasks and update their status.
  - Access a personalized calendar displaying tasks.
  - Communicate with managers via messages.
  - Submit holiday requests.
  - View login logs.

### **Task Management**

- **Assigning Tasks**
  - Managers can assign tasks specifying task type, description, and deadlines.
  - Optional start and end dates/times for tasks.
  - Tasks are color-coded on the calendar based on status.

- **Updating Task Status**
  - Employees can mark tasks as `In Progress` or `Completed`.
  - Managers can verify completed tasks, updating their status to `Verified`.

### **Messaging System**

- Real-time communication between managers and employees.
- Messages are timestamped and stored securely in the database.

### **Calendar Integration**

- **FullCalendar** integration for visual task management.
- Color-coded events based on task status:
  - `Assigned`: Blue
  - `In Progress`: Orange
  - `Completed`: Purple
  - `Verified`: Green
- Clickable events to view detailed task information.

### **Login Logging**

- Records employee login times to monitor attendance.
- Ensures one login record per user per day.

### **Holiday Requests**

- Employees can submit holiday requests with start and end dates and reasons.
- Managers can approve or deny requests, which are reflected on the calendar.

---

## **Technologies Used**

- **Backend**
  - Python 3.11
  - Flask 2.3.2
  - MySQL 8.0
  - Flask-Login for authentication
  - Flask-WTF and WTForms for form handling
  - Werkzeug Security for password hashing

- **Frontend**
  - HTML5 & CSS3
  - Bootstrap 5 for responsive design
  - JavaScript
  - FullCalendar for calendar integration
  - Flatpickr for enhanced date and time pickers

- **Others**
  - MySQL Connector/Python for database interactions

---

## **Database Design**

### **Database Connection**

The application connects to a MySQL database using the `mysql-connector-python` library. Database configurations are managed through a `config.py` file, ensuring separation of concerns and ease of configuration.

**Example `config.py`:**

```python
# config.py

DB_CONFIG = {
    'host': 'localhost',
    'user': 'app_user',          # Replace with your database username
    'password': 'app_password',  # Replace with your database password
    'database': 'taskmaster_pro' # Replace with your database name
}

# Admin credentials for initial setup
ADMIN_USER = 'root'               # Replace with your admin username
ADMIN_PASSWORD = 'root_password'  # Replace with your admin password
```

### **Database Schema**

The database consists of five primary tables:

1. **Users**
2. **Projects**
3. **Messages**
4. **Holidays**
5. **LoginLogs**

#### **1. Users Table**

Stores user information.

- **Columns**:
  - `user_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `username` (VARCHAR(50), UNIQUE, NOT NULL)
  - `password` (VARCHAR(255), NOT NULL)
  - `role` (ENUM('manager', 'employee'), NOT NULL)

#### **2. Projects Table**

Stores task information assigned to employees.

- **Columns**:
  - `project_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `name` (VARCHAR(100), NOT NULL)
  - `description` (TEXT)
  - `assigned_to` (INT, FOREIGN KEY to `Users.user_id`)
  - `status` (ENUM('assigned', 'in_progress', 'completed', 'verified'), DEFAULT 'assigned')
  - `completion_date` (DATE)
  - `task_type` (ENUM('video', 'social media', 'writing', 'image'), DEFAULT 'writing')
  - `start_date` (DATE)
  - `end_date` (DATE)
  - `start_time` (TIME)
  - `end_time` (TIME)

#### **3. Messages Table**

Stores messages exchanged between users.

- **Columns**:
  - `message_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `sender_id` (INT, FOREIGN KEY to `Users.user_id`)
  - `receiver_id` (INT, FOREIGN KEY to `Users.user_id`)
  - `content` (TEXT)
  - `timestamp` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### **4. Holidays Table**

Stores holiday requests made by employees.

- **Columns**:
  - `holiday_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `user_id` (INT, FOREIGN KEY to `Users.user_id`)
  - `start_date` (DATE)
  - `end_date` (DATE)
  - `reason` (TEXT)

#### **5. LoginLogs Table**

Stores login records for employees.

- **Columns**:
  - `log_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `user_id` (INT, FOREIGN KEY to `Users.user_id`)
  - `login_date` (DATE)
  - `login_time` (TIME)
  
- **Constraints**:
  - Unique constraint on `user_id` and `login_date` to prevent multiple logins per day.

### **Entity-Relationship (ER) Diagram**

![ER Diagram](https://i.imgur.com/YourERDiagramLink.png)

*Replace the image link with your actual ER diagram image.*

---

## **Installation**

### **Prerequisites**

- **Python 3.11** installed on your system.
- **MySQL 8.0** installed and running.
- **Git** installed for cloning the repository.

### **Steps**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/taskmaster_pro.git
   cd taskmaster_pro
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Unix or MacOS:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **Example `requirements.txt`:**

   ```
   Flask==2.3.2
   flask-login==0.6.2
   mysql-connector-python==8.0.32
   Flask-WTF==1.1.1
   WTForms==3.0.1
   Werkzeug==2.3.4
   ```

5. **Configure the Application**

   - Rename `config_example.py` to `config.py`.
   - Update the database configurations and admin credentials in `config.py`.

6. **Initialize the Database**

   The application includes a script to initialize the database schema and create necessary tables.

   ```bash
   python app.py
   ```

   *Upon running, the script will create the database and tables as per the schema.*

7. **Create an Admin User**

   - Access the registration page at `http://localhost:5000/register`.
   - Register a new user with the role `manager`.

---

## **Configuration**

All configurations are managed through the `config.py` file. Ensure that sensitive information like database passwords and secret keys are kept secure and not exposed in version control.

**Example `config.py`:**

```python
# config.py

DB_CONFIG = {
    'host': 'localhost',
    'user': 'app_user',          # Replace with your database username
    'password': 'app_password',  # Replace with your database password
    'database': 'taskmaster_pro' # Replace with your database name
}

# Admin credentials for initial setup
ADMIN_USER = 'root'               # Replace with your admin username
ADMIN_PASSWORD = 'root_password'  # Replace with your admin password

# Secret key for Flask sessions and CSRF protection
SECRET_KEY = 'your_secret_key'    # Replace with a secure key
```

---

## **Usage**

1. **Run the Application**

   ```bash
   python app.py
   ```

2. **Access the Application**

   Open your web browser and navigate to `http://localhost:5000/`.

3. **Register Users**

   - **Managers** can register themselves or add employees via the dashboard.
   - **Employees** can register if allowed or are added by managers.

4. **Assign Tasks**

   - Managers can assign tasks to employees with optional dates and times.
   - Tasks appear on both manager and employee calendars with color-coded statuses.

5. **View and Update Tasks**

   - Employees can view their assigned tasks and update their status.
   - Managers can verify completed tasks.

6. **Messaging**

   - Users can send and receive messages through the messaging interface.

7. **Calendar**

   - Access the calendar to view tasks visually.
   - Click on events to view detailed task information.

8. **Holiday Requests**

   - Employees can submit holiday requests.
   - Managers can approve or deny these requests.

---

## **Contributing**

Contributions are welcome! To contribute:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Open a Pull Request**

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Acknowledgements**

- Inspired by my previous project, [Chai the People](https://github.com/RitikDutta/chai_the_people), developed during a hackathon.
- [Flask](https://flask.palletsprojects.com/) - The web framework used.
- [Bootstrap](https://getbootstrap.com/) - For responsive design.
- [FullCalendar](https://fullcalendar.io/) - For calendar integration.
- [Flatpickr](https://flatpickr.js.org/) - For enhanced date and time pickers.

---

## **Contact**

For any inquiries or feedback, please contact:

- **Name:** Ritik Dutta
- **Email:** ritikdutta@example.com
- **GitHub:** [RitikDutta](https://github.com/RitikDutta)

---

*Thank you for using TaskMaster Pro!*