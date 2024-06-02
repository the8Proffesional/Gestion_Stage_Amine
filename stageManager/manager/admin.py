from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Dossiers, Student, Prof, Filiere, StudenttFiliere, Domaine, Prof_Filiere


class Etud(UserAdmin):
    model=Student
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('adresse','tel', 'Sex', 'Napog','CNE','dateN','lieuxN')}),
    )

class Professeur(UserAdmin):
    model=Prof
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('adresse','tel','dateN','lieuxN', 'SPC')}),
    )

admin.site.register(Student, Etud)
admin.site.register(Prof, Professeur)
admin.site.register(Dossiers)
admin.site.register(Filiere)
admin.site.register(StudenttFiliere)
admin.site.register(Domaine)
admin.site.register(Prof_Filiere)
# Register your models here.
