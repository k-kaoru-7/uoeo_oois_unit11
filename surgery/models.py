from surgery import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time, timedelta


"""
This script defines Model classes
Model classes perform manipulating a database and business logics
For manipulating a database, sqlalchemy is used as ORM
"""


class User(UserMixin, db.Model):
    """
    User class that represents the system users
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    employee_num = db.Column(db.String(5), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str):
        """
        Generate a hash for hiding password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        """
        Check if input password matches
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Patient(db.Model):
    """
    Class that represents patients
    Created by Doctor class
    """
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    address = db.Column(db.String(64))
    phone = db.Column(db.String(15))
    # This is used to be associated with HealthcareProfessional staff
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    appointment = db.relationship('Appointment', backref='patient', lazy='dynamic', \
                                  primaryjoin="Patient.id == Appointment.patient_id")
    prescription = db.relationship('Prescription', backref='patient', lazy='dynamic', \
                                  primaryjoin="Patient.id == Prescription.patient_id")
    # This is used to record when the patient is registered, set by default when creating instance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def persist(self):
        """
        Inserting a record into a database is performed
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deleting a record from a database is performed
        """
        db.session.delete(self)
        db.session.commit()


class Prescription(db.Model):
    """
    Class that represents prescription
    Created by Doctor class
    """
    __tablename__ = 'prescription'

    id = db.Column(db.Integer, primary_key=True)
    # This represents prescription type.
    type = db.Column(db.String(12))
    # This is used to be associated with patient
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    # This is used to be associated with Doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    # This is quantity of medicine
    quantity = db.Column(db.Integer)
    # This is dosage of medicine
    dosage = db.Column(db.Float)
    # This is used to record when the prescription is registered, set by default when creating instance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def persist(self):
        """
        Inserting a record into a database is performed
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deleting a record from a database is performed
        """
        db.session.delete(self)
        db.session.commit()


class HealthcareProfessional(db.Model):
    """
    Class that represents HealthcareProfessional staff
    """
    __tablename__ = 'healthcare_pro'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    employee_num = db.Column(db.String(5), index=True, unique=True)
    employee_type = db.Column(db.String(20))
    appointment = db.relationship('Appointment', backref='healthcare_pro', lazy='dynamic', \
                                  primaryjoin="HealthcareProfessional.id == Appointment.staff_id")
    # This is used to record when the healthcare_pro is registered, set by default when creating instance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity':'healthcare_pro',
        'polymorphic_on':employee_type
    }

    def persist(self):
        """
        Inserting a record into a database is performed
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deleting a record from a database is performed
        """
        db.session.delete(self)
        db.session.commit()

    # I did not implement a concrete logic as it is not the essence of this assignment
    def conduct_consultation(self) -> str:
        return 'The resulf of consultation'


class Doctor(HealthcareProfessional):
    """
    Class that represents doctors, inheriting HealthcareProfessional class.
    """
    __tablename__ = 'doctor'

    id = db.Column(db.Integer, db.ForeignKey('healthcare_pro.id'), primary_key=True)
    patient = db.relationship('Patient', backref='doctor', lazy='dynamic', \
                                  primaryjoin="Doctor.id == Patient.doctor_id")
    prescription = db.relationship('Prescription', backref='doctor', lazy='dynamic', \
                                  primaryjoin="Doctor.id == Prescription.doctor_id")

    __mapper_args__ = {
        'polymorphic_identity':'doctor',
    }

    def find_patient(self, name) -> Patient:
        """
        Find patient by the name and create instance.
        :param name:

        :return:
         patinet: Patient
        """
        patient = Patient.query.filter_by(name=name).first()

        return patient

    def register_patient(self, name: str, address: str, phone: str, doctor_id: int):
        """
        Register patient and insert into Database

        :param name:
        :param address:
        :param phone:
        :param doctor_id:
        """
        patient = Patient(name=name, address=address, phone=phone, doctor_id=doctor_id)
        patient.persist()

    def delete_patient(self, patient_id: int):
        """
        Delete the specified patient and delete from database

        :param patient_id:
        """
        patient = Patient.query.filter_by(id=patient_id).first()
        patient.delete()

    def issue_prescription(self, prescription_type: str, patient: Patient, quantity: int, dosage: float):
        """
        Issue prescription and Insert into Database

        :param prescription:
        :return:
        """
        prescription = Prescription(type=prescription_type, doctor_id=self.id, patient_id=patient.id, \
                                    quantity=quantity, dosage=dosage)
        prescription.persist()

    def cancel_prescription(self, prescription_id: int):
        """
        Cancel the specified prescription and delete from database
        :param prescription_id:

        """
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        prescription.delete()


class Nurse(HealthcareProfessional):
    """
    Class that represents doctors, inheriting HealthcareProfessional class.
    """
    __tablename__ = 'nurse'

    id = db.Column(db.Integer, db.ForeignKey('healthcare_pro.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'nurse',
    }


class Appointment(db.Model):
    """
    Class that represents patients
    Created by Receptionist class
    """
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    # This represents appointment type. Should select the below.
    # Consultation/Prescription/Surgery
    type = db.Column(db.String(12))
    # This is used to be associated with HealthcareProfessional
    staff_id = db.Column(db.Integer, db.ForeignKey('healthcare_pro.id'))
    # This is used to be associated with patient
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    # Appointment date
    date = db.Column(db.DateTime)
    # This is used to record the name of the receptionist making appointment
    created_by = db.Column(db.String(32))
    # This is used to record when the appointment is made, set by default when creating instance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def persist(self):
        """
        Inserting a record into a database is performed
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deleting a record from a database is performed
        """
        db.session.delete(self)
        db.session.commit()


"""
The below is classes mainly for business logic
These are not migrated into a database
"""
class AppointmentSchedule(object):
    """
    Model class that manages the schedule of appointments
    """
    def __init__(self):
        # Get all appointments from a database
        self.__appointments: list[Appointment] = Appointment.query.all()

    @property
    def appointments(self):
        """
        Getter for an instance value

        :return:
         self.__appointments: Appointment
        """
        return self.__appointments

    def add_appointment(self, appointment: Appointment):
        """
        Add a new appointment and insert into database

        :param appointment:
        """
        # Inserting a record into a database is performed
        appointment.persist()

        self.__appointments = Appointment.query.all()

    def cancel_appointment(self, appointment: Appointment):
        """
        Cancel the specified appointment and delete from database

        :param appointment_id
        """
        # Deleting a record from a database is performed
        appointment.delete()
        # remove the record from the appointment list(instance value)
        self.__appointments.remove(appointment)

    def find_next_available(self) -> datetime:
        """
        Find the next available date for appointment

        :return:
         next_available_date: datetime
        """
        scheduled_dates: list[datetime] = []
        # Hours available for appointment
        appointment_hours: list[int] = [9, 11, 14, 16]
        # Initialize next possible date
        next_available_date = date.today() + timedelta(days=1)
        next_available_date = datetime.combine(next_available_date, time())
        next_available_date = next_available_date.replace(hour=appointment_hours[0])

        if not self.__appointments:
            return next_available_date

        # Make list for scheduled dates of appointments
        for appointment in self.__appointments:
            scheduled_dates.append(appointment.date)

        # Sort by date
        scheduled_dates.sort()

        '''
        Iterate scheduled_dates, appointment_hours and next_possible_date
        Check if it matches next_possible_date.
        If matched, pass. If not matched, return next_possible_date as the next available date.
        '''
        while True:
            for dt in scheduled_dates:
                for h in appointment_hours:
                    next_available_date = next_available_date.replace(hour=h)
                    if next_available_date == dt:
                        continue
                    else:
                        return next_available_date

                next_available_date = next_available_date + timedelta(days=1)

    def is_date_available(self, date: datetime) -> bool:
        """
        Check if the input date is available

        :param date:
        :return:
         True: Available
         False: Unavailable
        """
        appointment = Appointment.query.filter_by(date=date).first()
        if appointment:
            return False
        else:
            return True


class Receptionist(object):
    """
    Model class for reception
    This class performing making an appointment and canceling
    """
    def __init__(self, name: str, employee_num: str):
        self.__name = name
        self.__employee_num = employee_num
        self.__scheduler = AppointmentSchedule()

    def find_staff(self, name) -> HealthcareProfessional:
        """
        Find doctor by the name.
        :param name:

        :return:
         staff: HealthcareProfessional
        """
        staff = HealthcareProfessional.query.filter_by(name=name).first()

        return staff

    def find_patient(self, name) -> Patient:
        """
        Find patient by the name and create instance.
        :param name:

        :return:
         patinet: Patient
        """
        patient = Patient.query.filter_by(name=name).first()

        return patient

    def add_patient(self, name, address, phone) -> Patient:
        """
        Add a new patient into database.
        :param name:
        :param address:
        :param phone:

        :return:
         patinet: Patient
        """
        patient = Patient(name=name, address=address, phone=phone)
        patient.persist()

        return patient

    def make_appointment(self, appointment_type: str, staff: HealthcareProfessional, patient: Patient, \
                         appointment_date: datetime) -> Appointment:
        """
        Make a new appointment by using AppointmentSchedule.
        :param appointment_type:
        :param staff:
        :param patient:
        """
        appointment = Appointment(type=appointment_type, staff_id=staff.id, patient_id=patient.id, \
                                  created_by=self.__name, date=appointment_date)
        self.__scheduler.add_appointment(appointment)

        return appointment

    def cancel_appointment(self, appointment_id: int):
        """
        Cancel the specified appointment by using AppointmentSchedule.

        :param appointment:
        """
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        self.__scheduler.cancel_appointment(appointment)

    def find_next_available(self) -> datetime:
        """
        Find next available date

        :return:
         next available date
        """
        return self.__scheduler.find_next_available()

    def check_available_date(self, date: datetime) -> bool:
        """
        Check if input date is available for the appointment

        :param date:
        :return:
         True:available
         False:unavailable
        """
        return self.__scheduler.is_date_available(date=date)