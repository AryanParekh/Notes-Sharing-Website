from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    def newsave(self):
        user=User(username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'])
        password=self.validated_data['password']
        user.set_password(password)
        user.save()
        user_signup=Signup.objects.create(user=user,
                                        contact=self.validated_data['contact'],
                                        branch=self.validated_data['branch'],
                                        role=self.validated_data['role'])
        user_signup.save()
        return user

    contact = serializers.CharField(max_length=10,default='')
    branch = serializers.CharField(max_length=30,default='')
    role = serializers.CharField(max_length=15,default='')

    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'password' , 'contact' , "branch","role")

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ('id','user','uploadingdate', 'branch', 'subject', 'notesfile' ,'filetype', 'description' , 'status')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)
    password = serializers.CharField(style={"input_type": "password"})
