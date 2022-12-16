from ast import Assign
from unittest import result
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.contrib import messages
from adminapp.models import AddCourseModel, AddSubjectModel, AnnouncementModel
from studentapp.models import Assignment_SubmitModel, StudentRegisterModel
from adminapp.models import TeacherRegistrationModel
from teacherapp.models import AddAssignmentModel
from datetime import date
from studentapp.models import ResultModel
from django.db.models import Q   
# Create your views here.
def teacher_login(request):
    if request.method == "POST":
        print('post')
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            teacher = TeacherRegistrationModel.objects.get(email = email ,password = password)
            # print(facultee)
            # print(facultee.faculty_id)
            ###****SMS OTP*******####
            # otp = stus.student_otp
            # url = "https://www.fast2sms.com/dev/bulkV2"
            # # create a dictionary
            # my_data = {'sender_id': 'FSTSMS', 
            #             'message': 'Welcome to CloudHost, your verification OPT is '+str(otp)+ 'Thanks for request of OTP.', 
            #             'language': 'english', 
            #             'route': 'p', 
            #             'numbers': stus.student_mobileno,
            # }

            # # create a dictionary
            # headers = {
            #     'authorization': 'D4vuFnk1sNQOl6SRpfZUT23ewPX0BoLrzAJVgqtW8bxyHEGjImfkE0NtULg1TG9xImYHpVZjQMnBSOoa',
            #     'Content-Type': "application/x-www-form-urlencoded",
            #     'Cache-Control': "no-cache"
            # }
            # # make a post request
            # response = requests.request("POST",
            #                             url,
            #                             data = my_data,
            #                             headers = headers)
            # # print the send message
            # print(response.text)        

            # return redirect('teacher-otp')

            # return render(request,'main/user-register.html')
            
            request.session['teacher_id']=teacher.teacher_id
            #print(teacher.teacher_id)
            messages.info(request, "Login Successfully.")
            return redirect("teacher_dashboard")
        except:
            print("error")
            messages.error(request,"Invalid EmailID or Password")
    return render(request, 'main/teacher-login.html')

def teacher_dashboard(request):
    a = StudentRegisterModel.objects.all()
    b = StudentRegisterModel.objects.count()
    c = AddAssignmentModel.objects.count()
    d = AnnouncementModel.objects.count()
    da = AddAssignmentModel.objects.all()
    if request.method == 'POST'  :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        a=StudentRegisterModel.objects.filter(Q(student_name__contains=search)|Q(course__branch_name__contains=search)|Q(student_mobileno__contains=search)|Q(student_email__contains=search)|Q(student_rollno__contains=search))
        print(a)
    return render(request, 'teacher/teacher-dashboard.html',{'a':a,'b':b,'c':c,'d':d})

def teacher_add_assignment(request):
    teacher_id = request.session['teacher_id']
    Assignment_details = TeacherRegistrationModel.objects.get(teacher_id=teacher_id)
    demo = Assignment_details.teacher_id
    print(demo)
    
    demo1 = Assignment_details.course.branch_name
    print(demo1)
    demo2 = Assignment_details.course.course_name
    print(demo2)
    a = AddCourseModel.objects.filter(branch_name=demo1, )
    b = AddSubjectModel.objects.filter(course_name= demo2 )
    if request.method == "POST" and request.FILES['file']:
        course_id = request.POST['course']
        subject = request.POST['subject']
        assignment_title = request.POST['title']
        assignment_description = request.POST['description']
        last_date = request.POST['date']
        assignment_marks = request.POST['marks']
        assignment_file = request.FILES['file']
        course = AddCourseModel.objects.get(course_id=course_id)
        
        Assignment_details = AddAssignmentModel.objects.create(Assignment_details = Assignment_details, course=course,  subject=subject, assignment_title=assignment_title, assignment_description=assignment_description, last_date=last_date,  assignment_marks=assignment_marks, assignment_file=assignment_file)
        messages.info(request,"Assignment Added Successfully")
        return redirect('teacher_dashboard')
    return render(request, 'teacher/teacher-add-assignment.html',{'a':a,'b':b})

