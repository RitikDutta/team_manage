from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_CONFIG
from models import User, load_user
from forms import RegistrationForm
from forms import MessageForm
from forms import AssignWorkForm
from forms import AddEmployeeForm
from forms import LoginForm
from datetime import datetime, date, timedelta, time
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Connection
def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data
        username = form.username.data
        password = form.password.data
        role = form.role.data

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Insert the new user into the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
                           (username, hashed_password, role))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Registration successful. You can now log in.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            # Handle duplicate username error
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                flash('Username already exists. Please choose a different username.')
            else:
                flash('An error occurred during registration. Please try again.')
            # Optionally, log the error for debugging
            print(f"Error: {err}")
    return render_template('register.html', form=form)


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password'], password):
            user_obj = User(user_id=user['user_id'], username=user['username'], role=user['role'])
            login_user(user_obj)
            flash('Logged in successfully.')

            # record login time for employees only once per day
            if user['role'] == 'employee':
                connection = get_db_connection()
                cursor = connection.cursor()
                today = date.today() 
                user_id = user['user_id']

                #check if a login record for today already exists
                cursor.execute("SELECT 1 FROM LoginLogs WHERE user_id = %s AND login_date = %s", (user_id, today))
                existing_login = cursor.fetchone()

                if not existing_login:
                    # no login recorded for today then insert a new one
                    now = datetime.now()
                    cursor.execute("INSERT INTO LoginLogs (user_id, login_date, login_time) VALUES (%s, %s, %s)",
                                   (user_id, today, now.time()))
                    connection.commit()

                cursor.close()
                connection.close()

            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

# app.py

@app.route('/employee_login_times')
@login_required
def employee_login_times():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT ll.login_date, ll.login_time, u.username
        FROM LoginLogs ll
        JOIN Users u ON ll.user_id = u.user_id
        ORDER BY ll.login_date DESC, ll.login_time DESC
    """)
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('employee_login_times.html', logs=logs)




#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

#dashboard view all things
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'manager':
        return redirect(url_for('manager_dashboard'))
    else:
        return redirect(url_for('employee_dashboard'))

#manager dashboard
@app.route('/manager')
@login_required
def manager_dashboard():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    return render_template('manager_dashboard.html')

#employee dashboard
@app.route('/employee')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    return render_template('employee_dashboard.html')

#add user
@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    form = AddEmployeeForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = 'employee'
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('add_employee'))
        
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, role))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Employee added successfully.')
        return redirect(url_for('manager_dashboard'))
    return render_template('add_employee.html', form=form)

#assign work
@app.route('/assign_work', methods=['GET', 'POST'])
@login_required
def assign_work():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    form = AssignWorkForm()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username FROM Users WHERE role = 'employee'")
    employees = cursor.fetchall()
    cursor.close()
    connection.close()
    # Populate the SelectField choices
    form.assigned_to.choices = [(employee['user_id'], employee['username']) for employee in employees]
    if form.validate_on_submit():
        # Collect form data
        name = form.name.data
        description = form.description.data
        assigned_to = form.assigned_to.data
        task_type = form.task_type.data
        start_date = form.start_date.data or date.today()
        start_time = form.start_time.data
        end_date = form.end_date.data or start_date
        end_time = form.end_time.data

        # Insert into database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Projects (name, description, assigned_to, task_type, start_date, start_time, end_date, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, description, assigned_to, task_type, start_date, start_time, end_date, end_time))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Work assigned successfully.')
        return redirect(url_for('manager_dashboard'))
    return render_template('assign_work.html', form=form)


@app.route('/verify_work')
@login_required
def verify_work():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.project_id, p.name, p.description, u.username
        FROM Projects p
        JOIN Users u ON p.assigned_to = u.user_id
        WHERE p.status = 'completed'
    """)
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('verify_work.html', projects=projects)




@app.route('/verify_project/<int:project_id>')
@login_required
def verify_project(project_id):
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Projects SET status = 'verified', completion_date = CURDATE() WHERE project_id = %s",
        (project_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Project verified successfully.')
    return redirect(url_for('verify_work'))


@app.route('/employee_calendar')
@login_required
def employee_calendar():
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    return render_template('employee_calendar.html')



@app.route('/employee_calendar_data')
@login_required
def employee_calendar_data():
    if current_user.role != 'employee':
        return jsonify([])  # Empty data for unauthorized access
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT name, start_date, end_date
        FROM Projects
        WHERE assigned_to = %s
    """, (current_user.id,))
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    events = []
    for project in projects:
        start = project['start_date']
        end = project['end_date']
        if start:
            event = {
                'title': project['name'],
                'start': start.isoformat(),
            }
            if end and end != start:
                # FullCalendar expects end date to be the day after for inclusive ranges
                event['end'] = (end + timedelta(days=1)).isoformat()
            events.append(event)
    return jsonify(events)



@app.route('/manager_calendar')
@login_required
def manager_calendar():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username FROM Users WHERE role = 'employee'")
    employees = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('manager_calendar.html', employees=employees)


@app.route('/manager_calendar_data')
@login_required
def manager_calendar_data():
    if current_user.role != 'manager':
        return jsonify([])
    employee_id = request.args.get('employee_id')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if employee_id:
        # Fetch tasks for a specific employee
        cursor.execute("""
            SELECT p.name, p.start_date, p.end_date, u.username
            FROM Projects p
            JOIN Users u ON p.assigned_to = u.user_id
            WHERE p.assigned_to = %s
        """, (employee_id,))
    else:
        # Fetch tasks for all employees
        cursor.execute("""
            SELECT p.name, p.start_date, p.end_date, u.username
            FROM Projects p
            JOIN Users u ON p.assigned_to = u.user_id
        """)
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    events = []
    for project in projects:
        start = project['start_date']
        end = project['end_date']
        if start:
            event = {
                'title': f"{project['name']} ({project['username']})",
                'start': start.isoformat(),
            }
            if end and end != start:
                event['end'] = (end + timedelta(days=1)).isoformat()
            events.append(event)
    return jsonify(events)



@app.route('/manager_done_projects')
@login_required
def manager_done_projects():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.project_id, p.name, p.description, u.username
        FROM Projects p
        JOIN Users u ON p.assigned_to = u.user_id
        WHERE p.status = 'verified'
    """)
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('manager_done_projects.html', projects=projects)


