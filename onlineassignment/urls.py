"""onlineassignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pip import main
import studentapp

from mainapp import views as mainapp_views
from adminapp import views as adminapp_views
from studentapp import views as studentapp_views
from teacherapp import views as teacherapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # main
    path('', mainapp_views.index, name='index'),
    
    #admin
    path('admin-login', adminapp_views.admin_login, name='admin_login'),
    path('admin-logout', adminapp_views.admin_logout, name='admin_logout'),
    path('admin-dashboard',adminapp_views.admin_dashboard, name='admin_dashboard'),
    path('admin-add-teacher', adminapp_views.admin_add_teacher, name='admin_add_teacher'),
    path('admin-announcement-news', adminapp_views.admin_announcement_news, name='admin_announcement_news'),
    path('admin-b-w-submit-assignment', adminapp_views.admin_b_w_submit_assignment, name='admin_b_w_submit_assignment'),
    path('admin-b-w-dates-assignment', adminapp_views.admin_b_w_dates_assignment, name='admin_b_w_dates_assignment'),
    path('admin-change-password', adminapp_views.admin_change_password, name='admin_change_password'),
    path('admin-checked-assignment', adminapp_views.admin_checked_assignment, name='admin_checked_assignment'),
    path('admin-checked', adminapp_views.admin_checked, name='admin_checked'),
    path('admin-add-course', adminapp_views.admin_add_course, name='admin_course'),
    path('admin-manage-teacher', adminapp_views.admin_manage_teacher, name='admin_manage_teacher'),
    #path('admin-profile', adminapp_views.admin_profile, name='admin_profile'),
    path('admin-search', adminapp_views.admin_search, name='admin_search'),
    # path('admin-subject-checked', adminapp_views.admin_subject_checked , name='admin_subject_checked'),
    # path('admin-subject-unchecked', adminapp_views.admin_subject_unchecked, name='admin_subject_unchecked'),
    path('admin-add-subject', adminapp_views.admin_add_subject, name='admin_subject'),
    path('admin-unchecked', adminapp_views.admin_unchecked, name='admin_unchecked'),
    path('admin-update-assignment', adminapp_views.admin_update_assignment, name='admin_update_assignment'),
    path('admin-update-course/<int:id>/', adminapp_views.admin_update_course, name='admin-update-course'),
    path('admin-update-subject/<int:id>', adminapp_views.admin_update_subject, name='admin-update-subject'),
    path('admin-update-teacher/<int:id>/', adminapp_views.admin_update_teacher, name='admin-update-teacher'),
    path('remove/<int:id>',adminapp_views.remove, name='remove'),
    path('removes/<int:id>',adminapp_views.removes, name='removes'),
    path('removed/<int:id>',adminapp_views.removed, name='removed'),
    #student
    path('student-login', studentapp_views.student_login, name='student_login'),
    path('student-registration', studentapp_views.student_registration, name='student_registration'),
    path('student-dashboard', studentapp_views.student_dashboard, name='student_dashboard'),
    path('student-new-assignments', studentapp_views.student_new_assignments, name='student_new_assignments'),
    path('student-submit-assignments/<int:id>/', studentapp_views.studnet_submit_assignments, name = 'student-submit-assignments'),
    # path('genuine/<int:id>',studentapp_views.genuine, name='genuine'),

    path('student-upload1-assignments', studentapp_views.student_upload1_assignments, name='student_upload1_assignments'),
    path('student-manage-assignment', studentapp_views.student_manage_assignment, name='student_manage_assignment'),
    path('student-update-assignment/<int:id>/', studentapp_views.student_update_assignment, name='student-update-assignment'),
    path('student-uploaded-assignments', studentapp_views.student_uploaded_assignments, name='student_uploaded_assignments'),
    path('student-annoucements', studentapp_views.student_annoucements, name='student_annoucements'),
    path('student-assignment-result/<int:hid>/', studentapp_views.student_assignment_result, name='student-assignment-result'),
    # path('student-otp',studentapp_views.student_otp,name='student_otp'),
    #teacher
    path('teacher-login', teacherapp_views.teacher_login, name='teacher_login'),
    path('teacher-dashboard', teacherapp_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-add-assignment', teacherapp_views.teacher_add_assignment, name='teacher_add_assignment'),
    path('teacher-announcement-news', teacherapp_views.teacher_announcement_news, name='teacher_announcement_news'),
    path('teacher-assignment', teacherapp_views.teacher_assignmnet, name='teacher_assignmnet'),
    path('teacher-checked', teacherapp_views.teacher_checked, name='teacher_checked'),
    path('teacher-manage-assignment', teacherapp_views.teacher_manage_assignment, name='teacher_manage_assignment'),
    path('teacher-profile', teacherapp_views.teacher_profile, name='teacher_profile'),
    path('teacher-reg-user', teacherapp_views.teacher_reg_user, name='teacher_reg_user'),
    path('teacher-settings', teacherapp_views.teacher_settings, name='teacher_settings'),
    path('teacher-student-update-assignment/<int:id>/', teacherapp_views.teacher_student_update_assignment, name='teacher-student-update-assignment'),
    # path('teacher-subject-checked', teacherapp_views.teacher_subject_checked, name='teacher_subject_checked'),
    # path('teacher-subject-unchecked', teacherapp_views.teacher_subject_unchecked, name='teacher_subject_unchecked'),
    path('teacher-subject-wise-report', teacherapp_views.teacher_subject_wise_report, name='teacher_subject_wise_report'),
    path('teacher-unchecked', teacherapp_views.teacher_unchecked, name='teacher_unchecked'),
    path('teacher-update-assignment/<int:id>', teacherapp_views.teacher_update_assignment, name='teacher-update-assignment'),
    path('teacher-uploded-assignment/<int:id>', teacherapp_views.teacher_uploded_assignment, name='teacher-uploded-assignment'),
    path('delete/<int:id>',teacherapp_views.delete, name='delete'),
    # path('teacher-otp',teacherapp_views.teacher_otp,name='teacher_otp'),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