def teacher_manage_assignment(request):
    f = request.session['teacher_id']
    a = TeacherRegistrationModel.objects.get(teacher_id=f)
    b = a.subject
    print(b)
    b = AddAssignmentModel.objects.filter(subject=b)
    if request.method == 'POST'  :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        b=AddAssignmentModel.objects.filter(Q(assignment_title__contains=search)|Q(course__branch_name__contains=search)|Q(subject__contains=search)|Q(assignment_description__contains=search)|Q(last_date__contains=search))
        print(b)
        
    return render(request, 'teacher/teacher-manage-assignment.html',{'b':b})

def teacher_update_assignment(request,id):
    a = AddAssignmentModel.objects.get(assignment_id=id)
    c = AddCourseModel.objects.all()
    b = AddSubjectModel.objects.all()
    data = get_object_or_404(AddAssignmentModel, assignment_id=id)
    if request.method == "POST":
        course_id = request.POST['course']
        subject = request.POST['subject']
        assignment_title = request.POST['title']
        assignment_description = request.POST['description']
        last_date = request.POST['date']
        assignment_marks = request.POST['marks']
        course = AddCourseModel.objects.get(course_id=course_id)
        
        data.course = course
        data.subject = subject
        data.assignment_title = assignment_title
        data.assignment_description = assignment_description
        data.last_date = last_date
        data.assignment_marks = assignment_marks
       
        data.save(update_fields=['course', 'subject','assignment_title','assignment_description','last_date','assignment_marks'])
        # messages.info(request, 'Updated Successfully.')
        data.save()
        messages.info(request,"Assignment Updated Successfully")
        return redirect(teacher_dashboard)
    return render(request, 'teacher/teacher-update-assignment.html',{'a':a,'b':b,'c':c})

def teacher_announcement_news(request):
    a=AnnouncementModel.objects.all()
    if request.method == 'POST'  :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        a=AnnouncementModel.objects.filter(Q(title__contains=search)|Q(describe__contains=search)|Q(date__contains=search))
        print(a)
    return render(request, 'teacher/teacher-announcement-news.html',{'a':a})

def delete(request, id):
    member = AnnouncementModel.objects.get(announcement_id=id)
    member.delete()
    messages.info(request,"Deleted Successfully")
    return redirect('teacher_dashboard')

def teacher_unchecked(request):
    teacher = request.session['teacher_id']
    b = TeacherRegistrationModel.objects.get(teacher_id=teacher)
    c = b.course_id
    print(c)
    e =b.subject
    print(e)
    data = Assignment_SubmitModel.objects.filter(submited_student=c ,assign__subject__icontains=e)
    print(data)
    # print(ab)
    for i in data:
        try:
             ResultModel.objects.get(stu=i)
             i.submited = True
             print('hi')
        except:
             i.submited = False
             print('hello')        
    return render(request, 'teacher/teacher-unchecked.html',{"a":data})

def teacher_student_update_assignment(request, id):
    teacher = request.session['teacher_id']
    b = TeacherRegistrationModel.objects.get(teacher_id=teacher)
    d=b.subject
    print(d)
    data = get_object_or_404(Assignment_SubmitModel, assign__subject__icontains=d,submit_id=id)

    if request.method == "POST":
        remarks = request.POST['remark']
        marks = request.POST['marks']
        ResultModel.objects.create(stu=data, remarks=remarks, marks=marks)
        
        data.submit_status='checked'
        data.save(update_fields=['submit_status'])
        data.save()
        messages.info(request,"Checked Successfully")
        return redirect('teacher_dashboard')
    return render(request, 'teacher/teacher-student-update-assignment.html',{'a':data})


def teacher_profile(request):
    teacher_id = request.session['teacher_id']
    a = TeacherRegistrationModel.objects.get(teacher_id=teacher_id)
    
    # faculty_name = request.session["faculty_name"]
    # j = FacultyRegisterModel.objects.filter(faculty_name=faculty_name)
    # obj=get_object_or_404(FacultyRegisterModel,faculty_id=faculty_id)
    # obj = get_object_or_404(FacultyRegisterModel, faculty_name=faculty_name)
    obj = get_object_or_404(TeacherRegistrationModel, teacher_id=teacher_id)
    if request.method == 'POST':
        teacher_name = request.POST['teachername']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        
        subject = request.POST['subject']
        password = request.POST['password']
        
       
        if not request.FILES.get("tphoto",False):
            # print("yes efffeg jfkdftjhkt")
            obj.teacher_name = teacher_name
            obj.email = email
            obj.mobileno = mobileno
            
            obj.subject = subject
            obj.password = password
            obj.save(update_fields=['teacher_name', 'email', 'mobileno',
                                         'subject', 'password'])
            obj.save()
             
        elif request.FILES.get("tphoto",False):
            tphoto = request.FILES['tphoto']
            obj.teacher_name = teacher_name
            obj.email = email
            obj.mobileno = mobileno
           
            obj.subject = subject
            obj.password = password
            obj.tphoto = tphoto
            obj.save(update_fields=['teacher_name', 'email', 'mobileno',
                                        'subject', 'password','tphoto'])
            obj.save()
           
        return redirect('teacher_profile')
    return render(request, 'teacher/teacher-profile.html',{'a':a})

