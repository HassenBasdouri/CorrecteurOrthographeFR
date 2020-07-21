#IA & Data Mining
#Dr Riadh BOUSLIMI
#Hassen Basdouri
#Mini-Projet : Un correcteur orthographique
import os
import unidecode
import random
alphabet ="esiarntolucmdpgbfhzvqyxjkw" #Ordonné selon la fréquence 
#Etape 1
def CreerDico(dicoBrut):
    """retourne simplement la liste des mots du dictionnaire (sans doublon)."""
    dico =dict()
    if os.access(dicoBrut, os.R_OK):
        fichier = open(dicoBrut,"r" ,encoding='utf-8')
        contenu = fichier.readlines()
        fichier.close()
    else:
        print("Le fichier",dicoBrut,"n'existe pas")
        return
    for phrase in contenu: 
        if len(phrase.split()) >= 2:
            cle = phrase.split()[0]
            if " " not in cle and cle[0].islower():
                if cle not in dico:
                    dico[cle] = 1
    return dico.keys()

def SimplifierMot(mot):
    """ Remplace chaque caractère accentué de la chaînes de caractères mot 
    par son équivalent non accentué."""
    return unidecode.unidecode(mot)

def MotHasard(dico):
     """Retourne un mot du dictionnaire dico au hasard, sous forme simplifiée."""
     mot=random.choice(list(dico))
     return mot

def PositionsLettre(mot, lettre):
    """Retourne l'ensemble des positions où le caractère lettre apparaît dans la chaîne de 
    caractères mot et qui retourne None si le caractère n'est pas présent."""
    res = [i for i in range(len(mot)) if mot.startswith(lettre, i)] 
    return res
def RemplaceLettre(mot, lettre, lpos):
    """renvoie une copie de la chaîne mot dont les caractères dont la position 
    apparaît dans la liste lpos sont remplacés par le caractère lettre."""
    for position in lpos:
        mot = mot[:int(position)] + lettre + mot[int(position)+1:]
    return mot
def JeuDuPendu1(dico):
     """permettant de jouer au jeu du pendu. Le jeu choisira aléatoirement 
     un mot dans le dictionnaire dico et affichera le caractère * pour 
     représenter les caractères inconnus."""
     mot=MotHasard(dico)
     return (RemplaceLettre(mot,"*",range(len(mot))))
#Etape 2
def CarVersListe():
    """ demandant à l'utilisateur de saisir une suite d'entiers séparés par 
    des espaces et qui renvoie cette suite sous forme de liste d'entiers."""
    ch=input()
    if ch !="":
        l=ch.split(" ")
    else:
        l=[]
    return l
def LettreInPsotions(mot, lettre, lpos):
    """renvoie True si la chaîne mot dont les caractères dont la position 
    apparaît dans la liste lpos sont seulement  le caractère lettre."""
    var=True
    for i in range(len(mot)):
        if str(i) in lpos:
            var=var and (lettre==mot[i]) 
        else :
            var = var and mot[i]!=lettre
    return var
def JeuDuPendu2(dico):
    """  permettant à la machine de jouer au jeu du pendu.
    Le jeu demandera à l'utilisateur de choisir un mot ainsi que le nombre de lettre qu'il
    contient. A partir de là, la machine proposera différentes lettres jusqu'à trouver le mot
    secret. Si la lettre appartient au mot secret, le jeu demande à l'utilisateur de saisir au
    clavier les positions où apparaît la lettre."""
    long=int(input("Choisiez un mot, quel est le nombre de lettre qu'il contient\n"))
    dico2=[SimplifierMot(i) for i in dico if len(i)==long] 
    print("On va chereche parmi "+str(len(dico2))+" mots")
    mot="*"*long
    avance=True
    i=0
    while avance and i<len(alphabet) and len(dico2)>1:
        c=alphabet[i]
        print("Le mot contient la lettre : "+c.upper()+"?\n Si oui tapez les positions seprées par des espaces, la position du premier caracter est 0 .")
        postions=CarVersListe()
        if postions!=[]:
            mot=RemplaceLettre(mot, c, postions)
            dico2=[s for s in dico2 if  LettreInPsotions(s,c,postions)]
            print("Reste "+str(len(dico2))+" mots ")
        else:
            dico2=[s for s in dico2 if s.find(c)==-1]
            print("Reste "+str(len(dico2))+" mots ")
        if len(dico2)<10:
            print(dico2)
            print(mot)
        i+=1
        if(mot.find("*")==-1):
            avance=False
    if len(dico2)==1:
        print(mot)
        return dico2[0]
    else:
        print(dico2)
        return mot
