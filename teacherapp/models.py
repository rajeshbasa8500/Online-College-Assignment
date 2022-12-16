from email.mime import image
from re import T
from unittest import result
from unittest.util import _MAX_LENGTH
from django.db import models
from adminapp.models import AddCourseModel, TeacherRegistrationModel
# from pytz import timezone
from datetime import date

# Create your models here.


class AddAssignmentModel(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    Assignment_details = models.ForeignKey(TeacherRegistrationModel, models.CASCADE, null=True)
    course = models.ForeignKey(AddCourseModel, models.CASCADE, null=True)
    subject = models.CharField(help_text='subject', max_length=50)
    assignment_title = models.CharField(help_text='assignment_title', max_length=40)
    assignment_description = models.CharField(help_text='assignment_description', max_length=50)
    posting_date = models.DateField(auto_now_add=True, null=True)
    last_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    assignment_marks = models.IntegerField(help_text='assignment_marks')
    assignment_file = models.FileField(upload_to='documents/', null=True)
    # accept = models.CharField(help_text='accept',max_length=40,null=True)
    class Meta:
        db_table = 'assignment_details'




