from surgery import app, db
from surgery.models import User, Patient, Appointment, HealthcareProfessional

# Run the application
app.run(host='127.0.0.1', port=5000, debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}