from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from manager.models import Dossiers, Student, StudenttFiliere, Domaine, Filiere, Prof_Filiere, Prof
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
import datetime
from django.db.models import Count
import pandas  as pd



# Login
#-----------

def index(request):
    user=None
    if request.method=='POST':
        username = request.POST["CIN"]
        password = request.POST["PW"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
        # Redirect to a success page.
            if user.role=="ETUDIANT":
                login(request, user)
                return redirect('FiliereEtud')
            elif user.role=="PROF":
                login(request, user)
                return redirect('filiereProf')
            elif user.role=="ADMIN":
                login(request, user)
                return redirect('filiereAdmin')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'CINE ou mot de passe incorrect')
            return redirect('index')
    else:
    
        return render(request, 'manager/index.html', {'user': user}) 

def deconexion(request):
    logout(request)
    return redirect('index')


# Etudiant
#-----------
def filiereEtudiant(request):
    if request.user.is_authenticated and request.user.role == 'ETUDIANT':
        FiliereEtud = StudenttFiliere.objects.filter(Etudiant=request.user)
        context = {'Filieres':FiliereEtud, 'user_name':request.user.username,  'first_name':request.user.first_name, 'last_name':request.user.last_name}
        return render(request, 'manager/FiliereEtud.html',context = context)
    else:
        return redirect('index')

def newdossier(request, niveau, nom_filier,year, cin):
    if request.user.is_authenticated and request.user.role == 'ETUDIANT':
        f=Filiere.objects.get(Nom_filiere=nom_filier)
        sf = StudenttFiliere.objects.get(Etudiant = request.user, Niveau=niveau, Filiere=f)
        d = Domaine.objects.filter(filiere = sf.Filiere.pk)
        pfs=Prof_Filiere.objects.filter(Niveau=niveau, filiere=f)
        profs=[]
        for pf in pfs:
            profs.append(pf.prof)
        ds=Dossiers.objects.filter(Student=request.user, Niveau=niveau)
        if request.method=='POST':
            typ = request.POST['Type']
            rapport=request.FILES['Rapport']
            dossier=request.FILES['Dossier']
            sujet=request.POST['Sujet']
            encadrant=request.POST['Encadrant']
            domaine=request.POST['Domaine']
            student=request.user
            
            if rapport != '' and dossier != '' and sujet != '':
                    if ds.count() < 2 :
                        d=Dossiers.objects.create(Type=typ, Rapport=rapport, Doss=dossier, Sujet=sujet, Encadrant=encadrant, Domaine=domaine, Nom_filiere=nom_filier, Niveau=niveau,  Student=student, Year=f'{year}-01-01')
                    else:
                        messages.error(request, 'Maximum de dossiers atteints !')
            else:
                messages.error(request, 'Champs Vide ou invalide!')

            url = reverse('home', kwargs={'niveau': niveau, 'nom_filier':nom_filier, 'year':year, 'cin':None})
            return redirect(url)    
        else:
            return render(request, 'manager/newdossier.html', { 'TypesStage': Dossiers.TYPES , 'domaines': d, 'cin':cin, 'niveau':niveau , 'year':year,  'nom_filier':nom_filier, 'profs':profs })
    else:
        return redirect('index')

def home(request, niveau, nom_filier,year, cin):
   if request.user.is_authenticated and request.user.role == 'ETUDIANT':
        dossiers = Dossiers.objects.filter(Student =request.user, Niveau=niveau, Nom_filiere=nom_filier, Year=f'{year}-01-01').order_by('Type')
        context = {'dossiers':dossiers, 'user_name':request.user.username,  'first_name':request.user.first_name, 'last_name':request.user.last_name, 'niveau':niveau, 'nom_filier':nom_filier, 'year':year, 'cin':cin}
        return render(request, 'manager/home.html',context = context)
   else:
        return redirect('index')

def deleteFilier(request, pk, niveau, year):
    #si valider ou commenter n'est pas effacer
    if request.user.is_authenticated and request.user.role == 'ETUDIANT':
        if request.method == 'POST':
            f= Filiere.objects.get(pk=pk)
            s=request.user
            sf = StudenttFiliere.objects.get(Etudiant=s, Filiere=f, Niveau=niveau, Year=f'{year}-01-01')
            dossiers = Dossiers.objects.filter(Student=s, Nom_filiere=f.Nom_filiere, Niveau=niveau, Year=f'{year}-01-01')
            if dossiers.count() != 0:
                messages.warning(request, "Cette Session contient des dossiers veuillez les supprimer d'abord!")
            else:
                sf.delete()
            return redirect('FiliereEtud')
    else:
        return redirect('index')
    
