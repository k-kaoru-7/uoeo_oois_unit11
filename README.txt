* About the Project
This project contains the application files for a local doctors' surgery system.
This system is for hospital's staffs. 
It is available to perform the below using this application.

- Manage appointments
- Issue prescriptions
- Manage patiens' information
- Manage healthcare staffs' information

* Design Concept
・Architecture
The system is designed based on Web Application Architecture by using Flask as a framework.
MVC model is basically adopted in the design as below. (Actually, it is nealy MVC model.)

- Model
 This performs data access and business logics.
 ORM(Object-relational mapping) is used to interact with a database.

- View
 This performs user interface, which is called templates in Flask application.
 It includes UI components such as forms or buttons that users can see.

- Controller
 Controller is a connecter between Model and View. 
 It accepts input data from View and manipulates Model.
 It also performs sending response to View.

The code is implemented according to Object Oriented Programming with Python.


・Structure
The structure of the project is the following.
root
├── surgery/
│   ├── __init__.py
│   ├── app.db
│   ├── templates/
│   │   ├── base.html
│   │   └── other html files that display each screen
│   ├── config.py
│   ├── forms.py
│   ├── models.py
│   └── routes.py
├── initialize.py
├── manage.py
├── test.py
└── requirements.txt

__init__.py
 This is used for initialization by Flask framework.

app.db
 This is a database files used in the application.
 SQLite is adopted as the database.
* This will be generated after the initialization of the application. See Usage section below.

templates/
 This includes html files used as View.
 base.html is a basic layout which is inherited by other View html.

models.py
 This defines classes that are used as Model.
 It performs manipulating a database and business logics.
 Sqlalchemy is used as ORM.

routes.py
 This defines Controller functions.
 It receives data from View through HTTP methods and manipulates Model or View classes.
 A part of validation of input data is conducted in Controller functions.

forms.py
 This defines form componets used in View and Controller.

config.py
 This includes configuration used in the application such as the database URI or a secret key.

initialize.py
 This is used to initialize the database settings. See Usage section below.
 
manage.py
 It runs the application.

test.py
 It includes test codes for the application.


* Functions
Users can perform the functions below by each screen.

・Reception page
 - Display a list of scheduled appointments
 - Make appointments based on users' requests
 - Cancel appointments

・Prescriotion page 
 * Only doctor user is allowd to access this page
 - Display a list of issued prescriptions
 - Issue prescriotions
 - Cancel prescriptions
 
 
・Patient page
 * Only doctor user is allowd to access this page
 * Less than 500 patients can be registered by each doctor
 - Display a list of registered patients
 - Register patient information
 - Delete patient information

・Healthcare Professional page
 * Only doctor user is allowd to access this page
 - Display a list of healthcare professionals
 - Register healthcare professional information
 - Delete healthcare professional information


* Authorization
Users must sign in to access the application.
Employee type is assigned to each user, doctor or nurse.
Only doctor is authorized to manage prescription, patient, healthcare professional information.


* Usage
Setup environments and initialize the application first.

1.Install libralies
$ pip install -r requirements.txt

2.Setup a database
$ flask db init
$ flask db migrate -m "create tables"
$ flask db upgrade

app.db is generated after this operation.

3.Initialize tables(Add user information)
$ python initialize.py user

User infromation to sign in and operate functions is registered.
Initial Username:David
Initial Password:cat

To clean a database environment, run this command.
But be careful since all tables are deleted from a database.
$ python initialize.py drop

4.Run the application
$ python manage.py

Now, you can access the application's top page.
Access http://127.0.0.1:5000/ with your browser.


* Contact
Kaoru Kitamura
University email address: kk21053@essex.ac.uk
