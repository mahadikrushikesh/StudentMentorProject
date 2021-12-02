from .models import *
from rest_framework import serializers
import re


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    mentor = serializers.SlugRelatedField(queryset=Mentor.objects.all(), slug_field="id")

    class Meta:
        model = NewUser
        fields = ['mentor', 'email', 'password', 'password2', 'role', 'registration_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = NewUser(
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d{2,})(?=.*[@$!%*#?&]{2,})[A-Za-z\d@$!#%*?&]{12,}$"
        pattern = re.compile(regex)
        match = re.search(pattern, password)
        if not match:
            raise serializers.ValidationError({"message": "password should contain minimum 8 letters(1 Upper Case "
                                                          "letter), 2 numbers and 2 special "
                                                          "characters.", "status": False})
        if password != password2:
            raise serializers.ValidationError({"message": "passwords must match.", "status": False})
        # password_hash = make_password(password)
        # mentor = Mentor.objects.get(email=self.validated_data.pop("mentor"))
        user.mentor = self.validated_data['mentor']
        user.set_password(password)
        user.role = self.validated_data['role']
        user.is_active = True
        user.is_admin = False
        user.is_superuser = False
        user.save()
        # user = NewUser.object.create(mentor=mentor, **self.validated_data)
        return user


class MentorSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Mentor
        fields = ['email', 'password', 'password2', 'role', 'registration_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        user = Mentor(
            email=self.validated_data['mentor_email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d{2,})(?=.*[@$!%*#?&]{2,})[A-Za-z\d@$!#%*?&]{12,}$"
        pattern = re.compile(regex)
        match = re.search(pattern, password)
        if not match:
            raise serializers.ValidationError({"message": "password should contain minimum 8 letters(1 Upper Case "
                                                          "letter), 2 numbers and 2 special characters.", "status": False})
        if password != password2:
            raise serializers.ValidationError({"message": "passwords must match.", "status": False})
        # password_hash = make_password(password)
        user.set_password(password)
        user.role = self.validated_data['role']
        user.is_admin = True
        user.is_active = True
        user.is_superuser = False
        user.save()
        return user


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=NewUser.objects.all(), slug_field="id")
    mentor = serializers.SlugRelatedField(queryset=Mentor.objects.all(), slug_field="id")

    class Meta:
        model = Questions
        fields = ['user', 'mentor', 'question', 'reply', 'message', 'file_name', 'file', 'post_time', 'replied_time']

    def save(self):
        question = Questions(
            question=self.validated_data['question']
        )
        question.user = self.validated_data['user']
        question.mentor = self.validated_data['mentor']
        question.reply = self.validated_data['reply']
        question.message = self.validated_data['message']
        question.file_name = self.validated_data['file_name']
        question.file = self.validated_data['file']
        question.post_time = self.validated_data['post_time']
        question.replied_time = self.validated_data['replied_time']
        # question = Questions.objects.create(user=user, mentor=mentor, **validated_data)
        question.save()

        return question

    # def update(self, instance, validated_data):
    #     question = Questions(
    #         question__exact=self.validated_data['question'],
    #         user=self.validated_data['student'],
    #         mentor=self.validated_data['mentor']
    #     )
    #     question.reply = self.validated_data['reply']
    #     question.message = self.validated_data['message']
    #     question.file_name = self.validated_data['file_name']
    #     question.file = self.validated_data['file']
    #     question.post_time = self.validated_data['post_time']
    #     question.replied_time = self.validated_data['reply_time']
    #     question.save()
    #
    #     return question
