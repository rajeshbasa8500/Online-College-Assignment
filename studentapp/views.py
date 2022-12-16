from distutils.log import error
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, redirect, render
from adminapp.models import AddSubjectModel, AnnouncementModel
from studentapp.models import ResultModel, StudentRegisterModel
from adminapp.models import AnnouncementModel
from teacherapp.models import AddAssignmentModel
from adminapp.models import AddCourseModel
from django.contrib import messages
from studentapp.models import Assignment_SubmitModel
from django.utils.crypto import get_random_string


# Create your views here.


def student_registration(request):
    a = AddCourseModel.objects.all()
    if request.method == 'POST' and request.FILES['file']:
        student_name = request.POST['studentname']
        student_rollno = request.POST['rollno']
        course_id = request.POST['course']
        student_mobileno = request.POST['mobileno']
        student_email = request.POST['email']
        student_password = request.POST['password']
        chars = '01234567899876543210112233445566778899'
        student_otp = get_random_string(4, chars)
        print(student_otp)
        student_photo = request.FILES['file']
        #print(course_id, 'GJHGHGGGG')
        course = AddCourseModel.objects.get(course_id=course_id)
        print(course, "hi")

        StudentRegisterModel.objects.create(student_name=student_name, student_rollno=student_rollno, course=course,
                                            student_mobileno=student_mobileno, student_email=student_email, student_password=student_password, student_otp=student_otp, student_photo=student_photo)
        messages.info(request, "Successfully Created Account.")
        return redirect('student_login')
    return render(request, 'main/student-registration.html', {'a': a})


def student_login(request):
    if request.method == "POST":
        print('post')
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = StudentRegisterModel.objects.get(
                student_email=email, student_password=password)
            # print(facultee)
            # print(facultee.faculty_id)
            # print('course')
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

            # return redirect('student-otp')

            # return render(request,'main/user-register.html')
            request.session['student_id'] = student.student_id
             
            messages.info(request, "Login Successfully.")
            return redirect("student_dashboard")
        except:
            print('error')
            messages.error(request,"Invalid EmailID or Password")
    return render(request, 'main/student-login.html ')


def student_dashboard(request):
    a = request.session['student_id']
    b = StudentRegisterModel.objects.get(student_id=a)
    d = b.course
    c = AddAssignmentModel.objects.filter(course=d).count()
    print(c,b,d)
    e = Assignment_SubmitModel.objects.filter(assign__course=d, submited_student=b).count()
    f =(c-e)
    # messages.info(request, "Login Successfully.")
    return render(request, 'student/student-dashboard.html',{'c':c,'e':e,'f':f})


def student_new_assignments(request):
    student = request.session['student_id']
    b = StudentRegisterModel.objects.get(student_id=student)
    c = b.course
    a = AddAssignmentModel.objects.filter(course=c).order_by('-assignment_id')
    for i in a:
        try:
            Assignment_SubmitModel.objects.get(assign=i, submited_student=b)
            i.submited = True
            print(i.course)
        except:
            i.submited = False
            # print(d, 'jhhj')

    return render(request, 'student/student-new-assignments.html', {'a': a})


def studnet_submit_assignments(request, id):
    student = request.session['student_id']
    a = AddAssignmentModel.objects.get(assignment_id=id)
    submited_student = StudentRegisterModel.objects.get(student_id=student)
    if request.method == 'POST' and request.FILES['myfile']:
        text = request.POST['text']
        myfile = request.FILES['myfile']
        Assignment_SubmitModel.objects.create(assign=a, submited_student=submited_student, text=text, myfile=myfile)
        messages.info(request, "Assignment Submited Successfully.")
        return redirect('student_dashboard')
    return render(request, 'student/student-submit-assignments.html', {'i': a})



def student_manage_assignment(request):
    student = request.session['student_id']
    b = StudentRegisterModel.objects.get(student_id=student)
    c = b.course
    a = AddAssignmentModel.objects.filter(course=c).order_by('-assignment_id')
    print(a)
    for i in a:
        try:
            Assignment_SubmitModel.objects.get(assign=i, submited_student=b)
            
            i.submited = True
            try:
                f=Assignment_SubmitModel.objects.get(assign=i, submited_student=b)
                ResultModel.objects.get(stu=f)
                i.status='Checked'
            except:
                i.status='Unchecked'
        except:
            i.submited = False
            # print(d, 'jhhj')
    

    return render(request, 'student/student-manage-assignment.html', {'a': a})


def student_update_assignment(request, id):
    student = request.session['student_id']
    a = AddAssignmentModel.objects.get(assignment_id=id)
    submited_student = StudentRegisterModel.objects.get(student_id=student)
    d = Assignment_SubmitModel.objects.get(assign=a, submited_student=submited_student)
    # print(d.text)
    # print(d.myfile)
    data = get_object_or_404(Assignment_SubmitModel, assign=a, submited_student=submited_student)
    
    if request.method == 'POST':
        text = request.POST['text']
       
        
        if not request.FILES.get("myfile", False):
            data.text = text
            data.save(update_fields=['text','assign','submited_student'])
            data.save()
            
        elif request.FILES.get("myfile", False):
            myfile = request.FILES["myfile"]
            data.text = text
            data.myfile = myfile
            data.save(update_fields=['text','myfile','assign','submited_student'])
            #  messages.info(request, 'Updated Successfully.')
            data.save()
        messages.info(request, "Assignment Updated Successfully.")
        return redirect('student_dashboard')
    return render(request, 'student/student-update-assignment.html', {'i': a,'d':d})

def student_assignment_result(request, hid):
    a = AddAssignmentModel.objects.get(assignment_id=hid)
    b = request.session['student_id']
    # c= StudentRegisterModel.objects.get(student_id=b)
    # d = c.course
    e=Assignment_SubmitModel.objects.get(assign=a)
    f= ResultModel.objects.get(stu=e)
    raj= f.marks
    if raj  == 50:
        print('hiii')
    print(raj)
    return render(request, 'student/student-assignment-result.html',{'i':a,'f':f})

def student_upload1_assignments(request):
    return render(request, 'student/student-upload1-assignments.html')


def student_uploaded_assignments(request):
    return render(request, 'student-uploaded-assignments.html')


def student_annoucements(request):
    a = AnnouncementModel.objects.all()
    return render(request, 'student/student-announcements.html', {'a': a})
#*****OTP********#
# def student_otp(request):
#     if request.method == "POST":
#         otp = request.POST.get('otp')
#         try:
#             check = StudentRegisterModel.objects.get(otp=otp)
#             request.session['student_id']=check.student_id
#             otp=check.otp
#             if otp == otp:
#                 messages.info(request,'Account Created Successfully!')
#                 return redirect('student_dashboard')
#         except:
#             messages.error(request,'The OTP you entered is incorrect.Please try again.')
#             print('The OTP you entered is incorrect.Please try again.')
#             return redirect('student_otp')
#     return render(request,'student/student-otp.html')



# student = request.session['student_id']
    # a = AddAssignmentModel.objects.get(assignment_id=id)
    # submited_student = StudentRegisterModel.objects.get(student_id=student)
    # data = get_object_or_404(Assignment_SubmitModel, submit_id=id)
    
    # if request.method == 'POST' and request.FILES['myfile']:
    #     text = request.POST['text']
    #     myfile = request.FILES['myfile']
    #     Assignment_SubmitModel.objects.create(assign=a, submited_student=submited_student, text=text, myfile=myfile)
  
    #     data.save(update_fields=['assign','submited_student','text', 'myfile',])
    #     # messages.info(request, 'Updated Successfully.')
    #     data.save()