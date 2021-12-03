# StudentMentorProject Python
REST-API-in-Django-using-Django-REST-Framework.
REST API in Django using Django REST Framework.

Python Version Django Version

This is an example project to illustrate an implementation of REST API in Django using Django REST Framework with multiple user types. In this Django app, teachers can upload and send marksheets of students. Students can see their marksheet if they are registered on the application or can download it directly from the email.

urls
Django REST API Root: http://127.0.0.1:8000/api/

Teachers Root: http://127.0.0.1:8000/teachers/

Admin Root: http://127.0.0.1:8000/admin/

Student Root: http://127.0.0.1:8000/

Running the Project Locally
First, clone the repository to your local machine:

git clone https://github.com/mahadikrushikesh/StudentMentorProject.git
Install the requirements:

pip install -r requirements.txt
Create the database:

python manage.py migrate
Finally, run the development server:

python manage.py runserver
The project will be available at 127.0.0.1:8000.
