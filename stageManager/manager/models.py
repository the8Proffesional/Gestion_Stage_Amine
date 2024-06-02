from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN", 'ADMIN'
        PROF="PROF", 'PROF'
        ETUDIANT="ETUDIANT", 'ETUDIANT'
    SEX = (
        ("Male", "Male"),
        ('Female', 'Female'),
    )
    base_role=Role.ADMIN
    base_role1=Role.ETUDIANT
    role = models.CharField(max_length = 20, choices= Role)
     
    Sex =  models.CharField(max_length = 10, choices=SEX)
    #adresse
    adresse=models.TextField(max_length=150,null=True)
    #tel
    tel=models.CharField(max_length=40,null=True)

    #N_apog
    Napog=models.IntegerField(default=0,null=True)
    #CNE
    CNE=models.CharField(max_length=50,null=True)
    #date_n
    dateN= models.DateField(auto_now=False, auto_now_add=False, null=True)
    #lieux_n
    lieuxN = models.CharField(max_length=50,null=True)
    
    
    #spc
    SPC = models.CharField(max_length = 50,null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role=self.base_role
            return super().save(*args, **kwargs)
        else:
            return super().save(*args, **kwargs)


class ProfManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result=super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.PROF)
        
class Prof(User):
    base_role=User.Role.PROF
    prof=ProfManager()
    class Meta:
        proxy=True


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result=super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.ETUDIANT)
    
class Student(User):
    base_role=User.Role.ETUDIANT
    student=StudentManager()
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    class Meta:
        proxy=True

class Dossiers(models.Model):
    TYPES = (
        ("1", "Stage d'initiation"),
        ('2', 'stage technique'),
        ('3', 'stage PFE'),
        ('4', 'Stage Professionel'),
    )
    NIVEAUX = (
        ("1ere Annee", "1ere Annee"),
        ("2eme Annee", "2eme Annee"),
        ('Licence Professionelle', 'Licence Professionelle'),
    )
    Type = models.CharField(max_length=50, choices=TYPES)
    Rapport = models.CharField(max_length=100, null=False, blank=False)
    Doss= models.CharField(max_length=100, null=False, blank=False)
    Sujet = models.CharField(max_length=100, null=False, blank=False)
    Encadrant = models.CharField(max_length=100, null=False, blank=False)
    Domaine = models.CharField(max_length=100, null=False, blank=False)

    Nom_filiere = models.CharField(max_length=100)
    Year = models.DateField(auto_now=False, auto_now_add=False)
    Niveau = models.CharField(max_length=50, choices = NIVEAUX)

    Student = models.ForeignKey(Student, on_delete=models.CASCADE)

    ValidationProf = models.BooleanField(default=False)
    ValidationAdmin = models.BooleanField(default=False)
    RemarqueProf = models.CharField(max_length=255, blank=True, null=True)
    RemarqueAdmin = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering=['Type']
    
    def __str__(self):
        return f"{self.Sujet} {self.Domaine}"

class Filiere(models.Model):
    Nom_filiere = models.CharField(max_length=100, unique=True) 
    def __str__(self):
        return f"{self.Nom_filiere}"


class StudenttFiliere(models.Model):
    NIVEAUX = (
        ("1ere Annee", "1ere Annee"),
        ("2eme Annee", "2eme Annee"),
        ('Licence Professionelle', 'Licence Professionelle'),
    )
    Niveau = models.CharField(max_length=50 , choices = NIVEAUX, null=False)
    Year = models.DateField(auto_now=False, auto_now_add=False, null=False)
    Etudiant = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=False)
    Filiere = models.ForeignKey(Filiere, on_delete=models.DO_NOTHING, null=False)
    class Meta:
        unique_together = ( 'Year', 'Etudiant')
        ordering = ['Year']
    def __str__(self):
        return f"{self.Etudiant.username}--{self.Filiere.Nom_filiere}--{self.Niveau} -- {self.Year.year}"

class Prof_Filiere(models.Model):
    NIVEAUX = (
        ("1ere Annee", "1ere Annee"),
        ("2eme Annee", "2eme Annee"),
        ('Licence Professionelle', 'Licence Professionelle'),
    )
    Niveau = models.CharField(max_length=50 , choices = NIVEAUX, null=False)
    prof = models.ForeignKey(Prof, on_delete=models.DO_NOTHING)
    filiere = models.ForeignKey(Filiere, on_delete=models.DO_NOTHING)
    Annee = models.DateField(auto_now=False, auto_now_add=False,  null=False)
    class Meta:
        unique_together = ('Niveau', 'filiere', 'prof', 'Annee')
        ordering = ['Annee', 'prof', 'Niveau']

    def __str__(self):
        return f'{self.prof.username}--{self.Niveau}--{self.filiere.Nom_filiere}'

class Domaine(models.Model):
    NomDomaine = models.CharField(max_length=100) 
    filiere = models.ForeignKey( Filiere , on_delete=models.CASCADE)
    def __str__(self):
        return self.NomDomaine







  