def newFiliere(request):
    if request.user.is_authenticated and request.user.role == 'ETUDIANT':
        student=request.user
        sfs = Prof_Filiere.objects.values('Niveau', 'filiere').annotate(count=Count('id')).values('Niveau', 'filiere').order_by('Niveau', 'filiere')
        sessions=[]

        for sf in sfs:
            sessions.append({ 'Niveau':sf['Niveau'], 'filiere': Filiere.objects.get(pk=sf['filiere'])})
        if request.method=='POST':
            data=request.POST['NomFiliere']
            annee=request.POST['Annee']
            data_list=data.split('*')
            f=Filiere.objects.get(Nom_filiere=data_list[1])
            result=Prof_Filiere.objects.filter(Niveau=data_list[0], Annee=f"{annee}-01-01", filiere=f)
            if result.count() == 0:
                messages.error(request, f"Cette session pour l'année {annee} n'existe pas essayer avec une  autre année!")
                return render(request, 'manager/newFiliere.html', {'sessions': sessions})
            else:
                try:
                    StudenttFiliere.objects.create(Etudiant=student, Filiere=f, Year=f"{annee}-01-01", Niveau=data_list[0]) 
                except IntegrityError:
                    messages.error(request, 'Cette Année universitaire exist déja !')
                    return render(request, 'manager/newFiliere.html', {'sessions': sessions})
            return redirect('FiliereEtud')
        else:
            return render(request, 'manager/newFiliere.html', {'sessions': sessions})
    else:
        return redirect('index')
    
def afficherdossier(request, pk):
    if request.user.is_authenticated and request.user.role == 'PROF':
        if request.method == 'POST':
            d = Dossiers.objects.get(pk=pk)
            val = request.POST.get('val')
            remarqProf=request.POST.get('remarqProf')
            if val == "on":
                d.ValidationProf = 1
            else:
                d.ValidationProf = 0
            d.RemarqueProf=remarqProf
            d.save()
            checked=d.ValidationProf
            url = reverse('homeProf', kwargs={'niveau': d.Niveau, 'nom_filier':d.Nom_filiere, 'annee':d.Year.year, 'cin':d.Student.username})
            return redirect(url)
        d = Dossiers.objects.get(pk=pk)
        checked=d.ValidationProf
        context = { 'dossier':d, 'checked': checked, 'Etudiant':d.Student, 'niveau': d.Niveau, 'nom_filier':d.Nom_filiere, 'annee':d.Year.year, 'cin':d.Student.username}
        return render(request, 'manager/afficherdossierProf.html', context=context)
    elif request.user.is_authenticated and request.user.role == 'ETUDIANT':
        d = Dossiers.objects.get(pk=pk)
        checked=d.ValidationProf
        context = { 'dossier':d, 'checked': checked, 'Etudiant':d.Student}
        return render(request, 'manager/afficherdossier.html', context=context)


def viewPdf(request, id, n):
    pdf = Dossiers.objects.get(id=id)
    return render(request, 'manager/viewPdf.html', {'pdf': pdf, 'n':n})

def register(request):
    if request.method =='POST':
        Napog=request.POST['Napog']
        CIN=request.POST['CIN']
        CNE=request.POST['CNE']
        SEX=request.POST['Sex']
        Nom=request.POST['Nom']
        prenom=request.POST['prenom']
        adresse=request.POST['adresse']
        tel=request.POST['tel']
        DateN=request.POST['DateN']
        LieuxN=request.POST['LieuxN']
        pw1=request.POST['pw1']
        pw2=request.POST['pw2']

        

        if pw1 != pw2:
            erreur ="Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau."
            context = {'register': True, 'erreur':erreur, 'Napog':Napog, 'CIN':CIN, 'CNE':CNE, 'Nom':Nom, 'prenom':prenom,'adresse':adresse, 'tel':tel, 'DateN':DateN, 'LieuxN':LieuxN, 'SEX':Student.SEX}
            return render(request, 'manager/enregistrement.html', context=context)
    
        Student.objects.create_user(Napog=Napog, username=CIN, CNE=CNE, Sex=SEX, first_name=prenom, last_name=Nom, adresse=adresse,  tel=tel, dateN=DateN, lieuxN=LieuxN, password=pw1)
        
        return redirect('listEtuds')
    context = {'register': True, 'SEX':Student.SEX}
    return render(request, 'manager/enregistrement.html', context=context)

