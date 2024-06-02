from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    # Login
    path('', views.index, name='index'),
     path('logout/', views.deconexion, name='logout'),

    #Etudiant
    path('FiliereEtudiant/', views.filiereEtudiant, name='FiliereEtud'),
    path('newFiliere/', views.newFiliere, name='newFiliere'),
    path('home/<str:niveau>/<str:nom_filier>/<int:year>/<str:cin>', views.home, name='home'),
    path('newdossier/<str:niveau>/<str:nom_filier>/<int:year>/<str:cin>', views.newdossier, name='newdossier'),
    path('register/', views.register, name='register'),
    path('deleteFilier/<int:pk>/<str:niveau>/<int:year>', views.deleteFilier, name='deleteFilier'),
    
    
    
    #Prof
    path('homeProf/<str:niveau>/<str:nom_filier>/<int:annee>/<str:cin>', views.homeProf, name='homeProf'),
    path('delete/<int:pk>', views.deletedossier, name='deletedossier'),
    path('afficherdossier/<int:pk>', views.afficherdossier, name='afficherdossier'),
    path('updatedossier/<int:pk>', views.updatedossier, name='updatedossier'),
    path('filiereProf/', views.filiereProf, name='filiereProf'),
    path('etudiantsFil/<str:niveau>/<str:filiere>/<int:annee>', views.etudiantsFiliere, name='etudiantsFil'),
    
    
    
    #Admin
    path('filiereAdmin/', views.filieresAdmin, name='filiereAdmin'),

    path('ajoutFilierAdmin/', views.ajoutFilierAdmin, name='ajoutFilierAdmin'),
    path('updateFiliere/<int:pk>', views.updateFiliere, name='updateFiliere'),

    path('listEtudiants/<str:niveau>/<str:filiere>/<int:annee>/<str:prof>', views.listEtudiants, name='listEtudiants'),

    

    path('listeProfs/', views.listProfs, name='listProfs'),
    path('ajoutProf/', views.ajoutProf, name='ajoutProf'),
    path('updateProf/<int:pk>', views.updateProf, name='updateProf'),
    path('deleteProf/<int:pk>', views.deleteProf, name='deleteProf'),
    path('afficherProf/<int:pk>', views.afficherProf, name='afficherProf'),

    path('listDossiers/<str:niveau>/<str:filiere>/<int:annee>/<str:encadrant>/<str:prof>', views.listDossiers, name='listDossiers'),

    path('afficherDossierAdmin/<int:pk>/<str:prof>', views.afficherDossierAdmin, name='afficherDossierAdmin'),
    path("deleteFiliere/<int:pk>", views.deleteFiliere, name="deleteFiliere"),
    path("newfiliereAdmin/<int:pk>", views.newfiliereAdmin, name="newfiliereAdmin"),
    path('deleteSession/<int:id>', views.deleteSession, name='deleteSession'),
    path('updateSession/<str:niveau>/<str:filiere>/<int:annee>/<str:prof>', views.updateSession, name='updateSession'),
]


