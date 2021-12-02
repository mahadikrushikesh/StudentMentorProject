from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    # path('', index, name='index'),
    path('register_user/', register_mentor, name='register_user'),
    path('register_student/', register_student, name='register_student'),
    path('login_user/', login_user, name='login_user'),
    path('post_question/', post_question, name='post_question'),
    path('get_all_questions/', get_all_questions, name='get_all_questions'),
    path('reply_to_question/', reply_to_question, name='reply_to_question'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
