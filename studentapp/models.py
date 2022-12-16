from email.mime import image
from re import T
from django.db import models
from adminapp.models import AddCourseModel
from teacherapp.models import AddAssignmentModel
 
# Create your models here.
class StudentRegisterModel(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(help_text='student_name',max_length=50)
    student_rollno = models.CharField(help_text='student_rollno',max_length=20)
    course = models.ForeignKey(AddCourseModel,models.CASCADE,null=True)
    student_mobileno = models.BigIntegerField(help_text='student_mobileno',null=True)
    student_email = models.CharField(help_text='student_email', max_length=30)
    student_password = models.CharField(help_text='student_password',max_length=18)
    student_otp = models.CharField(help_text='student_otp',max_length=18,null=True)
    student_photo = models.FileField(upload_to='documents/',null=True)
    
    class Meta:
        db_table='student_detail'

class Assignment_SubmitModel(models.Model):
    submit_id = models.AutoField(primary_key=True)
    submited_student = models.ForeignKey(StudentRegisterModel,models.CASCADE,null=True)
    assign = models.ForeignKey(AddAssignmentModel,models.CASCADE,null=True)
    text = models.CharField(help_text='text',max_length=80)
    myfile = models.FileField(upload_to='documents/',null=True)
    submited_date = models.DateField(auto_now_add=True, null=True)
    submit_status = models.CharField(help_text='submit_status',max_length=20,default='pending')
    
    class Meta:
        db_table='assignmentsubmit_detail'
    
class ResultModel(models.Model):
    result_id = models.AutoField(primary_key=True)
    stu = models.ForeignKey(Assignment_SubmitModel, models.CASCADE,null=True)
    remarks = models.CharField(help_text='remarks', max_length=20)
    marks = models.IntegerField(help_text='marks')
    #result_status = models.CharField(help_text='result_status',max_length=20,default='pending')
    class Meta:
        db_table = 'teacher_result'
    