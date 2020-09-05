"""NotesSharingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('userlogin/',userlogin,name="userlogin"),
    path('adminlogin/',adminlogin,name="adminlogin"),
    path('signup/',signup1,name="signup"),
    path('adminhome/',adminhome,name="adminhome"),
    path('logout/',Logout,name="logout"),
    path('profile/',profile,name="profile"),
    path('changepassword/',changepassword,name="changepassword"),
    path('uploadnotes/',uploadnotes,name="uploadnotes"),
    path('viewmynotes/',viewmynotes,name="viewmynotes"),
    path('deletemynotes/<int:pid>',deletemynotes,name="deletemynotes"),
    path('viewusers/',viewusers,name="viewusers"),
    path('deleteusers/<int:pid>',deleteusers,name="deleteusers"),
    path('user_viewallnotes/',user_viewallnotes,name="user_viewallnotes"),
    path('admin_viewallnotes/',admin_viewallnotes,name="admin_viewallnotes"),
    path('rejectnotes/<int:pid>',rejectnotes,name="rejectnotes"),
    path('acceptnotes/<int:pid>',acceptnotes,name="acceptnotes"),
    path('admin_viewacceptednotes/',admin_viewacceptednotes,name="admin_viewacceptednotes"),
    path('admin_viewrejectednotes/',admin_viewrejectednotes,name="admin_viewrejectednotes"),
    path('admin_viewpendingnotes/',admin_viewpendingnotes,name="admin_viewpendingnotes"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
