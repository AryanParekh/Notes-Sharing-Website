from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField()
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=215,null=True)
    status = models.CharField(max_length=15,default='pending')

    def __str__(self):
        return self.user.username+" "+self.status

class Assignments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=10)
    uploadingtime = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField()
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=215,null=True)
    comments= models.CharField(max_length=254,null=True)
    marks = models.CharField(max_length=10)
    status = models.CharField(max_length=15,default='pending')

    def __str__(self):
        return self.user.username+" "+self.status+" Assignment"
