from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange

"""
This script defines form classes for getting input data from screen
"""


class LoginForm(FlaskForm):
    """
    This is a form class used for login.html
    Validators of DataRequired are applied.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AppointmentForm(FlaskForm):
    """
    This is a form class used for make_appointment.html
    Validators of DataRequired and Length(for StringField) are applied.
    """
    # This is appointment type.
    type = SelectField('Type', choices=[("Consultation", "Consultation"), ("Prescription", "Prescription"), \
                                        ("Surgery", "Surgery")], validators=[DataRequired()])
    staff_name = StringField("Doctor's Name", validators=[DataRequired(), Length(max=32)])
    patient_name = StringField("Patient's Name", validators=[DataRequired(), Length(max=32)])
    patient_address = StringField("Patient's Address", validators=[DataRequired(), Length(max=64)])
    patient_phone = StringField("Patient's Phone", validators=[DataRequired(), Length(max=15)])
    date = DateField('Appointment Date', validators=[DataRequired()])
    # Time should be selected from the below
    time = SelectField('Appointment Time', choices=[("9:00", "9:00"), ("11:00", "11:00"), ("14:00", "14:00"), ("16:00", "16:00")], validators=[DataRequired()])
    submit = SubmitField('Register')


class PrescriptionForm(FlaskForm):
    """
    This is a form class used for issue_prescription.html
    Validators of DataRequired are applied.
    """
    # This is medicine type.
    type = SelectField('Type', choices=[("Tablet", "Tablet"), ("Powder", "Powder"), \
                                        ("Ointment", "Ointment")], validators=[DataRequired()])
    # Readonly field. The name of the doctor operating prescription page is automatically set to this field.
    doctor_name = StringField("Doctor's Name", render_kw={'readonly': True})
    patient_name = StringField("Patient's Name", validators=[DataRequired(), Length(max=32)])
    quantity = IntegerField('Quantity', validators=[DataRequired(message='This field must be input 1-30'), NumberRange(min=1, max=30, \
                                                                    message='Quantity must be 1-30')])
    dosage = DecimalField('Dosage', places=1, validators=[DataRequired()])
    submit = SubmitField('Register')


class PatientForm(FlaskForm):
    """
    This is a form class used for register_prescription.html
    Validators of DataRequired are applied.
    """
    name = StringField("Name", validators=[DataRequired(), Length(max=32)])
    address = StringField("Address", validators=[DataRequired(), Length(max=64)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=15)])
    doctor_name = StringField("Primaty Doctor's Name", validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('Register')


class HealthcareProfessionalForm(FlaskForm):
    """
    This is a form class used for register_healthcare_pro.html
    Validators of DataRequired are applied.
    """
    # This is medicine type.
    type = SelectField('Type', choices=[("doctor", "doctor"), ("nurse", "nurse")], validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(max=32)])
    employee_num = StringField("Employee Number", validators=[DataRequired(), Length(max=5)])
    submit = SubmitField('Register')