# Team Manage

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
   - [Database Connection](#database-connection)
   - [Database Schema](#database-schema)
   - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
6. [User Roles and Permissions](#user-roles-and-permissions)
7. [Application Workflow](#application-workflow)
8. [Detailed Components](#detailed-components)
   - [Routes and Views](#routes-and-views)
   - [Forms](#forms)
   - [Models](#models)
   - [Templates](#templates)
9. [Features](#features-1)
   - [User Registration and Authentication](#user-registration-and-authentication)
   - [Task Assignment and Management](#task-assignment-and-management)
   - [Messaging System](#messaging-system)
   - [Calendar Integration](#calendar-integration)
   - [Login Logging](#login-logging)
   - [Holiday Requests](#holiday-requests)
10. [Setting Up the Application](#setting-up-the-application)
    - [Installation Steps](#installation-steps)
    - [Configuration](#configuration)
    - [Running the Application](#running-the-application)
11. [Security Considerations](#security-considerations)
12. [Error Handling](#error-handling)
13. [Future Improvements](#future-improvements)
14. [Conclusion](#conclusion)
15. [GitHub Repository](#github-repository)
16. [Contact](#contact)

---

## **Introduction**

**Team Manage** is a comprehensive task management web application designed to streamline workflow within organizations. It facilitates seamless communication between managers and employees, efficient task assignment, progress tracking, and intuitive calendar integration for optimal scheduling and visualization.

---

## **About**

Team Manage is the successor and upgraded version of my previous project, **Chai the People**, developed during a hackathon. Building upon the foundations of Chai the People, Team Manage introduces enhanced features, an improved user interface, and robust backend functionalities to better serve organizational needs.

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

- **Task Views**
  - Employees can view their tasks.
  - Managers can view tasks assigned to employees.

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
    'database': 'team_manage'    # Replace with your database name
}

# Admin credentials for initial setup
ADMIN_USER = 'root'               # Replace with your admin username
ADMIN_PASSWORD = 'root_password'  # Replace with your admin password

# Secret key for Flask sessions and CSRF protection
SECRET_KEY = 'your_secret_key'    # Replace with a secure key
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

## **User Roles and Permissions**

The application distinguishes between two user roles:

1. **Manager**
   - Can assign tasks to employees.
   - Can view all tasks and employee calendars.
   - Can communicate with employees via messages.
   - Can approve or deny holiday requests.
   - Can monitor employee login logs.

2. **Employee**
   - Can view assigned tasks.
   - Can update task status.
   - Can access a personalized calendar displaying tasks.
   - Can communicate with managers via messages.
   - Can submit holiday requests.
   - Can view login logs.

---

## **Application Workflow**

### **1. Registration and Login**

- **Registration**: Users can register by providing a username, password, and selecting a role.
- **Login**: Users log in using their credentials.
- **Authentication**: Handled by Flask-Login.
- **Password Security**: Passwords are hashed using Werkzeug's `generate_password_hash` function.

### **2. Dashboard**

- **Manager Dashboard**:
  - Overview of tasks.
  - Access to assign work.
  - View messages and holiday requests.

- **Employee Dashboard**:
  - List of assigned tasks.
  - Option to update task status.
  - View messages.

### **3. Task Assignment**

- **Assigning Tasks**:
  - Managers can assign tasks to employees with optional start and end dates and times.
  - Tasks are stored in the `Projects` table.

### **4. Task Management**

- **Updating Task Status**:
  - Employees can mark tasks as `In Progress` or `Completed`.
  - Managers can verify completed tasks, changing the status to `Verified`.

### **5. Messaging System**

- **Sending Messages**:
  - Users can send messages to each other.
  - Messages include content and timestamp.

- **Viewing Messages**:
  - Users can view messages they've sent and received.
  - Messages are displayed in a list.

### **6. Calendar Integration**

- **Displaying Tasks**:
  - Tasks are displayed on a calendar using FullCalendar.
  - Events show task names and durations.

- **Navigation**:
  - Users can navigate between month, week, and day views.
  - Clicking on dates navigates to the day view.

- **Event Colors**:
  - Tasks are color-coded based on their status.

- **Event Details**:
  - Clicking on an event displays a modal with task details.

### **7. Login Logging**

- **Recording Logins**:
  - Employee login times are recorded in the `LoginLogs` table.
  - Only one login record per user per day is allowed.

- **Viewing Login Logs**:
  - Managers can view login logs to monitor employee attendance.

### **8. Holiday Requests**

- **Submitting Requests**:
  - Employees can request holidays by specifying start and end dates and a reason.

- **Approval Process**:
  - Managers can approve or deny holiday requests.
  - Approved holidays can be reflected in the calendar.

---

## **Detailed Components**

### **Routes and Views**

The application routes handle user requests and return responses. Key routes include:

- **User Authentication**:
  - `/register`: Handles user registration.
  - `/login`: Handles user login.
  - `/logout`: Logs the user out.

- **Dashboard**:
  - `/dashboard`: Redirects users to the appropriate dashboard based on role.
  - `/manager_dashboard`: Manager's dashboard.
  - `/employee_dashboard`: Employee's dashboard.

- **Task Management**:
  - `/assign_work`: Managers assign tasks.
  - `/view_assigned_work`: Employees view assigned tasks.
  - `/mark_as_completed/<project_id>`: Employees mark tasks as completed.
  - `/verify_project/<project_id>`: Managers verify completed tasks.

- **Messaging**:
  - `/messages`: View messages.
  - `/send_message`: Send a message.

- **Calendar**:
  - `/employee_calendar`: Employee's calendar view.
  - `/manager_calendar`: Manager's calendar view.
  - `/employee_calendar_data`: API endpoint for employee calendar data.
  - `/manager_calendar_data`: API endpoint for manager calendar data.

- **Login Logs**:
  - `/login_logs`: View login logs (manager only).

- **Holidays**:
  - `/request_holiday`: Employees submit holiday requests.
  - `/approve_holiday/<holiday_id>`: Managers approve holiday requests.
  - `/deny_holiday/<holiday_id>`: Managers deny holiday requests.

### **Forms**

Forms are used to collect user input. They are defined using WTForms.

- **RegistrationForm**
- **LoginForm**
- **AssignWorkForm**
- **MessageForm**
- **HolidayRequestForm**

### **Models**

Models represent the data structures.

- **User**: Represents a user in the application.
- **load_user**: Function to load a user from the database.

### **Templates**

HTML templates are used to render the views.

- **Base Template (`base.html`)**: Contains common HTML structure and includes blocks for content.
- **Authentication Templates**:
  - `login.html`
  - `register.html`

- **Dashboard Templates**:
  - `manager_dashboard.html`
  - `employee_dashboard.html`

- **Task Templates**:
  - `assign_work.html`
  - `view_assigned_work.html`

- **Messaging Templates**:
  - `messages.html`

- **Calendar Templates**:
  - `employee_calendar.html`
  - `manager_calendar.html`

- **Holiday Templates**:
  - `request_holiday.html`

---

## **Features**

### **User Registration and Authentication**

- **Registration**:
  - Users provide a username, password, and select their role.
  - Passwords are hashed before storage.
  - Unique usernames are enforced.

- **Authentication**:
  - Handled by Flask-Login.
  - Users are redirected to the login page if not authenticated.

- **Authorization**:
  - Routes are protected based on user roles.
  - Decorators check user permissions.

### **Task Assignment and Management**

- **Assigning Tasks**:
  - Managers can assign tasks to employees.
  - Optional start and end dates and times.
  - Task types can be selected.

- **Updating Task Status**:
  - Employees can mark tasks as `In Progress` or `Completed`.
  - Managers can verify tasks, changing the status to `Verified`.

- **Task Views**:
  - Employees can view their tasks.
  - Managers can view tasks assigned to employees.

### **Messaging System**

- **Sending Messages**:
  - Users can send messages to each other.
  - Messages include content and timestamp.

- **Viewing Messages**:
  - Users can view messages they've sent and received.
  - Messages are displayed in a list.

### **Calendar Integration**

- **Displaying Tasks**:
  - Tasks are displayed on a calendar using FullCalendar.
  - Events show task names and durations.

- **Navigation**:
  - Users can navigate between month, week, and day views.
  - Clicking on dates navigates to the day view.

- **Event Colors**:
  - Tasks are color-coded based on their status:
    - `Assigned`: Blue
    - `In Progress`: Orange
    - `Completed`: Purple
    - `Verified`: Green

- **Event Details**:
  - Clicking on an event displays a modal with task details.

### **Login Logging**

- **Recording Logins**:
  - Employee login times are recorded in the `LoginLogs` table.
  - Only one login record per user per day is allowed.

- **Viewing Login Logs**:
  - Managers can view login logs to monitor employee attendance.

### **Holiday Requests**

- **Submitting Requests**:
  - Employees can request holidays by specifying start and end dates and a reason.

- **Approval Process**:
  - Managers can approve or deny holiday requests.
  - Approved holidays can be reflected in the calendar.

---

## **Setting Up the Application**

### **Installation Steps**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/team_manage.git
   cd team_manage
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

### **Configuration**

All configurations are managed through the `config.py` file. Ensure that sensitive information like database passwords and secret keys are kept secure and not exposed in version control.

**Example `config.py`:**

```python
# config.py

DB_CONFIG = {
    'host': 'localhost',
    'user': 'app_user',          # Replace with your database username
    'password': 'app_password',  # Replace with your database password
    'database': 'team_manage'    # Replace with your database name
}

# Admin credentials for initial setup
ADMIN_USER = 'root'               # Replace with your admin username
ADMIN_PASSWORD = 'root_password'  # Replace with your admin password

# Secret key for Flask sessions and CSRF protection
SECRET_KEY = 'your_secret_key'    # Replace with a secure key
```

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
    'database': 'team_manage'    # Replace with your database name
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

## **Security Considerations**

- **Password Hashing**: Passwords are securely hashed before storage.

- **Input Validation**: User inputs are validated using WTForms validators to prevent SQL injection and other attacks.

- **CSRF Protection**: Flask-WTF provides CSRF protection for forms.

- **Session Management**: Flask-Login manages user sessions securely.

- **Error Handling**: Sensitive error messages are not exposed to users.

---

## **Error Handling**

- **Try-Except Blocks**: Database operations are wrapped in try-except blocks to handle exceptions gracefully.

- **User Feedback**: Flash messages inform users of successes or failures.

- **Logging**: Errors are printed to the console for debugging during development.

---

## **Future Improvements**

- **User Interface Enhancements**: Improve the design and usability of the interface.

- **Email Notifications**: Implement email notifications for messages and task updates.

- **File Uploads**: Allow attachments to tasks and messages.

- **Reporting**: Generate reports on task progress and employee performance.

- **Permissions**: Implement more granular permissions and roles.

- **Unit Testing**: Add tests to ensure code reliability.

- **Deployment**: Prepare the application for deployment in a production environment.

---

## **Conclusion**

Team Manage provides a robust platform for task management within an organization. With features like user authentication, task assignment, messaging, and calendar integration, it facilitates efficient communication and workflow management between managers and employees. By following this documentation, developers can understand, set up, and further enhance the application to meet specific needs.

**Note**: Always ensure to keep sensitive information secure, especially when configuring database connections and secret keys. For production environments, consider using environment variables and secure credential storage solutions.

---

## **GitHub Repository**

This project is an upgraded version of **Chai the People**, developed during a hackathon.

🔗 **Chai the People Repository:** [Chai the People](https://github.com/RitikDutta/chai_the_people)

🔗 **Team Manage Repository:** [Team Manage](https://github.com/yourusername/team_manage)

*(Replace `yourusername` with your actual GitHub username and ensure the repository URL is correct.)*

---

## **Contact**

For any inquiries or feedback, please contact:

- **Name:** Ritik Dutta
- **Email:** ritikdutta@example.com
- **GitHub:** [RitikDutta](https://github.com/RitikDutta)

---

*Thank you for using Team Manage!*