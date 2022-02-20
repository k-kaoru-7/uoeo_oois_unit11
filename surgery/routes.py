from datetime import datetime, date, timedelta
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from surgery import app
from surgery.forms import LoginForm, AppointmentForm, PrescriptionForm, PatientForm, HealthcareProfessionalForm
from surgery.models import User, AppointmentSchedule, Receptionist, HealthcareProfessional, Doctor, Patient, Prescription


"""
This scripts defines Controller classes
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Controller for Sign In page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print('Login Check')
        # Get user data from DB
        user = User.query.filter_by(username=form.username.data).first()
        # Check if input password matches
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            print('Login Failure')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print('Redirect Index')
        return redirect(url_for('index'))
    print('Render Login Page')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Controller for logout
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    Controller for Index page
    """

    return render_template('index.html', title='Home')


@app.route('/reception', methods=['GET', 'POST'])
@login_required
def reception():
    """
    Controller for Reception page
    Get all appointments from a database and send it to a template
    """
    # AppointmentSchedule manages all appointments in a database
    scheduler = AppointmentSchedule()

    # scheduler.appointments is getter to retrieve all appointments
    return render_template('reception.html', title='Reception', appointments=scheduler.appointments)


@app.route('/make_appointment', methods=['GET', 'POST'])
@login_required
def make_appointment():
    """
    Controller for Making Appointment page
    """
    # Create form class
    form = AppointmentForm()
    # Get User instance for creating receptionist
    user = User.query.filter_by(username=current_user.username).first()
    # Create Receptionist instance
    receptionist = Receptionist(name=user.username, employee_num=user.employee_num)
    # Get next available date
    next_available_date = receptionist.find_next_available()

    # When submitting form data with POST method, the logic to make appointment runs
    # In other cases, render a template for an initial display
    if form.validate_on_submit():
        # This logic runs when submitting form data with POST method
        print('Making Appointment')
        # Get form data
        appointment_type = form.type.data
        staff_name = form.staff_name.data
        patient_name = form.patient_name.data
        patient_address = form.patient_address.data
        patient_phone = form.patient_phone.data
        appointment_day = form.date.data
        appointment_hour = form.time.data # One of the following is set in this field [9:00|11:00|14:00|16:00]
        # Generate appointment date from day and hour in input form data
        appointment_date = datetime(year=appointment_day.year, month=appointment_day.month, day=appointment_day.day, \
                                    hour=int(appointment_hour.split(':')[0]))
        print(f'Appointment type:{appointment_type}')
        print(f'Doctor:{staff_name} Patient:{patient_name}')
        print(f'date:{appointment_date}')

        # Validation
        # Check if the appointment date is available
        if appointment_date.date() < date.today() + timedelta(days=1):
            flash(f'Please select any day after tommorow. Next available date is {next_available_date}')
            return render_template('make_appointment.html', title='Make Appointment', form=form, next_available_date=next_available_date)

        # Check if the appointment date is available
        if not receptionist.check_available_date(date=appointment_date):
            flash(f'{appointment_date} is not available. Next available date is {next_available_date}')
            return render_template('make_appointment.html', title='Make Appointment', form=form, next_available_date=next_available_date)

        # Find doctor from database and create instance
        staff = receptionist.find_staff(name=staff_name)
        if staff is None:
            # If doctor is not found, return error message.
            flash('Cannot find the doctor. Please Confirm the name.')
            return render_template('make_appointment.html', title='Make Appointment', form=form, next_available_date=next_available_date)

        # Find patient from database and create instance
        patient = receptionist.find_patient(name=patient_name)
        if patient is None:
            # If patient is not found, insert a new record into database as a new patient
            patient = receptionist.add_patient(name=patient_name, address=patient_address, phone=patient_phone)

        # Make an appointment
        # Inserting a record into a database is performed
        receptionist.make_appointment(appointment_type=appointment_type, staff=staff, patient=patient, appointment_date=appointment_date)

        flash('Succeeded making appointment.')
        return redirect(url_for('reception'))

    return render_template('make_appointment.html', title='Make Appointment', form=form, next_available_date=next_available_date)


