from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')



#inicio para o admin
def admin_pre_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/admin_inicio.html')


#pre tela para o professor
def prof_pre_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/prof_inicio.html')


#pre tela de login aluno
def estudante_pre_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/aluno_inicio.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/admincadastro.html',{'form':form})




def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('estudantelogin')
    return render(request,'school/estudantecadastro.html',context=mydict)


def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('professorlogin')
    return render(request,'school/professorcadastro.html',context=mydict)






#for checking user is techer , student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('professor-dashboard')
        else:
            return render(request,'school/professor_aguarde.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('estudante-dashboard')
        else:
            return render(request,'school/aluno_aguarde.html')




#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    teachersalario=models.TeacherExtra.objects.filter(status=True).aggregate(Sum('salario'))
    pendingteachersalario=models.TeacherExtra.objects.filter(status=False).aggregate(Sum('salario'))

    studentfee=models.StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalario':teachersalario['salario__sum'],
        'pendingteachersalario':pendingteachersalario['salario__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'school/admin_dashboard.html',context=mydict)







#for teacher sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_professor_view(request):
    return render(request,'school/admin_professor.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_professor_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-professor')
    return render(request,'school/admin_add_professor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_professor_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_professor.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_professor_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=False)
    return render(request,'school/admin_aprovar_professor.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-aprovar-professor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-aprovar-professor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-ver-professor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-ver-professor')
    return render(request,'school/admin_atualizar_professor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_professor_salario_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_professor_salario.html',{'teachers':teachers})






#for student by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_estudante_view(request):
    return render(request,'school/admin_estudante.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_estudante_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-estudante')
    return render(request,'school/admin_add_estudante.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_estudante_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_estudante.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-ver-estudante')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-aprovar-estudante')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-ver-estudante')
    return render(request,'school/admin_atualizar_estudante.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_estudante_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_aprovar_estudante.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-aprovar-estudante'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_estudante_mensalidade_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_estudante_mensalidade.html',{'students':students})






#attendance related viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_chamada_view(request):
    return render(request,'school/admin_chamada.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fazer_chamada_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.ChamadaForm()
    if request.method=='POST':
        form=forms.ChamadaForm(request.POST)
        if form.is_valid():
            #colocar no plural, pq essa aqui vai ser iterada
            Chamadas=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Chamadas)):
                ChamadaModel=models.Chamada()
                ChamadaModel.cl=cl
                ChamadaModel.date=date
                ChamadaModel.present_status=Chamadas[i]
                ChamadaModel.save()
            return redirect('admin-chamada')
        else:
            print('form invalid')
    return render(request,'school/admin_fazer_chamada.html',{'students':students,'aform':aform})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            Chamadadata=models.Chamada.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(Chamadadata,studentdata)
            return render(request,'school/admin_view_chamada_pagina.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_chamada_data.html',{'cl':cl,'form':form})









@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_mensalidade_view(request):
    return render(request,'school/admin_mensalidade.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_mensalidade_detalhes(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'school/admin_view_mensalidade.html',{'feedetails':feedetails,'cl':cl})








#notice related viewsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_noticia_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_noticia.html',{'form':form})








#for TEACHER  LOGIN    SECTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
@login_required(login_url='professorlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'salario':teacherdata[0].salario,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].dt_contrato,
        'notice':notice
    }
    return render(request,'school/professor_dashboard.html',context=mydict)



@login_required(login_url='professorlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/professor_chamada.html')


@login_required(login_url='professorlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.ChamadaForm()
    if request.method=='POST':
        form=forms.ChamadaForm(request.POST)
        if form.is_valid():
            Chamadas=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Chamadas)):
                ChamadaModel=models.Chamada()
                ChamadaModel.cl=cl
                ChamadaModel.date=date
                ChamadaModel.present_status=Chamadas[i]
                ChamadaModel.roll=students[i].roll
                ChamadaModel.save()
            return redirect('professor-chamada')
        else:
            print('form invalid')
    return render(request,'school/professor-fazer-chamada.html',{'students':students,'aform':aform})



@login_required(login_url='professorlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            Chamadadata=models.Chamada.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(Chamadadata,studentdata)
            return render(request,'school/professor_ver_chamada.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/professor_ver_chamada_data.html',{'cl':cl,'form':form})



@login_required(login_url='professorlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('professor-dashboard')
        else:
            print('form invalid')
    return render(request,'school/professor_aviso.html',{'form':form})







#FOR STUDENT AFTER THEIR Loginnnnnnnnnnnnnnnnnnnnn
@login_required(login_url='estudantelogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'school/estudante_dashboard.html',context=mydict)



@login_required(login_url='estudantelogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            Chamadadata=models.Chamada.objects.all().filter(date=date,cl=studentdata[0].cl)
            mylist=zip(Chamadadata,studentdata)
            return render(request,'school/estudante_ver_chamada.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/estudante_ver_chamada_data.html',{'form':form})









# tela de sobre
def sobre_view(request):
    return render(request,'school/sobre.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = 'Nome:' + name + '\nEmail: ' + email+ '\nMensagem:' +  sub.cleaned_data['Message']
            send_mail('SisEDist - Contato',message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/contatosucesso.html')
    return render(request, 'school/contato.html', {'form':sub})

def estudante_senha(request):
    sub = forms.SenhaForm()
    if request.method == 'POST':
        sub = forms.SenhaForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            nome=sub.cleaned_data['Nome']
            username=sub.cleaned_data['Nome_user']

            message = 'Nome:' + nome + '\nEmail: ' + email+ '\nUsername:' + username +  '\nObservação: ' + sub.cleaned_data['Observacao']
            send_mail('SisEDist - Perdi a senha(Aluno)',message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/estudantesenhasucesso.html')
    return render(request, 'school/estudantesenha.html', {'form':sub})    

def professor_senha(request):
    sub = forms.SenhaForm()
    if request.method == 'POST':
        sub = forms.SenhaForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            nome=sub.cleaned_data['Nome']
            username=sub.cleaned_data['Nome_user']

            message = 'Nome:' + nome + '\nEmail: ' + email+ '\nUsername:' + username +  '\nObservação: ' + sub.cleaned_data['Observacao']
            send_mail('SisEDist - Perdi a senha(Professor)',message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/professorsenhasucesso.html')
    return render(request, 'school/professorsenha.html', {'form':sub})   
#ss