def deletedossier(request, pk):
    d=Dossiers.objects.get(pk=pk)
    niveau=d.Niveau
    nom_filier=d.Nom_filiere
    year=d.Year
    d.delete()
    url = reverse('home', kwargs={'niveau':niveau , 'nom_filier':nom_filier, 'year':year.year, 'cin':None })
    return redirect(url)

def updatedossier(request, pk):
    if request.method =='POST':
        
        typ=request.POST['Type']
        rapport=request.POST['Rapport']
        doss=request.POST['Dossier']
        sujet=request.POST['Sujet']
        encadrant=request.POST['Encadrant']
        domaine=request.POST['Domaine']
        

        dossier = Dossiers.objects.get(pk=pk)

        dossier.Type = typ
        dossier.Rapport=rapport
        dossier.Doss =doss
        dossier.Sujet =sujet
        dossier.Encadrant=encadrant
        dossier.Domaine=domaine
        dossier.save()
        url = reverse('home', kwargs={'niveau': dossier.Niveau, 'nom_filier':dossier.Nom_filiere, 'year':dossier.Year.year , 'cin':None})
        return redirect(url)
    
    
    dossier = Dossiers.objects.get(pk=pk)
    f=Filiere.objects.get(Nom_filiere=dossier.Nom_filiere)
    sf = StudenttFiliere.objects.get(Etudiant = request.user, Niveau=dossier.Niveau, Year=f'{dossier.Year.year}-01-01' , Filiere=f)
    d = Domaine.objects.filter(filiere = sf.Filiere.pk)

    pfs=Prof_Filiere.objects.filter(Niveau=dossier.Niveau , filiere=f)
    profs=[]
    for pf in pfs:
        data={'prof':pf.prof, 'name':pf.prof.first_name+' '+pf.prof.last_name}
        profs.append(data)
    context = { 'dossier':dossier, 'TypesStage': Dossiers.TYPES , 'domaines': d, 'profs':profs}
    return render(request, 'manager/updatedossier.html', context=context)


#Prof
def filiereProf(request):
    if request.user.is_authenticated and request.user.role == 'PROF':
        annee=datetime.date.today().year
        FiliereProfe = Prof_Filiere.objects.filter(prof =request.user, Annee=f'{annee}-01-01')
        
        if request.method == 'POST':
            annee=request.POST['Annee']
            FiliereProfe = Prof_Filiere.objects.filter(prof =request.user, Annee=f'{annee}-01-01')


        context = {'Filieres':FiliereProfe, 'user_name':request.user.username,  'first_name':request.user.first_name, 'last_name':request.user.last_name, 'Annee':annee}
        return render(request, 'manager/FiliereProf.html',context = context)
    else:
        return redirect('index')

def etudiantsFiliere(request, niveau, filiere, annee):
    if request.user.is_authenticated and request.user.role == 'PROF':
        encadrant=request.user.first_name+' '+request.user.last_name
        #f=Filiere.objects.get(Nom_filiere=filiere)
        etudiants=Student.student.filter(dossiers__Encadrant=encadrant, dossiers__Niveau=niveau, dossiers__Year=f'{annee}-01-01', dossiers__Nom_filiere=filiere ).distinct()
        context={'etudiants':etudiants, 'filiere':filiere, 'niveau':niveau, 'user_name':request.user.username, 'annee':annee,  'first_name':request.user.first_name, 'last_name':request.user.last_name }
        return render(request, 'manager/etudiantsFiliere.html',context = context)
    else:
        return redirect('index')

def homeProf(request, niveau, nom_filier, annee, cin):
    if request.user.is_authenticated and request.user.role == 'PROF':
        e=Student.student.get(username=cin)
        encadrant=request.user.first_name+' '+request.user.last_name
        dossiers = Dossiers.objects.filter(Student =e, Niveau=niveau, Year=f'{annee}-01-01', Encadrant=encadrant,  Nom_filiere=nom_filier).order_by('Type')
        context = {'dossiers':dossiers, 'user_name':e.username,  'first_name':e.first_name, 'last_name':e.last_name, 'niveau':niveau, 'annee':annee, 'nom_filier':nom_filier, 'role':request.user.role }
        return render(request, 'manager/homeProf.html',context = context)
    else:
        return redirect('index')


