# StudentMentorProject Python
REST-API-in-Django-using-Django-REST-Framework.
REST API in Django using Django REST Framework.

Python Version Django Version

This is an example project to illustrate an implementation of JWT token authentication REST for a user API in Django using Django REST Framework with multiple user types. In this Django app, mentor and students can post a question with file attachment but only mentor can gives reply to question.

First createsuperuser and then register Mentor and access API's

urls
JWT Token Creation  http://127.0.0.1:8000/api/token/
JWT Token Refresh  http://127.0.0.1:8000/api/token/refresh/

Note:
Generated Auth token is valid for 1 hour you have refresh token with this Root: http://127.0.0.1:8000/api/token/refresh/
then token should be sent with every API through Postman In Authentication tab as a bearer token 

Django REST API Root: http://127.0.0.1:8000/app/

Mentor Registration  Root: http://127.0.0.1:8000/app/register_user/
Mentor/student post question   Root: http://127.0.0.1:8000/app/post_question/
Mentor Reply to question  Root: http://127.0.0.1:8000/app/reply_to_question/

get all question based on login user  Root: http://127.0.0.1:8000/app/get_all_questions/

Admin Root: http://127.0.0.1:8000/admin/

Student Registration  Root: http://127.0.0.1:8000/app/register_student/
User logout  Root: http://127.0.0.1:8000/app/logout/

Running the Project Locally
First, clone the repository to your local machine:

git clone https://github.com/mahadikrushikesh/StudentMentorProject.git
Install the requirements:

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
Finally, run the development server:

python manage.py runserver
The project will be available at 127.0.0.1:8000.
