from django import forms
from django.contrib.auth.models import User
from . import models

from django.forms import ModelForm

#from .models import Promise

#for admin
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee','status']



#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['salario','mobile','status']




#for Attendance related form
presence_choices=(('Present','Present'),('Falta','Falta'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

'''
class AskDateForm(forms.Form):
    date=forms.DateField()
'''
class DateInput(forms.DateInput):
    input_type = 'date'

class AskDateForm(forms.Form):
    date=forms.DateField(widget=DateInput)




    #def get_data_input_evento(self):
        #return self.date.strftime('%Y-%m-%dT%H:%M')




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