#Admin
def filieresAdmin(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        filieres = Filiere.objects.all()
        cs=[]
        for filiere in filieres:
            cs.append({'filiere' :filiere, 'number':Prof_Filiere.objects.filter(filiere=filiere).count()})
        context={'filieres':cs, 'user_name':request.user.username,  'first_name':request.user.first_name, 'last_name':request.user.last_name}
        return render(request, 'manager/filiereAdmin.html', context=context)
  
def updateFiliere(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        filiere=Filiere.objects.get(pk=pk)
        annee=f'{datetime.date.today().year}-01-01'
        pfs=Prof_Filiere.objects.filter(filiere=filiere, Annee=annee)
        if request.method == 'POST':

            form=request.POST['form_type']
            if form == "form1":
                nom=request.POST['nomFil']
                filiere.Nom_filiere=nom
                filiere.save()
                return redirect('filiereAdmin')
            elif form == "form2":
                a=request.POST['Annee']
                annee=f'{a}-01-01'
                pfs=Prof_Filiere.objects.filter(filiere=filiere, Annee=annee)
                return render(request, 'manager/updateFiliereAdmin.html', {'filiere':filiere, 'Sessions':pfs, 'Annee':a})
        a=datetime.date.today().year
        return render(request, 'manager/updateFiliereAdmin.html', {'filiere':filiere, 'Sessions':pfs, 'Annee':a})
        
    else:
        return redirect('index')
    
def ajoutFilierAdmin(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method == 'POST':
            nom=request.POST['nomFil']
            try:
                Filiere.objects.create(Nom_filiere=nom)
            except IntegrityError:
                messages.error(request, "Ce Nom de  filière existe déja!")
            return redirect('filiereAdmin')
        return render(request, 'manager/ajoutFilierAdmin.html')
    else:
        return redirect('index')      
    
def listProfs(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        profs=Prof.prof.all()
        return render(request, 'manager/listeProfs.html', {'profs':profs})
    
def afficherProf(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        p=Prof.prof.get(pk=pk)
        return render(request, 'manager/AfficherProf.html', {'prof':p})

def ajoutProf(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method =='POST':
            CIN=request.POST['CIN']
            Nom=request.POST['Nom']
            prenom=request.POST['prenom']
            adresse=request.POST['adresse']
            tel=request.POST['tel']
            DateN=request.POST['DateN']
            LieuxN=request.POST['LieuxN']
            spc=request.POST['spc']
            
            pw=CIN+'@est.fbs'
            notok=False
            try: 
                Prof.objects.create_user( username=CIN, first_name=prenom, last_name=Nom, adresse=adresse,  tel=tel, dateN=DateN, lieuxN=LieuxN, SPC=spc, password=pw)
            
            except:
                notok=True
                messages.error(request, 'Champs invalides ou manquant')
            
            if notok:                   
                context = {'register': True, 'CIN':CIN, 'Nom':Nom, 'prenom':prenom, 'adresse':adresse, 'tel':tel, 'DateN':DateN, 'LieuxN':LieuxN, 'spc':spc}
                return render(request, 'manager/ajoutProf.html', context=context)
            else:
                return redirect('listProfs')
         
        else:                       
            context = {'register': True }
            return render(request, 'manager/Admin/ajoutProf.html', context=context)

def updateProf(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        p=Prof.prof.get(pk=pk)
        if request.method =='POST':
            
            CIN=request.POST['CIN']
            Nom=request.POST['Nom']
            prenom=request.POST['prenom']
            adresse=request.POST['adresse']
            tel=request.POST['tel']
            DateN=request.POST['DateN']
            LieuxN=request.POST['LieuxN']
            spc=request.POST['spc']

            p.username=CIN
            p.first_name=prenom
            p.last_name=Nom
            p.adresse=adresse
            p.tel=tel
            p.dateN=DateN
            p.lieuxN=LieuxN
            p.SPC=spc
            p.set_password(CIN+'@est.fbs')
            p.save() 
           

            return redirect('listProfs')
        return render(request, 'manager/updateProf.html', {'prof':p})

def deleteProf(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        pfs=Prof_Filiere.objects.filter(prof__pk=pk)
        for pf in pfs:
            pf.delete()
        p=Prof.prof.get(pk=pk)
        print(p)
        p.delete()
        return redirect('listProfs')

def deleteSession(request, id):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method=='POST':
            ps=Prof_Filiere.objects.get(id=id)
            pk=ps.filiere.pk
            es=StudenttFiliere.objects.filter(Niveau=ps.Niveau, Filiere=ps.filiere, Year=ps.Annee)
            if es.count()==0:
                ps.delete()
            else:
                messages.error(request, 'Cette session contient des etudiants! ')
   
        url = reverse('updateFiliere', kwargs={'pk': pk})
        return redirect(url)

def updateSession(request, niveau, filiere, annee, prof):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        f=Filiere.objects.get(Nom_filiere=filiere)
        n=StudenttFiliere.NIVEAUX
        profs=Prof.prof.all()
        es=StudenttFiliere.objects.filter(Niveau=niveau, Filiere=f, Year=f'{annee}-01-01')
        if es.count() == 0:
            if request.method == 'POST':
                n=request.POST['niveau']
                profPK=request.POST['profPk']
                a=request.POST['Annee']
                p=Prof.prof.get(username=prof)
                pf=Prof_Filiere.objects.get(Niveau=niveau, prof=p, filiere=f, Annee=f'{annee}-01-01')
                pf.Niveau=n
                pf.prof=p
                pf.Annee=f'{a}-01-01'
                pf.save()
                url = reverse('updateFiliere', kwargs={'pk': f.pk})
                return redirect(url)

            return render(request, 'manager/updateSession.html', {'filiere':f, 'Niveaux':n, 'profs':profs, 'niveau':niveau, 'prof':prof, 'annee':annee})
        else:
            messages.error(request, 'Cette session contient des etudiants! ')
            url = reverse('updateFiliere', kwargs={'pk': f.pk})
            return redirect(url)
        
def listEtudiants(request, niveau, filiere, annee, prof):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        p=Prof.prof.get(username=prof)
        f=Filiere.objects.get(Nom_filiere=filiere)
        
        encadrant=p.first_name+' '+p.last_name
        etudiants=Student.student.filter(dossiers__Encadrant=encadrant, dossiers__Niveau=niveau, dossiers__Year=f'{annee}-01-01', dossiers__Nom_filiere=filiere ).distinct()
        return render(request, 'manager/listEtudiantsSession.html', {'pk':f.pk, 'etudiants':etudiants, 'niveau':niveau, 'filiere':filiere, 'annee':annee, 'encadrant':encadrant, 'prof':prof  })



def deleteFiliere(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method == 'POST':

            f=Filiere.objects.get(pk=pk)
            profFiliere=Prof_Filiere.objects.filter(filiere=f)
            etudiantFiliere=StudenttFiliere.objects.filter(Filiere=f)
            if profFiliere.count() == 0 and etudiantFiliere.count() == 0 :
                f.delete()
            else:
                messages.info(request, "Cette Filiers est reliée a des étudiant ou des professeur Veuillez les deconnecter d'abords")
            filieres=Filiere.objects.all()
            sc=[]
            for filiere in filieres:
                sc.append({'filiere':filiere, 'number':Prof_Filiere.objects.filter(filiere=filiere).count()})
            context={'filieres':sc, 'user_name':request.user.username,  'first_name':request.user.first_name, 'last_name':request.user.last_name}
            return render(request, 'manager/filiereAdmin.html', context=context)

def newfiliereAdmin(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        
        n=StudenttFiliere.NIVEAUX
        f=Filiere.objects.get(pk=pk)
        profs=Prof.prof.all()
        if request.method == 'POST':
            niveau=request.POST['niveau']
            profPK=request.POST['profPk']
            annee=request.POST['Annee']
            prof=Prof.prof.get(pk=profPK)
            f=Filiere.objects.get(pk=pk)
            notOk=False
            try:
                Prof_Filiere.objects.create(prof=prof, filiere=f, Niveau=niveau, Annee=f'{annee}-01-01')
            except IntegrityError:
                notOk=True
                error_message = "Une erreur s'est produite : Cette Session existe déjà. Veuillez saisir une session unique."
                messages.error(request, error_message)
            if notOk:
                
                return render(request, 'manager/newfiliereAdmin.html', {'filiere':f, 'Niveaux':n, 'profs':profs })
            else:
                
                url = reverse('updateFiliere', kwargs={'pk': pk})
                return redirect(url)
        return render(request, 'manager/newfiliereAdmin.html', {'filiere':f, 'Niveaux':n, 'profs':profs })

def listDossiers(request, niveau, filiere, annee, encadrant, prof):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        ds=Dossiers.objects.filter(Nom_filiere=filiere, Niveau=niveau, Year=f'{annee}-01-01', Encadrant=encadrant)
        e=ds.first().Student
        return render(request, 'manager/listDossiers.html', {'dossiers':ds, 'niveau':niveau,  'filiere':filiere, 'annee':annee, 'prof':prof, 'etudiant':e })
    

def afficherDossierAdmin(request, pk, prof):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        dossier=Dossiers.objects.get(pk=pk)
        if request.method == 'POST':
            val = request.POST.get('valA')
            remarqAdmin=request.POST.get('remarqAdmin')
            if val == "on":
                dossier.ValidationAdmin = 1
            else:
                dossier.ValidationAdmin = 0
            dossier.RemarqueAdmin=remarqAdmin
            dossier.save()
            url = reverse('listDossiers', kwargs={'niveau': dossier.Niveau, 'filiere': dossier.Nom_filiere, 'annee': dossier.Year.year, 'encadrant': dossier.Encadrant, 'prof':prof } )
            return redirect(url)
        return render(request, 'manager/afficherDossierAdmin.html', {'dossier':dossier, 'prof':prof})

def domainesAdmin(request, nomFiliere):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        f=Filiere.objects.get(Nom_filiere=nomFiliere)
        if request.method ==  'POST':
            domaine=request.POST['domaine']    
            Domaine.objects.create(NomDomaine=domaine, filiere=f)
        domaines=Domaine.objects.filter(filiere=f)   
        context={'Filiere':f, 'domaines':domaines }
        return render(request, 'manager/domainesAdmin.html', context)
    
def deleteDomaine(request,nomFiliere, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method == 'POST':
            d=Domaine.objects.get(pk=pk)
            d.delete()
        f=Filiere.objects.get(Nom_filiere=nomFiliere)
        domaines=Domaine.objects.filter(filiere=f)   
        context={'Filiere':f, 'domaines':domaines }
        return render(request, 'manager/domainesAdmin.html', context)

def listEtuds(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        etuds=Student.student.all()
        return render(request, 'manager/listeEtuds.html', {'etuds':etuds})

def afficherEtud(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        e=Student.student.get(pk=pk)
        return render(request, 'manager/AfficherEtud.html', {'Etudiant':e})

def updateEtud(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        e=Student.student.get(pk=pk)
        if request.method =='POST':

            Napoge=request.POST['Napog']
            CIN=request.POST['CIN']
            CNE=request.POST['CNE']
            sex=request.POST['Sex']
            Nom=request.POST['Nom']
            prenom=request.POST['prenom']
            adresse=request.POST['adresse']
            tel=request.POST['tel']
            DateN=request.POST['DateN']
            LieuxN=request.POST['LieuxN']

            e.Napog=Napoge
            e.username=CIN
            e.CNE=CNE
            e.first_name=prenom
            e.last_name=Nom
            e.Sex=sex
            e.adresse=adresse
            e.tel=tel
            e.dateN=DateN
            e.lieuxN=LieuxN
            e.save() 
           

            return redirect('listEtuds')
        return render(request, 'manager/updateEtud.html', {'Etudiant':e})


def importerEtud(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        if request.method == "POST" and request.FILES['file']:
            excel_file = request.FILES['file']
            try:
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    Student.objects.create_user(
                    Napog=row['N Apog'],
                    username=row['CIN'],
                    CNE=row['CNE'],
                    Sex=row['SEX'],
                    last_name=row['NOM'],
                    first_name=row['PRENOM'],
                    adresse=row['ADRESSE'],
                    tel=row['TEL'],
                    dateN=row['DATE Naissance'],
                    lieuxN=row['Lieux Naissance'],
                    password=row['mot de passe']
                    )
                redirect('listEtuds')
            except Exception as e:

                messages.error(request, f'Error importing data: {e}')
            etuds=Student.student.all()
            return render(request, 'manager/listeEtuds.html', {'etuds':etuds})


def deleteEtud(request, pk):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        fetuds=StudenttFiliere.objects.filter(Etudiant__pk=pk)
        for fetud in fetuds:
            fetud.delete()
        e=Student.student.get(pk=pk)
        e.delete()
        return redirect('listEtuds')
