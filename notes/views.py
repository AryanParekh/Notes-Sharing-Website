from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics,mixins
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import authentication_classes,permission_classes


# Create your views here.
def home(request):
    return render(request,'home.html')

def userlogin(request):
    error=""
    if request.method == 'POST':
        email_id= request.POST['emailid']
        pass_word= request.POST['pwd']
        user = authenticate(username=email_id,password=pass_word)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error = "yes"
    d= {'error':error}
    return render(request,'userlogin.html',d)

def adminlogin(request):
    error=""
    if request.method == 'POST':
        user_name= request.POST['uname']
        pass_word= request.POST['pwd']
        user = authenticate(username=user_name,password=pass_word)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error = "yes"
    d= {'error':error}
    return render(request,'adminlogin.html',d)

def signup1(request):
    error=""
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        emailid=request.POST.get('emailid')
        password=request.POST.get('password')
        contact=request.POST.get('contact')
        branch=request.POST.get('branch')
        role=request.POST.get('role')
        try:
            user= User.objects.create_user(
                username=emailid,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            user.save()
            user_additional_data=Signup.objects.create(
                user=user,
                contact=contact,
                branch=branch,
                role=role
            )
            user_additional_data.save()
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)

def adminhome(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes=Notes.objects.all()
    pending=0
    accepted=0
    rejected=0
    for i in notes:
        if i.status=='pending':
            pending=pending+1
        elif i.status=='accepted':
            accepted=accepted+1
        elif i.status=='rejected':
            rejected=rejected+1
    d={'a':accepted,'p':pending,'r':rejected,'t':accepted+pending+rejected}
    return render(request,'adminhome.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None
    try:
        data = Signup.objects.get(user=user)
    except Signup.DoesNotExist:
        data = None
    d={'user':user,'data':data}
    return render(request,'profile.html',d)

def changepassword(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('userlogin')
    if request.method=='POST':
        o=request.POST.get('old')
        n=request.POST.get('new')
        c=request.POST.get('confirm')
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'changepassword.html',d)

def uploadnotes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error=""
    if request.method=='POST':
        b=request.POST.get('branch')
        s=request.POST.get('subject')
        n=request.FILES.get('notesfile')
        f=request.POST.get('filetype')
        d=request.POST.get('description')
        u=Signup.objects.filter(user=request.user).first()
        try:
            user= Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,filetype=f,description=d,status='pending')
            user.save()
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'uploadnotes.html',d)

def viewmynotes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user=Signup.objects.filter(user=request.user).first()
    notes = Notes.objects.filter(user=user)
    d={'notes':notes}
    return render(request,'viewmynotes.html',d)

def deletemynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('viewmynotes')

def viewusers(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    users = Signup.objects.all()
    d={'users':users}
    return render(request,'viewusers.html',d)

def deleteusers(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    users=User.objects.get(id=pid)
    users.delete()
    return redirect('viewusers')

def user_viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'user_viewallnotes.html',d)

def admin_viewallnotes(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'admin_viewallnotes.html',d)

def rejectnotes(request,pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes = Notes.objects.get(id=pid)
    notes.status='rejected'
    notes.save()
    return redirect('admin_viewallnotes')

def acceptnotes(request,pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes = Notes.objects.get(id=pid)
    notes.status='accepted'
    notes.save()
    return redirect('admin_viewallnotes')

def admin_viewacceptednotes(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'admin_viewacceptednotes.html',d)

def admin_viewrejectednotes(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'admin_viewrejectednotes.html',d)

def admin_viewpendingnotes(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'admin_viewpendingnotes.html',d)


# SERIALIZER views

@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def User_list(request):
    if request.method=="GET":
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        data=[]
        for a in serializer.data:
            d={}
            d.update({'id':a['id']})
            d.update({'username':a['username']})
            d.update({'first_name':a['first_name']})
            d.update({'last_name':a['last_name']})
            data.append(d)
        return Response(data)

    elif request.method=="POST":
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.newsave()
            token=Token.objects.create(user=user)
            data={
                'id':user.id,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'password':user.password,
                'token':token.key
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def User_detail(request,pk):
    try:
        user=User.objects.get(pk=pk)
        user_signup=Signup.objects.filter(user=user).first()
        token,_=Token.objects.get_or_create(user=user)

    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        serializer=UserSerializer(user)
        data={}
        if user_signup!=None:
            u=serializer.data
            data={
                'id':u['id'],
                'username':u['username'],
                'first_name':u['first_name'],
                'last_name':u['last_name'],
                'password':u['password'],
                'contact':user_signup.contact,
                'branch':user_signup.branch,
                'role':user_signup.role,
                'token':token.key
            }
        else:
            data=serializer.data
        return Response(data)

    elif request.method=="DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class Notes_list(APIView):
#     def get(self,request):
#         notes=Notes.objects.all()
#         serializer=NotesSerializer(notes,many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer=NotesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Notes_list(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class= NotesSerializer
    queryset=Notes.objects.all()

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Notes_detail(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class= NotesSerializer
    queryset=Notes.objects.all()
    lookup_field='id'

    def get(self,request,id):
        return self.retrieve(request)

    def put(self,request,id):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)

class Login1(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            token =Token.objects.get(user=user)
            user_signup=Signup.objects.filter(user=user).first()
            notes=Notes.objects.filter(user=user_signup)
            notes_data=[]
            if (notes!=None):
                for note in notes:
                    d={
                        'id':note.id,
                        'user':note.user.user.username,
                        'uploadingdate':note.uploadingdate,
                        'branch':note.branch,
                        'subject':note.subject,
                        'notesfile':note.notesfile.url,
                        'filetype':note.filetype,
                        'description':note.description,
                        'status':note.status,
                    }
                    notes_data.append(d)
            login(request, user)
            data={
                'id':user.id,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'password':user.password,
                'contact':"" if user_signup==None else user_signup.contact,
                'branch':"" if user_signup==None else user_signup.branch,
                'role':"" if user_signup==None else user_signup.role,
                'notes':notes_data,
                'token':token.key
            }
            return Response(data)
        else:
            data = {"Message": "There was error authenticating"}
            return JsonResponse(data)

class Verified_Notes_list(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class= NotesSerializer
    queryset=Notes.objects.filter(status='accepted')

    def get(self,request):
        return self.list(request)