dico=CreerDico("dico.txt")
#Etape 3
def DistanceMot(mot1, mot2):
    """retourne la distance entre deux mots."""
    distance=0
    #mettre les chaines dans des listes
    l1=[ch for ch in mot1]
    l2=[ch for ch in mot2]
    #avoir deux liste de la meme taille 
    max_length=max(len(l2),len(l1))
    l1+=[""]*(max_length-len(l1))
    l2+=[""]*(max_length-len(l2))
    
    for j, i in zip (l1,l2) :
            if i!=j:
                distance=distance+1
    return distance
def DistanceMotListe(mot, listeMots, dist): 
    """retourne la liste des mots de la liste listeMots dont la distance 
    à la chaîne de caractères mot est inférieure ou égale à dist."""
    l=[]
    for i in listeMots :
        if DistanceMot(mot,i)<= dist :
            l.append(i)
    return l 
def SuppMotListe(lettre, listeMots):
    """supprime de la liste listeMots tous les mots contenant le caractère lettre."""
    l=[]
    for mot in listeMots :
        if mot.find(lettre)==-1 :
            l.append(mot)
    return l
def StatLettre(listeMots): 
    """Renvoie le nombre d'occurrences des lettres apparaissant dans les mots
     de la liste listeMots, stockés dans une structure de dictionnaire."""
    d={}
    for mot in listeMots :
        mot=SimplifierMot(mot)
        for lettre in mot :
            if lettre not in d :
                d[lettre]=0
            else:
                d[lettre]+=1    
    return sorted(d.items(), key=lambda x: x[1], reverse=True)
def JeuDuPendu3(dico):
    """ À l'aide des fonctions précédentes, améliorez  en utilisant le liste 
    dico des mots de la langue française."""
#Etape 4
def MotContient(mot):
    """retourne la liste des lettres (sans doublon) contenues dans la chaîne de 
    caractères mot."""
    l=[]
    for i in mot :
        l.append(i)
    liste_sans = list(set(l))
    return liste_sans
def StatLettre2(listeMots): 
    """ retourne, dans une structure de dictionnaire, le nombre de mots de la liste
    listeMots dans lesquels chaque lettre apparait."""
    d={}
    for mot in listeMots :
        mot=SimplifierMot(mot)
        for lettre in mot :
            if lettre not in d :
                d[lettre]=0
            else:
                d[lettre]+=1    
    return sorted(d.items(), key=lambda x: x[1], reverse=True)
def DevinerLettre(listeMots, dejaTestes): 
    """retourne la lettre la plus pertinente parmi celles n'apparaissant pas dans 
    la liste dejaTestes, i.e. qui divise la liste listeMots de mots possibles le 
    plus parfaitement en deux."""
    c=StatLettre2(dejaTestes)[0][0]
    return (c)
#Etape 5

def Remplace1(mot):
    """Retourne la liste des mots que l'on obtient en remplacant
    chaque lettre de <mot> par toutes les autres lettres de l'alphabet
    exemple:
    >> Remplace1("moi") retournera ["aoi","boi",...,"loi","noi",...,"zoi",
                                    "mai","mbi",...,"mni","mpi",...,"mzi",
                                    "moa","mob",...,"mof","moj",...,"moz"]
    """
    l=[]
    for i in range(len(mot)):
        for j in range(len(alphabet)):
            l.append(mot[:i] + alphabet[j] + mot[i+1:])
    return l

