import sys
from surgery.models import User, Doctor
from surgery import db


"""
This scripts is used for initializing a database

[Usage]
python initialize.py drop
 ->Drop all tables on a database
python initialize.py user
 ->Insert an initial user and doctor into a database
"""


def add_doctor():
    """
    Insert an doctor into doctor table
    """
    doctor = Doctor(name='David', employee_num='DC001', employee_type='doctor')
    db.session.add(doctor)
    db.session.commit()

    doctors = Doctor.query.all()
    for doctor in doctors:
        print(doctor.employee_num, doctor.name)


def add_user():
    """
    Insert an user into user table
    """
    user = User(username='David', employee_num='DC001')
    user.set_password('cat')
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.employee_num, user.username)


def drop_all():
    """
    Drop all tables
    """
    db.drop_all()


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'user':
        add_doctor()
        add_user()
    elif mode == 'drop':
        drop_all()