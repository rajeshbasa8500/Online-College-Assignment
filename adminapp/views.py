from ast import Add
from distutils.log import error
from email.headerregistry import Address
from fileinput import close
from re import A
from ssl import ALERT_DESCRIPTION_UNEXPECTED_MESSAGE
from unittest import result
from wsgiref.util import request_uri
from xml.etree.ElementTree import QName
from django.shortcuts import redirect, render
from adminapp.models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from studentapp.models import Assignment_SubmitModel, ResultModel, StudentRegisterModel
from onlineassignment.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from studentapp.views import studnet_submit_assignments
from teacherapp.models import AddAssignmentModel
from django.db.models import Q
# Create your views here.


def admin_login(request):
    print('get')
    if request.method == "POST":
        print('post')
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email == "admin" and password == "admin":
            messages.info(request, "Login Successfully.")
            return redirect("admin_dashboard")
            
        else:
            messages.error(request,"Invalid EmailID or Password")
            return redirect("admin_login")
    return render(request, 'main/admin-login.html')


def admin_logout(request):
    # messages.info(request, 'Logout Successfully.')
    return redirect('index')


def admin_dashboard(request):
    a = AddCourseModel.objects.all().count()
    c = AddSubjectModel.objects.all().count()
    d = TeacherRegistrationModel.objects.all().count()
    b = TeacherRegistrationModel.objects.all()
    # messages.info(request, 'Login Successfully.')
    if request.method == 'POST'  :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        b=TeacherRegistrationModel.objects.filter(Q(teacher_name__contains=search)|Q(email__contains=search)|Q(mobilenoF__contains=search)|Q(course__branch_name__contains=search)|Q(subject__contains=search))
        print(b)
    return render(request, 'admin/admin-dashboard.html', {'a': a, 'b': b, 'c': c, 'd': d})


def admin_add_course(request):

    if request.method == 'POST':
        course_name = request.POST['coursename']
        branch_name = request.POST['branchname']

        AddCourseModel.objects.create(
            course_name=course_name, branch_name=branch_name)
        messages.info(request,"Course Added Successfully")
        return redirect("admin_dashboard")
    c = AddCourseModel.objects.all()
    return render(request, 'admin/admin-course.html', {'c': c})


def admin_add_subject(request):
    r = AddCourseModel.objects.all()
    b = AddSubjectModel.objects.all()
    if request.method == 'POST':
        course_name = request.POST['coursename']
        branch_name = request.POST['branchname']
        subject_name = request.POST['subjectname']
        shortcut_name = request.POST['shortcutname']
        code = request.POST['code']
        AddSubjectModel.objects.create(course_name=course_name, branch_name=branch_name,
                                       subject_name=subject_name, shortcut_name=shortcut_name, code=code)
        messages.info(request,"Subject Added Successfully")
        return redirect('admin_dashboard')
    d = AddSubjectModel.objects.all()
    
    return render(request, 'admin/admin-subject.html', {'r': r, 'b': b, 'd': d})


def admin_add_teacher(request):
    a = AddCourseModel.objects.all()
    b = AddSubjectModel.objects.all()
    if request.method == "POST" and request.FILES['tphoto']:
        teacher_name = request.POST['teachername']
        gender = request.POST['gender']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        course_id = request.POST['course']
        subject = request.POST['subject']
        chars = 'abcdefghijklmnopqrstuvwxyz098764321'
        password = get_random_string(6, chars)
        print(password)
        teacher_otp = get_random_string(4, chars)
        print(teacher_otp)
        t_photo = request.FILES['tphoto']
        course = AddCourseModel.objects.get(course_id=course_id)
        print(course, "hi")

        teacher_register = TeacherRegistrationModel.objects.create(teacher_name=teacher_name, gender=gender, email=email, mobileno=mobileno, course=course,  subject=subject, password=password,teacher_otp=teacher_otp, tphoto=t_photo)

        html_content = "<br/>Dear Faculty, <br/>   Your Login Credentials are generated <b> <br> Username: </b> " + \
            str(email) + "<br> <b>Passwod: </b> " + str(password) + \
            "<br> from Onlineassignment  System.  <br>  Thank You For Your Registration."
        from_mail = DEFAULT_FROM_EMAIL
        to_mail = [teacher_register.email]
        # if send_mail(subject,message,from_mail,to_mail):
        msg = EmailMultiAlternatives(
            "Account Registered Status", html_content, from_mail, to_mail)
        msg.attach_alternative(html_content, "text/html")
        print(email)
        messages.info(request,"Teacher Added Successfully")
        return redirect("admin_dashboard")
    else:
        
        return render(request, 'admin/admin-add-teacher.html', {'a': a, 'b': b})


def admin_manage_teacher(request):
    a = TeacherRegistrationModel.objects.all()
    if request.method == 'POST' and 'btn' in request.POST :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        a = TeacherRegistrationModel.objects.filter(Q(teacher_id__contains=search)|Q(teacher_name__contains=search)|Q(email__contains=search)|Q(mobileno__contains=search)|Q(course__branch_name__contains=search)|Q(subject__contains=search))
       
    return render(request, 'admin/admin-manage-teacher.html', {'a': a})


