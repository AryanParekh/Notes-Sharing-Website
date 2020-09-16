from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from django.shortcuts import get_object_or_404

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
                last_name=last_name
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
        u= User.objects.filter(username=request.user.username).first()
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
    user = User.objects.get(id=request.user.id)
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
