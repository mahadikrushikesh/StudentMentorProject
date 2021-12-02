import datetime
import logging
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, is_password_usable
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import *
from .serializers import RegistrationSerializer, MentorSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger('views_logger')


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def register_mentor(request):
    """ This function is for to create User

    Method: POST
    :parameter
    {
    "email": "mentor@gmail.com",
    "password": "PASSWORD",
    "password2": "PASSWORD",
    "role": "mentor"
    }

    role will be "mentor" for mentor
    :rtype: String
    """
    response_data = {}
    role = request.data.get("role", None)
    if not role:
        value = None
        if role == "mentor":
            value = MentorSerializer
        if value:
            serializer = value(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                logger.info('Registering User ' + user.email)
                response_data["data"] = {"email": user.email, "role": user.role}
                response_data["status"] = True
                response_data["message"] = "User registered successfully"
            else:
                response_data = serializer.errors
                logger.error('error while creating User ' + serializer.errors)
        else:
            response_data["data"] = None
            response_data["status"] = False
            response_data["message"] = "Please provide correct role for mentor"
    else:
        response_data["data"] = None
        response_data["status"] = False
        response_data["message"] = "Please provide role"
    return Response(response_data)


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def register_student(request):
    """ This function is for to create User

    Method: POST
    :parameter
    {
    "student_email": "xyz@gmail.com",
    "password": "PASSWORD",
    "password2": "PASSWORD",
    "mentor_email": "mentor@gmail.com",
    "role": "student"
    }

    role will be "student" for a student
    :rtype: String
    """
    response_data = {}
    role = request.data.get("role", None)
    if request.user.is_authenticated:
        if role:
            value = None
            if role == "student":
                value = RegistrationSerializer
            if value:
                email = request.data.get("mentor_email", None)
                mentor = Mentor.objects.get(email=email)
                data = {"mentor": mentor.pk,
                        "email": request.data.get("student_email"),
                        "password": request.data.get("password"),
                        "password2": request.data.get("password2"),
                        "mentor_email": email,
                        "role": "student"}
                serializer = value(data=data)
                if serializer.is_valid():
                    user = serializer.save()
                    # user = NewUser.objects.create(**data)
                    logger.info('Registering User ' + user.email)
                    response_data["data"] = {"email": user.email, "role": user.role}
                    response_data["status"] = True
                    response_data["message"] = "User registered successfully"
                else:
                    response_data = serializer.errors
                    logger.error('error while creating User ' + mentor.email)
            else:
                response_data["data"] = None
                response_data["status"] = False
                response_data["message"] = "Invalid role"
        else:
            response_data["data"] = None
            response_data["status"] = False
            response_data["message"] = "Please provide role"
    else:
        response_data["data"] = None
        response_data["status"] = False
        response_data["message"] = "You are not logged in, please do login first"
    return Response(response_data)


@api_view(['POST', ])
@permission_required([IsAuthenticated])
def login_user(request):
    """ This function is for to logged in user based on given credentials

    Method: POST
        :parameter
        {
        "email": "xyz@gmail.com",
        "password": "PASSWORD",
        "role": "mentor"
        }

        role will be in option ["student", "mentor"]
        :rtype: JSON
    """
    response = {"data": None, "status": False, "message": ""}
    email = request.data.get("email", None)
    password = request.data.get("password", None)
    role = request.data.get("role", None)
    print(email, password)
    if email and password:
        value = None
        if role == "mentor":
            value = Mentor
        elif role == "student":
            value = NewUser
        if value:
            try:
                user = value.objects.get(email=email)
                if check_password(password, user.password):
                    print("log in ")
                    auth.login(request, user)
                    data = {"user_email": user.email, "token": user.token, "login_time": datetime.now().strftime('%d %b %Y %H:%M %p'),
                            "registration_date": user.registration_date.strftime('%d %b %Y %H:%M %p')}
                    logger.info('User logged in  ' + user.email)
                    response["data"] = data
                    response["status"] = True
                    response["message"] = "logged in successfully"
                else:
                    response["data"] = None
                    response["status"] = False
                    response["message"] = "failed to login, Invalid password"
            except value.DoesNotExist:
                response["data"] = None
                response["status"] = False
                response["message"] = "failed to login, Invalid username"
                logger.error('error User log in  ' + email)
        else:
            response["data"] = None
            response["status"] = False
            response["message"] = "please provide correct role"
    else:
        response["data"] = None
        response["status"] = False
        response["message"] = "Please provide all parameters"
    return Response(response)


@api_view(['POST', ])
@login_required(login_url='/app/login_user/')
@permission_required([IsAuthenticated])
def post_question(request):
    """This function or API is for to post a question by user or student

    Method: POST
        :parameter
        {
        "student_email": "xyz@gmail.com",
        "mentor_email": "mentor@gmail.com",
        "question": "What is google?",
        "message": ""
        }

        Note: can attach file with this payload, "message" field is optional
        :rtype: JSON
    """
    response = {"data": None, "status": False, "message": ""}
    student_email = request.data.get("student_email", None)
    mentor_email = request.data.get("mentor_email", None)
    question = request.data.get("question", None)
    message = request.data.get("message", None)
    file = request.FILES.get("file", None)
    print(file)
    if request.user.is_authenticated:
        if student_email and question:
            try:
                user = NewUser.objects.get(email=student_email)
                mentor = Mentor.objects.get(email=mentor_email)
                dict_ = {"mentor": mentor.pk, "user": user.pk, "question": question, "message": message,
                         "reply": None, "file_name": file.name if file else None,
                         "file": file, "post_time": datetime.now(), "replied_time": None}
                serializer = QuestionSerializer(data=dict_)
                if serializer.is_valid():
                    data = serializer.save()
                    # data = Questions.objects.create(user=user, mentor=mentor, **dict_)
                    logger.info('post student question  ' + user.email)
                    response["data"] = {"question": data.question, "student_email": data.user.email,
                                        "mentor_email": data.mentor.email}
                    response["status"] = True
                    response["message"] = "Query Saved Successfully"
                else:
                    response = serializer.errors
            except ObjectDoesNotExist:
                logger.error('user not exist  ' + student_email)
                response["data"] = None
                response["status"] = False
                response["message"] = "User Not Found"
        else:
            response["data"] = None
            response["status"] = False
            response["message"] = "Please provide all parameters"
    else:
        response["data"] = None
        response["status"] = False
        response["message"] = "You are not logged in, please do login first"
    return Response(response)


@api_view(['POST', ])
@login_required(login_url='/app/login_user/')
@permission_required([IsAuthenticated])
def get_all_questions(request):
    """This API is for to show all questions based on user email ID

    Method: POST
    payload:
    {
    "email": "mentor@gmail.com"
    "role": "mentor"
    }

    :rtype: JSON
    :return:
    """
    response = {"data": None, "status": False, "message": ""}
    email = request.data.get("email", None)
    role = request.data.get("role", None)
    if request.user.is_authenticated:
        questions = None
        if role == "mentor":
            mentor = Mentor.objects.get(email=email)
            questions = Questions.objects.filter(mentor=mentor)
        elif role == "student":
            user = NewUser.objects.get(email=email)
            questions = Questions.objects.filter(user=user)
        if questions:
            question_list = []
            for question in questions:
                data = {"student_email": question.user.email, "mentor_email": question.mentor.email,
                        "question": question.question, "reply": question.reply, "attachment_name": question.file_name}
                question_list.append(data)
            if question_list:
                response["data"] = question_list
                response["status"] = True
                response["message"] = "data retrieved"
            else:
                response["data"] = None
                response["status"] = False
                response["message"] = "data not found"
        else:
            response["data"] = None
            response["status"] = False
            response["message"] = "there is no data associated with this email ID or provide correct role"
    else:
        response["data"] = None
        response["status"] = False
        response["message"] = "You are not logged in, please do login first"
    return Response(response)


@api_view(['POST', ])
@login_required(login_url='/app/login_user/')
@permission_required(['app.reply_question', IsAuthenticated])
def reply_to_question(request):
    """ This function is used for to reply to a particular student or user question

    Method: POST
        :parameter
        {
        "student_email": "xyz@gmail.com",
        "mentor_email": "mentor@gmail.com",
        "question": "What is google?",
        "reply": "search engine",
        "role": "mentor",
        "message": ""

        }

        Note: can attach file, "message" field is optional
        :rtype: JSON
    """
    response = {"data": None, "status": False, "message": ""}
    student_email = request.data.get("student_email", None)
    mentor_email = request.data.get("mentor_email", None)
    question = request.data.get("question", None)
    reply = request.data.get("reply", None)
    role = request.data.get("role", None)
    message = request.data.get("message", None)
    file = request.FILES.get("file", None)
    if request.user.is_authenticated:
        if role == "mentor":
            if student_email and mentor_email and question and reply:
                try:
                    user = NewUser.objects.get(email=student_email)
                    mentor = Mentor.objects.get(email=mentor_email)
                    question_obj = Questions.objects.get(user=user, mentor=mentor, question__exact=question)
                    question_obj.reply = reply
                    question_obj.message = message
                    question_obj.reply_time = datetime.now()
                    question_obj.file_name = file.name if file else None
                    question_obj.file = file
                    question_obj.save()
                    logger.info('replying to question by  ' + mentor.email)
                    response["data"] = {"student": user.email, "mentor": mentor.email, "question": question,
                                        "reply": reply}
                    response["status"] = True
                    response["message"] = "Replied to Query Successfully"
                except ObjectDoesNotExist:
                    logger.error('some one user is not exist ' + student_email + '  ' + mentor_email)
                    response["data"] = None
                    response["status"] = False
                    response["message"] = "User Not Found"
            else:
                response["data"] = None
                response["status"] = False
                response["message"] = "Please provide all parameters, reply can not be empty"
        else:
            response["data"] = None
            response["status"] = False
            response["message"] = "Students can not do reply to questions"
    else:
        response["data"] = None
        response["status"] = False
        response["message"] = "You are not logged in, please do login first"
    return Response(response)


@api_view(['POST', ])
@login_required(login_url='/app/login_user/')
@permission_required([IsAuthenticated])
def logout_view(request):
    """ This function is for To get logout user successfully

    :param request:
    :return:

    """
    response = {"data": None, "status": False, "message": ""}
    logout(request)
    response["data"] = request.user.email
    response["status"] = True
    response["message"] = "logged out Successfully"
    return Response(response)

