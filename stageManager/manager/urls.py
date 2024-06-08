from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('afficherPdf/<int:id>/<int:n>', views.viewPdf, name='viewPdf'),
    
    
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
    path('updateEtud/<int:pk>', views.updateEtud, name='updateEtud'),
    path('deleteProf/<int:pk>', views.deleteProf, name='deleteProf'),
    path('deleteEtud/<int:pk>', views.deleteEtud, name='deleteEtud'),
    path('afficherProf/<int:pk>', views.afficherProf, name='afficherProf'),

    path('listDossiers/<str:niveau>/<str:filiere>/<int:annee>/<str:encadrant>/<str:prof>', views.listDossiers, name='listDossiers'),

    path('afficherDossierAdmin/<int:pk>/<str:prof>', views.afficherDossierAdmin, name='afficherDossierAdmin'),
    path("deleteFiliere/<int:pk>", views.deleteFiliere, name="deleteFiliere"),
    path("newfiliereAdmin/<int:pk>", views.newfiliereAdmin, name="newfiliereAdmin"),
    path('deleteSession/<int:id>', views.deleteSession, name='deleteSession'),
    path('updateSession/<str:niveau>/<str:filiere>/<int:annee>/<str:prof>', views.updateSession, name='updateSession'),
    path('domainesFilière/<str:nomFiliere>', views.domainesAdmin, name="domainesAdmin"),
    path('deleteDomaine/<str:nomFiliere>/<int:pk>', views.deleteDomaine, name='deleteDomaine'),
    path('importerEtud', views.importerEtud, name='importerEtud'),
    path('listEtuds', views.listEtuds, name='listEtuds'),
    path('afficherEtud/<int:pk>', views.afficherEtud, name='afficherEtud'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


