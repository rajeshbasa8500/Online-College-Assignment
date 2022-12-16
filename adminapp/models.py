from email.mime import image
from pydoc import describe
from re import T
from turtle import title
from django.db import models

# Create your models here.
# class TeacherRegisterModel(models.Model)
    
class AddCourseModel(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(help_text='course_name',max_length=50)
    branch_name = models.CharField(help_text='branch_name',max_length=50)
    
    class Meta:
        db_table='course_details'

class AddSubjectModel(models.Model):
    subject_id = models.AutoField(primary_key=True)
    course_name = models.CharField(help_text='course_name',max_length=50,null=True)
    branch_name = models.CharField(help_text='branch_name',max_length=50,null=True)
    subject_name = models.CharField(help_text='subject_name',max_length=50)
    shortcut_name = models.CharField(help_text='shortcut_name',max_length=50)
    code = models.CharField(help_text='code',max_length=50)
    
    class Meta:
        db_table='subject_details' 

class AnnouncementModel(models.Model):
    announcement_id= models.AutoField(primary_key=True)
    title = models.CharField(help_text="title",max_length=20)
    describe = models.CharField(help_text="describe",max_length=50)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    
    class Meta:
        db_table='announcement_details'
        
class TeacherRegistrationModel(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name= models.CharField(help_text="teacher_name",max_length=30)
    gender = models.CharField(help_text="gender",max_length=10)
    email = models.CharField(help_text="email",max_length=30)
    mobileno = models.BigIntegerField(help_text="mobileno",null=True)
    course = models.ForeignKey(AddCourseModel,models.CASCADE,null=True)
    subject = models.CharField(help_text="subject",max_length=80)
    password = models.CharField(help_text='password',max_length=18,null=True)
    teacher_otp = models.CharField(help_text='teacher_otp',max_length=18,null=True)
    tphoto = models.ImageField(null=True, blank=True)
    
    class Meta:
        db_table='teacher_details'
    
        
    
   
                   