@app.route('/cancel_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def cancel_appointment(appointment_id):
    """
    Controller for canceling an appointment
    Delete the specified appointment from a database by using appointment_id in a parameter

    :param appointment_id:
    """
    # Get User instance for creating receptionist
    user = User.query.filter_by(username=current_user.username).first()
    # Create Receptionist instance
    receptionist = Receptionist(name=user.username, employee_num=user.employee_num)

    # Cancel appointment
    # Deleting a record from a database is performed
    receptionist.cancel_appointment(appointment_id=appointment_id)

    flash(f'Canceled appointment:{appointment_id}')
    return redirect(url_for('reception'))


@app.route('/prescription', methods=['GET', 'POST'])
@login_required
def prescription():
    """
    Controller for Prescription page
    Get all prescriptions from a database and send it to a template
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    prescriptions = Prescription.query.all()

    return render_template('prescription.html', title='Prescription', prescriptions=prescriptions)


@app.route('/issue_prescription', methods=['GET', 'POST'])
@login_required
def issue_prescription():
    """
    Controller for Issuing Prescription page
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('prescription'))

    # Create form class
    form = PrescriptionForm()

    # When submitting form data with POST method, the logic to issue prescription runs
    # In other cases, render a template for an initial display
    if form.validate_on_submit():
        # This logic runs when submitting form data with POST method
        print('Issuing Prescription')
        # Get form data
        prescription_type = form.type.data
        patient_name = form.patient_name.data
        quantity = form.quantity.data
        dosage = form.dosage.data

        # Validation
        # Find patient from database
        patient = doctor.find_patient(name=patient_name)
        if patient is None:
            flash(f'The patient you entered is not registered. Please register the patient.')
            return render_template('issue_prescription.html', title='Issue Prescription', form=form)

        # Issue prescription
        # Inserting a record into a database is performed
        doctor.issue_prescription(prescription_type=prescription_type, patient=patient, quantity=quantity, dosage=dosage)

        flash('Succeeded issue prescription.')
        return redirect(url_for('prescription'))

    form.doctor_name.data = doctor.name

    return render_template('issue_prescription.html', title='Issue Prescription', form=form)


@app.route('/cancel_prescription/<int:prescription_id>', methods=['GET', 'POST'])
@login_required
def cancel_prescription(prescription_id):
    """
    Controller for canceling a prescription
    Delete the specified prescription from a database by using prescription_id in a parameter

    :param prescription_id:
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('prescription'))

    # Cancel appointment
    # Deleting a record from a database is performed
    doctor.cancel_prescription(prescription_id=prescription_id)

    flash(f'Canceled prescription:{prescription_id}')
    return redirect(url_for('prescription'))


@app.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    """
    Controller for Reception page
    Get all patients from a database and send it to a template
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    patients = Patient.query.all()

    return render_template('patient.html', title='Manage Patient', patients=patients)