@app.route('/employee_done_projects')
@login_required
def employee_done_projects():
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT project_id, name, description
        FROM Projects
        WHERE assigned_to = %s AND status = 'verified'
    """, (current_user.id,))
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('employee_done_projects.html', projects=projects)


@app.route('/view_messages')
@login_required
def view_messages():
    if current_user.role != 'manager':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.message_id, u.username AS sender, m.content, m.timestamp
        FROM Messages m
        JOIN Users u ON m.sender_id = u.user_id
        WHERE m.receiver_id = %s
        ORDER BY m.timestamp DESC
    """, (current_user.id,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_messages.html', messages=messages)

@app.route('/view_assigned_work')
@login_required
def view_assigned_work():
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Projects WHERE assigned_to = %s", (current_user.id,))
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_assigned_work.html', projects=projects)


@app.route('/mark_as_completed/<int:project_id>')
@login_required
def mark_as_completed(project_id):
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Projects SET status = 'completed' WHERE project_id = %s AND assigned_to = %s",
                   (project_id, current_user.id))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Project marked as completed.')
    return redirect(url_for('view_assigned_work'))


@app.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    if current_user.role != 'employee':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))
    form = MessageForm()
    if form.validate_on_submit():
        content = form.content.data
        connection = get_db_connection()
        cursor = connection.cursor()
        #for only one manager
        cursor.execute("SELECT user_id FROM Users WHERE role = 'manager' LIMIT 1")
        manager = cursor.fetchone()
        if manager:
            manager_id = manager[0]
            cursor.execute("INSERT INTO Messages (sender_id, receiver_id, content) VALUES (%s, %s, %s)",
                           (current_user.id, manager_id, content))
            connection.commit()
            flash('Message sent to manager.')
        else:
            flash('No manager found.')
        cursor.close()
        connection.close()
        return redirect(url_for('employee_dashboard'))
    return render_template('send_message.html', form=form)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))



def initialize_database():
    try:
        # Connect to MySQL Server
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()

        # Create the database if it doesn't exist
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci'".format(DB_CONFIG['database'])
        )
        cursor.execute("USE `{}`".format(DB_CONFIG['database']))

        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Users` (
          `user_id` int NOT NULL AUTO_INCREMENT,
          `username` varchar(50) NOT NULL,
          `password` varchar(255) NOT NULL,
          `role` enum('manager','employee') NOT NULL,
          PRIMARY KEY (`user_id`),
          UNIQUE KEY `username` (`username`)
        ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        # Create Projects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Projects` (
          `project_id` int NOT NULL AUTO_INCREMENT,
          `name` varchar(100) NOT NULL,
          `description` text,
          `assigned_to` int DEFAULT NULL,
          `status` enum('assigned','in_progress','completed','verified') DEFAULT 'assigned',
          `completion_date` date DEFAULT NULL,
          `task_type` enum('video','social media','writing','image') NOT NULL DEFAULT 'writing',
          `start_date` date DEFAULT NULL,
          `end_date` date DEFAULT NULL,
          `start_time` time DEFAULT NULL,
          `end_time` time DEFAULT NULL,
          PRIMARY KEY (`project_id`),
          KEY `assigned_to` (`assigned_to`),
          CONSTRAINT `Projects_ibfk_1` FOREIGN KEY (`assigned_to`) REFERENCES `Users` (`user_id`) ON DELETE SET NULL
        ) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        # Create Messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Messages` (
          `message_id` int NOT NULL AUTO_INCREMENT,
          `sender_id` int DEFAULT NULL,
          `receiver_id` int DEFAULT NULL,
          `content` text,
          `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`message_id`),
          KEY `sender_id` (`sender_id`),
          KEY `receiver_id` (`receiver_id`),
          CONSTRAINT `Messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE,
          CONSTRAINT `Messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE
        ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        # Create Holidays table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Holidays` (
          `holiday_id` int NOT NULL AUTO_INCREMENT,
          `user_id` int DEFAULT NULL,
          `start_date` date DEFAULT NULL,
          `end_date` date DEFAULT NULL,
          `reason` text,
          PRIMARY KEY (`holiday_id`),
          KEY `user_id` (`user_id`),
          CONSTRAINT `Holidays_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        # Create LoginLogs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `LoginLogs` (
          `log_id` int NOT NULL AUTO_INCREMENT,
          `user_id` int DEFAULT NULL,
          `login_date` date DEFAULT NULL,
          `login_time` time DEFAULT NULL,
          PRIMARY KEY (`log_id`),
          UNIQUE KEY `unique_user_date` (`user_id`,`login_date`),
          CONSTRAINT `LoginLogs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE
        ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        # Commit the changes
        connection.commit()
        print("Database initialized successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist and could not be created")
        else:
            print(err)
    finally:
        cursor.close()
        connection.close()




if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