def admin_update_teacher(request, id):
    a = TeacherRegistrationModel.objects.get(teacher_id=id)
    b = AddCourseModel.objects.all()
    c = AddSubjectModel.objects.all()
    data = get_object_or_404(TeacherRegistrationModel, teacher_id=id)
    if request.method == "POST":
        teacher_name = request.POST['teachername']
        gender = request.POST['gender']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        course_id = request.POST['course']
        course = AddCourseModel.objects.get(course_id=course_id)
        subject = request.POST['subject']

        data.teacher_name = teacher_name
        data.gender = gender
        data.email = email
        data.mobileno = mobileno
        data.course = course
        data.subject = subject
        data.save(update_fields=['teacher_name', 'gender',
                  'email', 'mobileno', 'course', 'subject'])
        # messages.info(request, 'Updated Successfully.')
        data.save()
        messages.info(request,"Teacher Updated Successfully")
        return redirect('admin_dashboard')
    return render(request, 'admin/admin-update-teacher.html', {'a': a, 'b': b, 'c': c})


def admin_announcement_news(request):
    a = AnnouncementModel.objects.all()
    if request.method == "POST":
        print("hi")
        title = request.POST['title']
        describe = request.POST['describe']
        date = request.POST['date']

        AnnouncementModel.objects.create(title=title, describe=describe, date=date)
        messages.info(request,"Announcement Added Successfully")
        return redirect('admin_dashboard')
    
    return render(request, 'admin/admin-announcement-news.html', {'a': a})


def remove(request, id):
    member = AnnouncementModel.objects.get(announcement_id=id)
    member.delete()
    messages.info(request,"Deleted Successfully")
    return redirect('admin_dashboard')
 
def removed(request, id):
    member = AddCourseModel.objects.get(course_id=id)
    member.delete()
    messages.info(request,"Deleted Successfully")
    return redirect('admin_dashboard')

def removes(request, id):
    member = AddSubjectModel.objects.get(subject_id=id)
    member.delete()
    messages.info(request,"Deleted Successfully")
    return redirect('admin_dashboard')


def admin_b_w_submit_assignment(request):
    return render(request, 'admin/admin-b-w-submit-assignment.html')


def admin_b_w_dates_assignment(request):
    # order = AddAssignmentModel.objects.all()
    if request.method == "POST":
        postingdate =request.POST.get('postingdate')
        postingdate1 = request.POST.get('postingdate1')
        order = AddAssignmentModel.objects.filter(posting_date__gte=postingdate,posting_date__lte=postingdate1)
        print(order,'hello ')
        # print(order,'hiiii')
        # return redirect('admin_b_w_submit_assignment',)
        return render(request, 'admin/admin-b-w-dates-assignment.html',{"order":order})
        # print()
    order=None
    
    return render(request, 'admin/admin-b-w-dates-assignment.html',{"order":order})
    


def admin_change_password(request):
    return render(request, 'admin/admin-change-password.html')


def admin_checked_assignment(request):
    return render(request, 'admin/admin-checked-assignment.html')

def admin_search(request):
    da = AddAssignmentModel.objects.all()
    if request.method == 'POST' and 'btn' in request.POST :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        da = AddAssignmentModel.objects.filter(Q(assignment_id__contains=search)|Q(course__branch_name__contains=search)|Q(subject__contains=search)|Q(posting_date__contains=search)|Q(last_date__contains=search)|Q(assignment_marks__contains=search))
        
    return render(request, 'admin/admin-search.html',{'data':da})
        
def admin_bw_dates_assignment(request):
    return render(request, 'admin/admin-bw-dates-assignment.html')

def admin_unchecked(request):
    
    b = Assignment_SubmitModel.objects.filter(submit_status="pending")
    
    return render(request, 'admin/admin-un-checked.html',{'b':b})

def admin_checked(request):
    
    a = ResultModel.objects.all().order_by
    # print('a')
    # if request.method == 'POST'  :
    #     print('hi')
    #     search = request.POST.get('search')
    #     print(search)
    #     print('jj')
    #     a=ResultModel.objects.filter(Q(stu_id__contains=search)|Q(stu__assign__assignment_title__contains=search)|Q(stu__assign__course__branch_name__contains=search)|Q(stu__assign__subject__contains=search)|Q(stu__submited_student__student_name__contains=search)|Q(stu__submited_date__contains=search))
    #     print(a) 
    return render(request, 'admin/admin-checked.html',{'a':a})

def admin_update_assignment(request):
    return render(request, 'admin/admin-update-assignment.html')


def admin_update_course(request, id):
    a = AddCourseModel.objects.get(course_id=id)
    data = get_object_or_404(AddCourseModel, course_id=id)
    if request.method == 'POST':
        course_name = request.POST['coursename']
        branch_name = request.POST['branchname']

        data.course_name = course_name
        data.branch_name = branch_name

        data.save(update_fields=['course_name', 'branch_name'])
        # messages.info(request, 'Updated Successfully.')
        data.save()
        messages.info(request,"Course Updated Successfully")
        return redirect('admin_dashboard')

    return render(request, 'admin/admin-update-course.html', {'f': a})


def admin_update_subject(request, id):
    r = AddCourseModel.objects.all()
    a = AddSubjectModel.objects.get(subject_id=id)
    data = get_object_or_404(AddSubjectModel, subject_id=id)
    if request.method == 'POST':
        course_name = request.POST['coursename']
        branch_name = request.POST['branchname']
        subject_name = request.POST['subjectname']
        shortcut_name = request.POST['shortcutname']
        code = request.POST['code']

        data.course_name = course_name
        data.branch_name = branch_name
        data.subject_name = subject_name
        data.shortcut_name = shortcut_name
        data.code = code

        data.save(update_fields=['course_name', 'branch_name',
                  'subject_name', 'shortcut_name', 'code'])
        # messages.info(request, 'Updated Successfully.')
        data.save()
        messages.info(request,"Subject Updated Successfully")
        return redirect('admin_dashboard')
    return render(request, 'admin/admin-update-subject.html', {'a': a,'r':r})