def teacher_subject_wise_report(request):
     # order = AddAssignmentModel.objects.all()
    if request.method == "POST":
        postingdate =request.POST.get('postingdate')
        postingdate1 = request.POST.get('postingdate1')
        order = AddAssignmentModel.objects.filter(posting_date__gte=postingdate,posting_date__lte=postingdate1)
        print(order,'hello ')
        # print(order,'hiiii')
        # return redirect('admin_b_w_submit_assignment',)
        return render(request, 'teacher/teacher-subject-wise-report.html',{"order":order})
        # print()
    order=None
    
    return render(request, 'teacher/teacher-subject-wise-report.html')

def teacher_reg_user(request):
    a = StudentRegisterModel.objects.all()
    if request.method == 'POST' and 'btn' in request.POST :
        print('hi')
        search = request.POST.get('search')
        print(search)
        print('jj')
        a=StudentRegisterModel.objects.filter(Q(student_name__contains=search)|Q(student_mobileno__contains=search)|Q(course__branch_name__contains=search)|Q(student_email__contains=search)|Q(student_rollno__contains=search))
        print(a,'jjooo')
    return render(request, 'teacher/teacher-reg-user.html',{'a':a})

def teacher_settings(request):
    return render(request, 'teacher/teacher-settings.html')

def teacher_assignmnet(request):
    return render(request, 'teacher/teacher-assignment.html')

def teacher_checked(request):
    teacher = request.session['teacher_id']
    b = TeacherRegistrationModel.objects.get(teacher_id=teacher)
    c = b.course_id
    print(c)
 
    e =b.subject
    print(e)
    data = Assignment_SubmitModel.objects.filter(submited_student=c ,assign__subject__icontains=e)
    
    print(data)
    # print(ab)
    for i in data:
        try:
             ResultModel.objects.get(stu=i)
             i.submited = True
             print('hi')
        except:
             i.submited = False
             print('hello')        
    return render(request, 'teacher/teacher-checked.html',{"a":data})

def teacher_uploded_assignment(request,id):
    teacher = request.session['teacher_id']
    b = TeacherRegistrationModel.objects.get(teacher_id=teacher)
    d=b.subject
    print(d)
    data = get_object_or_404(Assignment_SubmitModel, assign__subject__icontains=d,submit_id=id)
    da = get_object_or_404(ResultModel,stu=data)
    if request.method == "POST":
        remarks = request.POST['remark']
        marks = request.POST['marks']
        
        da.remarks = remarks
        da.marks = marks 
        da.save(update_fields=['remarks', 'marks'])
        da.save()
        messages.info(request, 'Marks Updated Successfully.')
        return redirect('teacher_dashboard')
    return render(request, 'teacher/teacher-uploded-assignment.html',{'a':data,"da":da})

#*****OTP********#
# def teacher_otp(request):
#     if request.method == "POST":
#         otp = request.POST.get('otp')
#         try:
#             check = TeacherRegistrationModel.objects.get(otp=otp)
#             request.session['teacher_id']=check.teacher
#             otp=check.otp
#             if otp == otp:
#                 messages.info(request,'Account Created Successfully!')
#                 return redirect('teacher_dashboard')
#         except:
#             messages.error(request,'The OTP you entered is incorrect.Please try again.')
#             print('The OTP you entered is incorrect.Please try again.')
#             return redirect('teacher_otp')
#     return render(request,'teacher/teacher-otp.html')



# def teacher_subject_checked(request):
#     a = AddSubjectModel.objects.all()
#     return render(request, 'teacher/teacher-subject-checked.html',{'a':a})

# def teacher_subject_unchecked(request):
#     a = AddSubjectModel.objects.all()
#     return render(request, 'teacher/teacher-subject-unchecked.html',{'a':a})

