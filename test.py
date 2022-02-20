from surgery.models import Patient
from surgery import db

"""
Test scripts to insert 500 records into patient table
"""


def add_patient():
    for count in range(500):
        patient = Patient(name=f'Test{count+1}', address='Test', phone='123456789', doctor_id=1)
        db.session.add(patient)
        db.session.commit()


if __name__ == '__main__':
    add_patient()