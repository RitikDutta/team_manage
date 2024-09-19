from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField, TimeField # Import DateField
from wtforms.validators import Optional, ValidationError
from datetime import datetime, date, timedelta, time



def validate_end_date(form, field):
    if field.data and form.start_date.data and field.data < form.start_date.data:
        raise ValidationError('End date cannot be before start date.')

def validate_times(form, field):
    if (form.start_time.data and not form.start_date.data) or (form.end_time.data and not form.end_date.data):
        raise ValidationError('Start/End date is required if time is specified.')
    if form.start_date.data and form.end_date.data:
        start_datetime = datetime.combine(form.start_date.data, form.start_time.data or datetime.min.time())
        end_datetime = datetime.combine(form.end_date.data, form.end_time.data or datetime.max.time())
        if start_datetime >= end_datetime:
            raise ValidationError('End date/time must be after start date/time.')


#different forms to add details
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('employee', 'Employee'), ('manager', 'Manager')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddEmployeeForm(FlaskForm):
    username = StringField('Employee Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Employee Password', validators=[DataRequired()])
    submit = SubmitField('Add Employee')

class AssignWorkForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    assigned_to = SelectField('Assign To', coerce=int)
    submit = SubmitField('Assign Work')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Message')

class AssignWorkForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    assigned_to = SelectField('Assign To', coerce=int)
    task_type = SelectField('Task Type', choices=[
        ('video', 'Video'),
        ('social media', 'Social Media'),
        ('writing', 'Writing'),
        ('image', 'Image')
    ], validators=[DataRequired()]) 
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional(), validate_end_date])
    end_time = TimeField('End Time', format='%H:%M', validators=[Optional(), validate_times])
    submit = SubmitField('Assign Work')

