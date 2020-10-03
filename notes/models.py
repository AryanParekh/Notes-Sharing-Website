from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    BRANCH_CHOICE=[('Computer Science','Computer Science'),('Mechanical','Mechanical'),('Electrical','Electrical'),('Electronics','Electronics')]
    branch = models.CharField(max_length=30,choices=BRANCH_CHOICE,default='Computer Science')
    role = models.CharField(max_length=15,choices=[('Student','Student'),('Teacher','Teacher')],default='Student')

    def __str__(self):
        return self.user.username

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.DateField()
    BRANCH_CHOICE=[('Computer Science','Computer Science'),('Mechanical','Mechanical'),('Electrical','Electrical'),('Electronics','Electronics')]
    branch = models.CharField(max_length=30,choices=BRANCH_CHOICE,default='Computer Science')
    subject = models.CharField(max_length=30)
    notesfile = models.FileField()
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=215,null=True)
    status = models.CharField(max_length=15,choices=[('accepted','accepted'),('rejected','rejected'),('pending','pending')],default='pending')

    def __str__(self):
        return self.user.username+" "+self.status

class Assignments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.DateField()
    uploadingtime = models.DateField()
    BRANCH_CHOICE=[('Computer Science','Computer Science'),('Mechanical','Mechanical'),('Electrical','Electrical'),('Electronics','Electronics')]
    branch = models.CharField(max_length=30,choices=BRANCH_CHOICE,default='Computer Science')
    subject = models.CharField(max_length=30)
    notesfile = models.FileField()
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=215,null=True)
    teacher=models.CharField(max_length=30,default='none')
    comments= models.CharField(max_length=254,null=True)
    marks = models.CharField(max_length=10)
    status = models.CharField(max_length=15,choices=[('checked','checked'),('unchecked','unchecked')],default='unchecked')

    def __str__(self):
        return self.user.username+" "+self.status+" Assignment"
