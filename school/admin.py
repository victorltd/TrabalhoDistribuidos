from django.contrib import admin
from .models import Chamada,StudentExtra,TeacherExtra,Notice

class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class ChamadaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Chamada, ChamadaAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)