def Supprime1(mot):
    """Retourne la liste des mots que l'on obtient en supprimant chacune 
    des lettres de <mot>
    exemple:
    >> Supprime1("arbre") retournera ["rbre","abre","arre","arbe","arbr"]
    """
    l=[]
    for i in range(len(mot)):
        l.append(mot[:i] + mot[i+1:])
    return l
  
def Ajoute1(mot):
    """Retourne la liste des mots que l'on obtient 
    en ajoutant chaque lettre de l'alphabet Ã  toutes les 
    positions du mot <mot>
    exemple
    >> Ajoute1("le") retournera ["ale","ble",...,"zle",
                                 "lae","lbe",...,"lze",
                                 "lea","leb",...,"lez"]
    """
    l=[]
    for i in range(len(mot)+1):
        for j in range(len(alphabet)):
            l.append(mot[:i] + alphabet[j] + mot[i:])
    return l
def Echange1(mot):
    """Retourne la liste des mots que l'on obtient en effectuant
    toutes les permutations de deux lettres du mot <mot>
    exemple:
    >> Echange1("lui") retournera ["uli", "iul", "liu"]
    """
    l=[]
    for i in range(len(mot)):
        for j in range(i+1,len(mot)):
            l.append(mot[:i]+mot[j] + mot[i+1:j] +mot[i]+mot[j+1:])
    return l
def Edit1(mot, dico):
    """Retourne la liste de tous les mots du dictionnaire <dico> 
    à distance d'édition 1 de <mot>
    """
    liste=[]
    l=Remplace1(mot)+Supprime1(mot)+Ajoute1(mot)+Echange1(mot)
    for i in l:
        if i in dico:
            liste.append(i)
    return(liste)
def Edit2(mot, dico):
    """retourne la liste de tous les mots du dictionnaire dico à distance d'édition 2 du mot mot."""
    edit1=Edit1(mot, dico)
    edit2=[]
    for i in edit1:
        edit2+=Edit1(i,dico)
    return edit2
def ChoixListe(l):
    """affiche les éléments de la liste l en les numérotant, demande à l'utilisateur 
    de rentrer au clavier le numéro d'un élément et le retourne."""
    choix=0
    for i in range(len(l)):
        print('-'+str(i+1)+"- "+l[i])
    while (choix <1) or (choix >len(l)):
        choix=int(input())
    return(l[int(choix)-1])
def CorrigerMot(mot, dico): 
    """énumère la liste de tous les mots du dictionnaire dico à distance d'édition 1 ou 2 
    du mot mot, propose à l'utilisateur de choisir l'orthographe correcte et renvoie le mot choisi."""
    choix=""
    mot=mot.lower()
    if mot not in dico:
        choises=Edit1(mot,dico)+Edit2(mot,dico)
        choises=list(set(choises))
        if choises !=[]:
            print("Correction de mot :' "+mot+"'\n Choix :")
            choix=ChoixListe(choises)
    else:
        return mot #Le mot mot exist dans le dictionnaire français .
    if choix!="":
        return choix
    else:
        return mot #n'existe pas des mots proches de mot mot
def CorrigerTexte(texte, dico):
    """crée une copie du texte texte en en parcourant l'ensemble des mots et en 
    corrigeant les mots mal orthographiés en demandant à l'utilisateur de choisir la bonne orthographe."""
    list=texte.split()
    newText=""
    for i in list:
        newText+=" "+CorrigerMot(str(i),dico)
    return newText
def main(dico):
    choix=int(input("___________\n-1- Jeu Du Pendu \n-2- Correcteur d'orthographe \n-3- Exite\n___________\n"))
    if choix==1:
        JeuDuPendu2(dico)
        main(dico)
    if choix==2:
        texte=input("Tapez votre texte \n")
        newText=CorrigerTexte(texte,dico)
        print("Le text :\n '"+texte+"' \n aprés correction sera :\n'"+newText+"'\n")
        main(dico)
    if choix == 3 :
        exit()
main(dico)
