

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


    path('admin-professor', views.admin_professor_view,name='admin-professor'),
    path('admin-add-professor', views.admin_add_professor_view,name='admin-add-professor'),
    path('admin-ver-professor', views.admin_view_professor_view,name='admin-ver-professor'),
    path('admin-aprovar-professor', views.admin_aprovar_professor_view,name='admin-aprovar-professor'),
    path('aprovar-professor/<int:pk>', views.approve_teacher_view,name='aprovar-professor'),
    path('apagar-professor/<int:pk>', views.delete_teacher_view,name='apagar-professor'),
    path('apagar-professor-escola/<int:pk>', views.delete_teacher_from_school_view,name='apagar-professor-escola'),
    path('atualizar-professor/<int:pk>', views.update_teacher_view,name='atualizar-professor'),
    path('admin-ver-salarios', views.admin_view_professor_salario_view,name='admin-ver-salarios'),


    path('admin-estudante', views.admin_estudante_view,name='admin-estudante'),
    path('admin-add-estudante', views.admin_add_estudante_view,name='admin-add-estudante'),
    path('admin-ver-estudante', views.admin_view_estudante_view,name='admin-ver-estudante'),
    path('apagar-estudante-escola/<int:pk>', views.delete_student_from_school_view,name='apagar-estudante-escola'),
    path('apagar-estudante/<int:pk>', views.delete_student_view,name='apagar-estudante'),
    path('atualizar-estudante/<int:pk>', views.update_student_view,name='atualizar-estudante'),
    path('admin-aprovar-estudante', views.admin_aprovar_estudante_view,name='admin-aprovar-estudante'),
    path('aprovar-estudante/<int:pk>', views.approve_student_view,name='aprovar-estudante'),
    path('admin-ver-mensalidades', views.admin_view_estudante_mensalidade_view,name='admin-ver-mensalidades'),


    path('admin-chamada', views.admin_chamada_view,name='admin-chamada'),
    path('admin-fazer-chamada/<str:cl>', views.admin_fazer_chamada_view,name='admin-fazer-chamada'),
    path('admin-ver-chamada/<str:cl>', views.admin_view_attendance_view,name='admin-ver-chamada'),


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
    path('contato', views.contactus_view),
]
