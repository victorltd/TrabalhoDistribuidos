"""
by sumit kumar
written by fb.com/sumit.luv

"""

#alteracao lustosa
from django.contrib import admin
from django.urls import path
from school import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('admin_inicio', views.admin_pre_view),
    path('prof_inicio', views.prof_pre_view),
    path('aluno_inicio', views.estudante_pre_view),


    path('admincadastro', views.admin_signup_view),
    path('estudantecadastro', views.student_signup_view,name='estudantecadastro'),
    path('professorcadastro', views.teacher_signup_view),
    path('adminlogin', LoginView.as_view(template_name='school/adminlogin.html')),
    path('estudantelogin', LoginView.as_view(template_name='school/estudantelogin.html')),
    path('professorlogin', LoginView.as_view(template_name='school/professorlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='school/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),


    path('admin-teacher', views.admin_professor_view,name='admin-teacher'),
    path('admin-add-teacher', views.admin_add_professor_view,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_professor_view,name='admin-view-teacher'),
    path('admin-approve-teacher', views.admin_aprovar_professor_view,name='admin-approve-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('delete-teacher-from-school/<int:pk>', views.delete_teacher_from_school_view,name='delete-teacher-from-school'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('admin-view-teacher-salary', views.admin_view_professor_salario_view,name='admin-view-teacher-salary'),


    path('admin-student', views.admin_estudante_view,name='admin-student'),
    path('admin-add-student', views.admin_add_estudante_view,name='admin-add-student'),
    path('admin-view-student', views.admin_view_estudante_view,name='admin-view-student'),
    path('delete-student-from-school/<int:pk>', views.delete_student_from_school_view,name='delete-student-from-school'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-approve-student', views.admin_aprovar_estudante_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('admin-view-student-fee', views.admin_view_estudante_mensalidade_view,name='admin-view-student-fee'),


    path('admin-attendance', views.admin_chamada_view,name='admin-attendance'),
    path('admin-take-attendance/<str:cl>', views.admin_fazer_chamada_view,name='admin-take-attendance'),
    path('admin-view-attendance/<str:cl>', views.admin_view_attendance_view,name='admin-view-attendance'),


    path('admin-mensalidade', views.admin_mensalidade_view,name='admin-mensalidade'),
    path('admin-view-mensalidade/<str:cl>', views.admin_view_mensalidade_detalhes,name='admin-view-mensalidade'),

    path('admin-notice', views.admin_noticia_view,name='admin-notice'),



    path('professor-dashboard', views.teacher_dashboard_view,name='professor-dashboard'),
    path('professor-chamada', views.teacher_attendance_view,name='professor-chamada'),
    path('professor-fazer-chamada/<str:cl>', views.teacher_take_attendance_view,name='professor-fazer-chamada'),
    path('professor-ver-chamada/<str:cl>', views.teacher_view_attendance_view,name='professor-ver-chamada'),
    path('professor-aviso', views.teacher_notice_view,name='professor-aviso'),

    path('estudante-dashboard', views.student_dashboard_view,name='estudante-dashboard'),
    path('estudante-chamada', views.student_attendance_view,name='estudante-chamada'),




    path('sobre', views.sobre_view),
    path('contactus', views.contactus_view),
]