@app.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    """
    Controller for Registering Patient page
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    # Create form class
    form = PatientForm()

    # When submitting form data with POST method, the logic to register patient runs
    # In other cases, render a template for an initial display
    if form.validate_on_submit():
        # This logic runs when submitting form data with POST method
        print('Registering Prescription')
        # Get form data
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        doctor_name = form.doctor_name.data

        # Validation
        # Check if the name is already used
        patient = Patient.query.filter_by(name=name).first()
        if patient:
            flash(f'This name:{name} is already registered. Please confirm name or add any identifier to the name ')
            return render_template('register_patient.html', title='Register Patient', form=form)

        # Find doctor from database
        doctor = Doctor.query.filter_by(name=doctor_name).first()
        if doctor is None:
            flash(f'The doctor you entered is not registered.')
            return render_template('register_patient.html', title='Register Patient', form=form)

        # Check if the number of registered patients by a doctor
        # More than 500 is not allowed to be registered
        count = Patient.query.filter_by(doctor_id=doctor.id).count()
        print(count)
        if count >= 500:
            flash(f'Less than 500 patients can be registered by a doctor.')
            return render_template('register_patient.html', title='Register Patient', form=form)

        # Register patient
        # Inserting a record into a database is performed
        doctor.register_patient(name=name, address=address, phone=phone, doctor_id=doctor.id)

        flash('Succeeded register patient.')
        return redirect(url_for('patient'))

    return render_template('register_patient.html', title='Register Patient', form=form)


@app.route('/delete_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def delete_patient(patient_id):
    """
    Controller for deleting a patient
    Delete the specified patient from a database by using patient_id in a parameter

    :param patient_id:
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('prescription'))

    # Deleting a record from a database is performed
    doctor.delete_patient(patient_id=patient_id)

    flash(f'Deleted patient:{patient_id}')
    return redirect(url_for('patient'))


@app.route('/healthcare_pro', methods=['GET', 'POST'])
@login_required
def healthcare_pro():
    """
    Controller for Healthcare Professional page
    Get all healthcare professionals from a database and send it to a template
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    healthcare_pros = HealthcareProfessional.query.all()

    return render_template('healthcare_pro.html', title='Manage Healthcare Professional', healthcare_pros=healthcare_pros)


@app.route('/register_healthcare_pro', methods=['GET', 'POST'])
@login_required
def register_healthcare_pro():
    """
    Controller for Registering Healthcare Professional page
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    form = HealthcareProfessionalForm()

    # When submitting form data with POST method, the logic to register healthcare professional runs
    # In other cases, render a template for an initial display
    if form.validate_on_submit():
        # This logic runs when submitting form data with POST method
        print('Registering Healthcare Professional')
        # Get form data
        name = form.name.data
        employee_type = form.type.data
        employee_num = form.employee_num.data

        # Check if the name is already used
        healthcare_pro = HealthcareProfessional.query.filter_by(name=name).first()
        if healthcare_pro:
            flash(f'This name:{name} is already registered. Please confirm name or add any identifier to the name ')
            return render_template('register_healthcare_pro.html', title='Register Healthcare Professional', form=form)

        # Validation
        # Check if the employee number is already used
        healthcare_pro = HealthcareProfessional.query.filter_by(employee_num=employee_num).first()
        if healthcare_pro:
            flash(f'This employee number:{employee_num} is already used.')
            return render_template('register_healthcare_pro.html', title='Register Healthcare Professional', form=form)

        # Inserting a record into a database is performed
        healthcare_pro = HealthcareProfessional(name=name, employee_type=employee_type, employee_num=employee_num)
        healthcare_pro.persist()

        flash('Succeeded register Healthcare Professional.')
        return redirect(url_for('healthcare_pro'))

    return render_template('register_healthcare_pro.html', title='Register Healthcare Professional', form=form)


@app.route('/delete_healthcare_pro/<int:healthcare_pro_id>', methods=['GET', 'POST'])
@login_required
def delete_healthcare_pro(healthcare_pro_id):
    """
    Controller for deleting a healthcare professional
    Delete the specified appointment from a database by using appointment_id in a parameter

    :param healthcare_pro_id:
    """
    # Authorization
    # Only doctor user is allowed to perform this operation.
    doctor = Doctor.query.filter_by(employee_num=current_user.employee_num).first()
    if doctor is None:
        flash(f'You are not authorized to perform this operation.')
        return redirect(url_for('index'))

    # Deleting a record from a database is performed
    healthcare_pro = HealthcareProfessional.query.filter_by(id=healthcare_pro_id).first()
    healthcare_pro.delete()

    flash(f'Deleted Healthcare Professional:{healthcare_pro_id}')
    return redirect(url_for('healthcare_pro'))