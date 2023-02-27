# -*- coding: utf-8 -*-

import numpy as np
from random import *
import random
import copy
import time

#Fonctions obligatoires#

def affiche_plateau(L_joueurs):
    M=np.array([["A1","B1","C1","D1","E1"],["A2","B2","C2","D2","E2"],["A3","B3","C3","D3","E3"],["A4","B4","C4","D4","E4"],["A5","B5","C5","D5","E5"]])
    for i in range(0,len(M)):
        for j in range(0,len(M)):
            for k in L_joueurs:
                if k['pos']==M[i,j]:
                    M[i,j]=k['pion']
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j]!="X" and M[i,j]!="O" and M[i,j]!="Y" and M[i,j]!="Z":
                M[i,j]="."
    print("   | A B C D E |")
    print("---- - - - - - |")
    print("1  | {} {} {} {} {} |".format(M[0,0],M[0,1],M[0,2],M[0,3],M[0,4]))
    print("2  | {} {} {} {} {} |".format(M[1,0],M[1,1],M[1,2],M[1,3],M[1,4]))
    print("3  | {} {} {} {} {} |".format(M[2,0],M[2,1],M[2,2],M[2,3],M[2,4]))
    print("4  | {} {} {} {} {} |".format(M[3,0],M[3,1],M[3,2],M[3,3],M[3,4]))
    print("5  | {} {} {} {} {} |".format(M[4,0],M[4,1],M[4,2],M[4,3],M[4,4]))
    print(16*"-")
    return None

def affiche_cartes(L_cartes):
    L=", ".join(L_cartes)
    print(L)
    return None

def valeur(c):
    if c[0]=="0":
        valeur=10
    elif c[0]=="V":
        valeur=11
    elif c[0]=="D":
        valeur=12
    elif c[0]=="R":
        valeur=13
    elif c[0]=="1" and c[1]!="0":
        valeur=14
    elif c[0]=="J":
        valeur=15
    else:
        valeur=int(c[0])
    return valeur

def KO(joueur):
    if joueur['pv']>0:
        return False
    else:
        return True

def nb_KO(L_joueurs):
    nbKO=0
    for joueur in L_joueurs:
        if KO(joueur):
            nbKO=nbKO+1
    return nbKO

def voisins(direction,case):
    R=[]
    M=np.array([["A1","B1","C1","D1","E1"],["A2","B2","C2","D2","E2"],["A3","B3","C3","D3","E3"],["A4","B4","C4","D4","E4"],["A5","B5","C5","D5","E5"]])
    for i in range(0,len(M)):
        for j in range(0,len(M)):
            if M[i,j]==case:
                C=j
                L=i
    if direction=="ortho":
        Co=M[:,C]
        Lo=M[L,:]
        if L>=1 and L<=3:
            R.append(Co[L-1])
            R.append(Co[L+1])
        elif L==0:
            R.append(Co[L+1])
        else:
            R.append(Co[L-1])
        if C>=1 and C<=3:
            R.append(Lo[C-1])
            R.append(Lo[C+1])
        elif C==0:
            R.append(Lo[C+1])
        else:
            R.append(Lo[C-1])
        return R
    elif direction=="diag":
        if L>=1 and C>=1:
            for k in M[L-1,:]:
                for l in M[:,C-1]:
                    if k==l:
                        R.append(k)
        if L>=1 and C<=3:
            for k in M[L-1,:]:
                for l in M[:,C+1]:
                    if k==l:
                        R.append(k)
        if L<=3 and C>=1:
            for k in M[L+1,:]:
                for l in M[:,C-1]:
                    if k==l:
                        R.append(k)
        if L<=3 and C<=3:
            for k in M[L+1,:]:
                for l in M[:,C+1]:
                    if k==l:
                        R.append(k)
        return R

def est_voisin(j1,j2,direction):
    J1=voisins(direction,j1['pos'])
    if j2['pos'] in J1:
            return True
    return False

def init_pioche():
    C=['1C','7C','8C','9C','0C']
    K=['1K','7K','8K','9K','0K']
    P=['1P','7P','8P','9P','0P']
    T=['1T','7T','8T','9T','0T']
    J=['J1','J2']   
    V=['VC','VK','VP','VT']
    D=['DC','DK','DP','DT']
    R=['RC','RK','RP','RT']
    jeu=C+K+P+T+J+V+D+R
    random.shuffle(jeu)
    return jeu

def init_defausse():
    defausse=[]
    return defausse

def defausse2pioche(defausse,pioche):
    pioche.extend(defausse)
    random.shuffle(pioche)
    for i in range(0,len(defausse)):
        del defausse[0]
    return None

def est_vide(paquet):
    if paquet==[]:
        return True
    else:
        return False

def pioche_cartes(n,L_cartes):
    L_cartes1=copy.deepcopy(L_cartes[-n:])
    for i in range(n):
        del L_cartes[-1]
    return L_cartes1

def init_joueurs(n,pioche):
    if n<2 or n>4:
        return "Impossible, le jeu se joue avec 2 à 4 joueurs."
    else:
        jeu=[]
        if n==2:
            joueur1=dict(pion='X',pos='A1',pv=10,cartes=pioche_cartes(5,pioche))
            joueur2=dict(pion='O',pos='E5',pv=10,cartes=pioche_cartes(5,pioche))
            jeu.append(joueur1)
            jeu.append(joueur2)
        elif n==3:
            joueur1=dict(pion='X',pos='A1',pv=10,cartes=pioche_cartes(5,pioche))
            joueur2=dict(pion='O',pos='E1',pv=10,cartes=pioche_cartes(5,pioche))
            joueur3=dict(pion='Y',pos='E5',pv=10,cartes=pioche_cartes(5,pioche))
            jeu.append(joueur1)
            jeu.append(joueur2)
            jeu.append(joueur3)
        else:
            joueur1=dict(pion='X',pos='A1',pv=10,cartes=pioche_cartes(5,pioche))
            joueur2=dict(pion='O',pos='E1',pv=10,cartes=pioche_cartes(5,pioche))
            joueur3=dict(pion='Y',pos='E5',pv=10,cartes=pioche_cartes(5,pioche))
            joueur4=dict(pion='Z',pos='A5',pv=10,cartes=pioche_cartes(5,pioche))
            jeu.append(joueur1)
            jeu.append(joueur2)
            jeu.append(joueur3)
            jeu.append(joueur4)
        return jeu
            
#Fonctions en plus# 
    
def start(pioche,jeu):
    save=[]
    for l in range(0,len(jeu)):
        jeu[l]['joueur']="joueur {}".format(l+1)
        J=random.sample(pioche,1)
        j="".join(J)
        Vj=valeur(j)
        pioche.remove(j)
        save.append(j)
        jeu[l]['carte1']=j
        jeu[l]['Vcarte1']=Vj
    pioche=pioche+save
    random.shuffle(pioche)
    for k in range(len(jeu)):
        print("{} a pioché la carte {}.".format(jeu[k]['joueur'],jeu[k]['carte1']))
        time.sleep(3)
    ordre=sorted(jeu, key=lambda t: t['Vcarte1'], reverse=True)
    while ordre[0]['Vcarte1']==ordre[1]['Vcarte1']:
        nb=len(ordre)-1
        while ordre[0]['Vcarte1']!=ordre[nb]['Vcarte1']:
            del ordre[nb]
            nb=nb-1
        print("\n")
        time.sleep(2)
        if len(jeu)>2:
            print("Les joueurs suivants vont donc devoir repiocher une carte pour pouvoir départager : ")
            for i in ordre:
                time.sleep(1)
                print("- "+i['joueur'])
        else:
            print("Les joueurs ont pioché des cartes de même valeur. Ils vont donc repiocher pour pouvoir départager.")
        time.sleep(3)
        print("\n")
        save=[]
        for l in range(0,len(ordre)):
            J=random.sample(pioche,1)
            j="".join(J)
            Vj=valeur(j)
            pioche.remove(j)
            save.append(j)
            ordre[l]['carte1']=j
            ordre[l]['Vcarte1']=Vj
        pioche=pioche+save
        random.shuffle(pioche)
        print("\n")
        time.sleep(2)
        for k in range(len(ordre)):
            print("{} a pioché la carte {}.".format(ordre[k]['joueur'],ordre[k]['carte1']))
            time.sleep(3)
        ordre=sorted(ordre, key=lambda t: t['Vcarte1'], reverse=True)
    print("\n")
    if len(jeu)>2:
        print("Donc {} commence puis on tournera dans le sens horaire.".format(ordre[0]['joueur']))
    else:
        print("Donc {} commence.".format(ordre[0]['joueur']))
    nb=0
    while jeu[nb]!=ordre[0]:
        jeu.append(jeu[nb])
        nb=nb+1
    for i in range(0,nb):
        del jeu[0]
    return None

def cartes_couleur(main):
    compteur=[0,0,0]
    for i in main:
        if i[0]=="J":
            compteur[0]=compteur[0]+1
        elif i[1]=="C" or i[1]=="K":
            compteur[1]=compteur[1]+1
        else:
            compteur[2]=compteur[2]+1
    return compteur

def cartes_tour(jeu,defausse,pioche):
    for joueur in jeu:
        time.sleep(2)
        print("C'est au tour de {} de jouer.\n".format(joueur['pion']))
        CJ=[]
        if KO(joueur)==True and joueur['pos']=="00":
            continue
        else:
            if len(joueur['cartes'])>=3:
                NbCJ=randint(1,3)
            elif len(joueur['cartes'])==2:
                NbCJ=randint(1,2)
            elif len(joueur['cartes'])==1:
                NbCJ=1
            else:
                joueur['pv']=joueur['pv']-1
            for i in range(0,NbCJ):
                main=cartes_couleur(joueur['cartes'])
                voisin=[]
                for k in range(len(jeu)):
                    if jeu[k]['pion']!=joueur['pion'] and jeu[k]['pv']!="00":
                        if est_voisin(joueur,jeu[k],"ortho")==True or est_voisin(joueur,jeu[k],"diag")==True:
                            voisin.append(jeu[k])
                r=cartes_attaque(joueur)
                VO=[]
                VD=[]
                for v in range(0,len(voisin)):
                    if voisin[v]['pos'] in voisins("ortho",joueur['pos']):
                        VO.append(voisin[v])
                    else:
                        VD.append(voisin[v])
                if i==0:
                    if (len(voisin)==0 or main[0]==0) and (len(VO)==0 or r[1]==0) and (len(VD)==0 or r[0]==0) and main[2]==0:
                        joueur['cartes']=sorted(joueur['cartes'], key=lambda t: valeur(t))
                        for i in range(2):
                            defausse.append(joueur['cartes'].pop(0))
                        break
                    else:
                        if main[0]!=0 and len(voisin)!=0:
                            joker(joueur,jeu,voisin,defausse,CJ)
                        elif (r[0]!=0 and len(VD)!=0) or (r[1]!=0 and len(VO)!=0):
                            attaque(joueur,jeu,VO,VD,r,defausse,CJ)
                        elif joueur['pos']!="C3":
                            bouge(joueur,voisin,defausse,CJ)
                        if NbCJ==1:
                            joueur['cartes']=sorted(joueur['cartes'], key=lambda t: valeur(t))
                            defausse.append(joueur['cartes'].pop(0))
                            
                elif i==1:
                    if (len(voisin)==0 or main[0]==0) and (len(VO)==0 or r[1]==0) and (len(VD)==0 or r[0]==0) and main[2]==0:
                        joueur['cartes']=sorted(joueur['cartes'], key=lambda t: valeur(t))
                        defausse.append(joueur['cartes'].pop(0))
                        break
                    else:
                        if main[0]!=0 and len(voisin)!=0:
                            joker(joueur,jeu,voisin,defausse,CJ)
                        elif (r[0]!=0 and len(VD)!=0) or (r[1]!=0 and len(VO)!=0):
                            attaque(joueur,jeu,VO,VD,r,defausse,CJ)
                        elif joueur['pos']!="C3":
                            bouge(joueur,voisin,defausse,CJ)
                else:
                    if (len(voisin)==0 or main[0]==0) and (len(VO)==0 or r[1]==0) and (len(VD)==0 or r[0]==0) and main[2]==0:
                        break
                    else:
                        if main[0]!=0 and len(voisin)!=0:
                            joker(joueur,jeu,voisin,defausse,CJ)
                        elif (r[0]!=0 and len(VD)!=0) or (r[1]!=0 and len(VO)!=0):
                            attaque(joueur,jeu,VO,VD,r,defausse,CJ)
                        elif joueur['pos']!="C3":
                            bouge(joueur,voisin,defausse,CJ)
        if est_vide(CJ):
            joueur['pv']=joueur['pv']-1
        if len(joueur['cartes'])<=3:
            if len(pioche)>=2:
                Ncartes=pioche_cartes(2,pioche)
                joueur['cartes'].extend(copy.deepcopy(Ncartes))
            else:
                defausse2pioche(defausse,pioche)
                Ncartes=pioche_cartes(2,pioche)
                joueur['cartes'].extend(copy.deepcopy(Ncartes))
        elif len(joueur['cartes'])==4:
            Ncartes=pioche_cartes(1,pioche)
            joueur['cartes'].extend(copy.deepcopy(Ncartes))
        if est_vide(pioche)==True:
            defausse2pioche(defausse,pioche)
        for j in jeu:
            if KO(j):
                defausse.extend(j['cartes'])
                j['pos']="00"
        time.sleep(3)
        print("Plateau du jeu :\n")
        time.sleep(3)
        affiche_plateau(jeu)
        time.sleep(3)
        print("\nVoici les cartes qui ont été jouées pendant le tour dans l'ordre :\n".format(joueur['pion']))
        time.sleep(2)
        affiche_cartes(CJ)
        time.sleep(3)
        print("\nLa main et les points d'endurance de chaque joueur sont les suivants:\n")
        for j in jeu:
            time.sleep(4)
            print("{} :\n".format(j['pion']))
            time.sleep(1)
            print("Main : ")
            affiche_cartes(j['cartes'])
            time.sleep(1)
            print("PV : {}".format(j['pv']))
            print("\n")
    return None

def joker(joueur,jeu,voisin,defausse,CJ):
    CJ.append(carte_utilisée("J",joueur,defausse))
    vs=randint(0,len(voisin)-1)
    for j in jeu:
        if j!=joueur and voisin[vs]==j and j['pv']!="00":
            j['cartes']=sorted(j['cartes'], key= lambda t: valeur(t), reverse=True)
            CV=j['cartes'].pop(0)
            joueur['cartes'].append(CV)
            time.sleep(2)
            print("\nLe joueur {} a volé la carte {} au joueur {}.\n".format(joueur['pion'],CV,j['pion']))
            time.sleep(2)
            return None
            
def attaque(joueur,jeu,VO,VD,c,defausse,CJ):
    VC=[]
    for j in jeu:
        if j!=joueur and j['pv']!='00':
            if j['pos'] in voisins("ortho","C3") or j['pos'] in voisins("diag","C3"):
                VC.append(j['pos'])
    if c[0]!=0 and len(VD)!=0 and (c[1]==0 or len(VO)==0):
        JA=randint(0,len(VD)-1)
        for j in jeu:
            if j==VD[JA] and j['pv']!="00":
                if j['pos']=="C3":
                    if joueur['pos']=="B2" and "D4" not in VC:
                        j['pos']="D4"
                        CU=carte_utilisée("C", joueur, defausse)
                        CJ.append(CU)
                    elif joueur['pos']=="D2" and "B4" not in VC:
                        j['pos']="B4"
                        CU=carte_utilisée("C", joueur, defausse)
                        CJ.append(CU)
                    elif joueur['pos']=="B4" and "D2" not in VC:
                        j['pos']="D2"
                        CU=carte_utilisée("C", joueur, defausse)
                        CJ.append(CU)
                    elif "B2" not in VC:
                        j['pos']="B2"
                        CU=carte_utilisée("C", joueur, defausse)
                        CJ.append(CU)
                else:
                    CU=carte_utilisée("C", joueur, defausse)
                    CJ.append(CU)
                    if joueur['pos']=="C3":
                        parade(joueur,j,defausse,CU,"diag",2,CJ)
                    else:
                        parade(joueur,j,defausse,CU,"diag",1,CJ)
    elif c[1]!=0 and len(VO)!=0 and (c[0]==0 or len(VD)==0):
        JA=randint(0,len(VO)-1)
        for j in jeu:
            if j==VO[JA] and j['pv']!="00":
                if j['pos']=='C3':
                    if joueur['pos']=="C2" and "C4" not in VC:
                        j['pos']="C4"
                        CU=carte_utilisée("K", joueur, defausse)
                        CJ.append(CU)
                    elif joueur['pos']=="C4" and "C2" not in VC:
                        j['pos']="C2"
                        CU=carte_utilisée("K", joueur, defausse)
                        CJ.append(CU)
                    elif joueur['pos']=="D3" and "B3" not in VC:
                        j['pos']="B3"
                        CU=carte_utilisée("K", joueur, defausse)
                        CJ.append(CU)
                    elif "D3" not in VC:
                        j['pos']="D3"
                        CU=carte_utilisée("K", joueur, defausse)
                        CJ.append(CU)
                else:
                    CU=carte_utilisée("K", joueur, defausse)
                    CJ.append(CU)
                    if joueur['pos']=="C3":
                        parade(joueur,j,defausse,CU,"ortho",2,CJ)
                    else:
                        parade(joueur,j,defausse,CU,"ortho",1,CJ)
    else:
        JA1=randint(0,1)
        if JA1==0:
            JA=randint(0,len(VD)-1)
            for j in jeu and j['pv']!="00":
                if j==VD[JA]:
                    if j['pos']=="C3":
                        if joueur['pos']=="B2" and "D4" not in VC:
                            j['pos']="D4"
                            CU=carte_utilisée("C", joueur, defausse)
                            CJ.append(CU)
                        elif joueur['pos']=="D2" and "B4" not in VC:
                            j['pos']="B4"
                            CU=carte_utilisée("C", joueur, defausse)
                            CJ.append(CU)
                        elif joueur['pos']=="B4" and "D2" not in VC:
                            j['pos']="D2"
                            CU=carte_utilisée("C", joueur, defausse)
                            CJ.append(CU)
                        elif "B2" not in VC:
                            j['pos']="B2"
                            CU=carte_utilisée("C", joueur, defausse)
                            CJ.append(CU)
                    else:
                        CU=carte_utilisée("C", joueur, defausse)
                        CJ.append(CU)
                        if joueur['pos']=="C3":
                            parade(joueur,j,defausse,CU,"diag",2,CJ)
                        else:
                            parade(joueur,j,defausse,CU,"diag",1,CJ)
        else:
            JA=randint(0,len(VO)-1)
            for j in jeu:
                if j==VO[JA] and j['pv']!="00":
                    if j['pos']=='C3':
                        if joueur['pos']=="C2" and "C4" not in VC:
                            j['pos']="C4"
                            CU=carte_utilisée("K", joueur, defausse)
                            CJ.append(CU)
                        elif joueur['pos']=="C4" and "C2" not in VC:
                            j['pos']="C2"
                            CU=carte_utilisée("K", joueur, defausse)
                            CJ.append(CU)
                        elif joueur['pos']=="D3" and "B3" not in VC:
                            j['pos']="B3"
                            CU=carte_utilisée("K", joueur, defausse)
                            CJ.append(CU)
                        elif "D3" not in VC:
                            j['pos']="D3"
                            CU=carte_utilisée("K", joueur, defausse)
                            CJ.append(CU)
                    else:
                        CU=carte_utilisée("K", joueur, defausse)
                        CJ.append(CU)
                        if joueur['pos']=="C3":
                            parade(joueur,j,defausse,CU,"ortho",2,CJ)
                        else:
                            parade(joueur,j,defausse,CU,"ortho",1,CJ)
    return None
    
def cartes_attaque(joueur):
    r=[0,0]
    for carte in joueur['cartes']:
        if carte[1]=='C':
            r[0]=r[0]+1
        elif carte[1]=='K':
            r[1]=r[1]+1
    return r

def cartes_mvt(joueur):
    m=[0,0]
    for carte in joueur['cartes']:
        if carte[1]=='P':
            m[0]=m[0]+1
        elif carte[1]=='T':
            m[1]=m[1]+1
    return m

def carte_utilisée(style,joueur,defausse):
    random.shuffle(joueur['cartes'])
    for i in range(0,len(joueur['cartes'])):
        if joueur['cartes'][i][1]==style or joueur['cartes'][i][0]==style:
            carte_utilisée=joueur['cartes'][i]
            defausse.append(joueur['cartes'].pop(i))
            return carte_utilisée

def bouge(joueur,voisin,defausse,CJ):
    Npos=priorité_mvt(joueur,voisin,defausse,CJ)
    if Npos!=False:
        joueur['pos']=Npos
    return None
    
def priorité_mvt(joueur,voisin,defausse,CJ):
    c=cartes_mvt(joueur)
    positions=[["A1","B1","C1","D1","E1"],["A2","B2","C2","D2","E2"],["A3","B3","C3","D3","E3"],["A4","B4","C4","D4","E4"],["A5","B5","C5","D5","E5"]]
    VO=[]
    VD=[]
    for v in range(0,len(voisin)):
        if voisin[v]['pos'] in voisins("ortho",joueur['pos']):
            VO.append(voisin[v]['pos'])
        else:
            VD.append(voisin[v]['pos'])
    for i in range(0,len(positions)):
        for j in range(0,len(positions)):
            if positions[i][j]==joueur['pos']:
                l=i
                k=j
    if l==2 or k==2:
        if l<2:
            if positions[l+1][k] in VO or c[1]==0:
                a=randrange(-1,2,2)
                if positions[l+1][k+a] in VD or c[0]==0:
                    if positions[l+1][k-a] in VD or c[0]==0:
                        if positions[l][k+a] in VO or c[1]==0:
                            if positions[l][k-a] in VO or c[1]==0:
                                return False
                            else:
                                CJ.append(carte_utilisée("T", joueur, defausse))
                                return positions[l][k-a]
                        else:
                            CJ.append(carte_utilisée("P",joueur,defausse))
                            return positions[l][k+a]
                    else:
                        CJ.append(carte_utilisée("P",joueur,defausse))
                        return positions[l+1][k-a]
                else:
                    CJ.append(carte_utilisée("P",joueur,defausse))
                    return positions[l+1][k+a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l+1][k]
        elif l>2:
            if positions[l-1][k] in VO or c[1]==0:
                a=randrange(-1,2,2)
                if positions[l-1][k+a] in VD or c[0]==0:
                    if positions[l-1][k-a] in VD or c[0]==0:
                        if positions[l][k+a] in VO or c[1]==0:
                            if positions[l][k-a] in VO or c[1]==0:
                                return False
                            else:
                                CJ.append(carte_utilisée("T",joueur,defausse))
                                return positions[l][k-a]
                        else:
                            CJ.append(carte_utilisée("T",joueur,defausse))
                            return positions[l][k+a]
                    else:
                        CJ.append(carte_utilisée("P",joueur,defausse))
                        return positions[l-1][k-a]
                else:
                    CJ.append(carte_utilisée("P",joueur,defausse))
                    return positions[l-1][k+a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l-1][k]
        elif k<2:
            if positions[l][k+1] in VO or c[1]==0:
                a=randrange(-1,2,2)
                if positions[l+a][k+1] in VD or c[0]==0:
                    if positions[l-a][k+1] in VD or c[0]==0:
                        if positions[l+a][k] in VO or c[1]==0:
                            if positions[l-a][k] in VO or c[1]==0:
                                return False
                            else:
                                CJ.append(carte_utilisée("T",joueur,defausse))
                                return positions[l-a][k]
                        else:
                            CJ.append(carte_utilisée("T",joueur,defausse))
                            return positions[l+a][k]
                    else:
                        CJ.append(carte_utilisée("P",joueur,defausse))
                        return positions[l-a][k+1]
                else:
                    CJ.append(carte_utilisée("P",joueur,defausse))
                    return positions[l+a][k+1]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l][k+1]
        else:
            if positions[l][k-1] in VO or c[1]==0:
                a=randrange(-1,2,2)
                if positions[l+a][k-1] in VD or c[0]==0:
                    if positions[l-a][k-1] in VD or c[0]==0:
                        if positions[l+a][k] in VO or c[1]==0:
                            if positions[l-a][k] in VO or c[1]==0:
                                return False
                            else:
                                CJ.append(carte_utilisée("T",joueur,defausse))
                                return positions[l-a][k]
                        else:
                            CJ.append(carte_utilisée("T",joueur,defausse))
                            return positions[l+a][k]
                    else:
                        CJ.append(carte_utilisée("P",joueur,defausse))
                        return positions[l-a][k-1]
                else:
                    CJ.append(carte_utilisée("P",joueur,defausse))
                    return positions[l+a][k-1]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l][k-1]
    elif l<2 and k<2:
        if positions[l+1][k+1] in VD or c[0]==0:
            a=randint(0,1)
            if positions[l+a][k+(1-a)] in VO or c[1]==0:
                if positions[l+(1-a)][k+a] in VO or c[1]==0:
                    return False
                else:
                    CJ.append(carte_utilisée("T",joueur,defausse))
                    return positions[l+(1-a)][k+a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l+a][k+(1-a)]
        else:
            CJ.append(carte_utilisée("P",joueur,defausse))
            return positions[l+1][k+1]
    elif l<2 and k>2:
        if positions[l+1][k-1] in VD or c[0]==0:
            a=randint(0,1)
            if positions[l+a][k-(1-a)] in VO or c[1]==0:
                if positions[l+(1-a)][k-a] in VO or c[1]==0:
                    return False
                else:
                    CJ.append(carte_utilisée("T",joueur,defausse))
                    return positions[l+(1-a)][k-a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l+a][k-(1-a)]
        else:
            CJ.append(carte_utilisée("P",joueur,defausse))
            return positions[l+1][k-1]
    elif l>2 and k>2:
        if positions[l-1][k-1] in VD or c[0]==0:
            a=randint(0,1)
            if positions[l-a][k-(1-a)] in VO or c[1]==0:
                if positions[l-(1-a)][k-a] in VO or c[1]==0:
                    return False
                else:
                    CJ.append(carte_utilisée("T",joueur,defausse))
                    return positions[l-(1-a)][k-a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l-a][k-(1-a)]
        else:
            CJ.append(carte_utilisée("P",joueur,defausse))
            return positions[l-1][k-1]
    else:
        if positions[l-1][k+1] in VD or c[0]==0:
            a=randint(0,1)
            if positions[l-a][k+(1-a)] in VO or c[1]==0:
                if positions[l-(1-a)][k+a] in VO or c[1]==0:
                    return False
                else:
                    CJ.append(carte_utilisée("T",joueur,defausse))
                    return positions[l-(1-a)][k+a]
            else:
                CJ.append(carte_utilisée("T",joueur,defausse))
                return positions[l-a][k+(1-a)]
        else:
            CJ.append(carte_utilisée("P",joueur,defausse))
            return positions[l-1][k+1]


def parade(j1,j2,defausse,CU,direction,pv,CJ):
    j2['cartes']=sorted(j2['cartes'], key=lambda t: valeur(t))
    if direction=="ortho":
        for i in range(len(j2['cartes'])):
            if j2['cartes'][i][1]=="K" and valeur(j2['cartes'][i])>valeur(CU):
                CU2=j2['cartes'].pop(i)
                defausse.append(CU2)
                CJ.append(CU2)
                time.sleep(2)
                print("\nLe joueur {} a essayé de mettre un coup au joueur {} mais joueur {} a paré le coup en utilisant la carte {}.\n".format(j1['pion'],j2['pion'],j2['pion'],CU2))
                time.sleep(2)
                return None
        j2['pv']=j2['pv']-pv
        return None
    else:
        for i in range(len(j2['cartes'])):
            if j2['cartes'][i][1]=="C" and valeur(j2['cartes'][i])>valeur(CU):
                CU2=j2['cartes'].pop(i)
                defausse.append(CU2)
                CJ.append(CU2)
                time.sleep(2)
                print("\nLe joueur {} a essayé de mettre un coup au joueur {} mais joueur {} a paré le coup en utilisant la carte {}.\n".format(j1['pion'],j2['pion'],j2['pion'],CU2))
                time.sleep(2)
                return None
        j2['pv']=j2['pv']-pv
        return None
    
    


if __name__=="__main__":    
    print("Test valeur(carte)")
    print("test1: 9T, valeur attendue 9")
    t_v1='9T'
    if valeur(t_v1)==9:
        print("ok")
    else:
        print("probl: valeur attendue 9")
    print("test2: 0T,valeur attendue 10")
    t_v2='0C'
    if valeur(t_v2)==10:
        print("ok")
    else:
        print("probl: valeur attendue 10")
    print("test3: RC, valeur attendue 13")
    t_v3='RC'
    if valeur(t_v3)==13:
        print("ok\n")
    else:
        print("probl: valeur attendue 13\n")
    
    print("Test KO(joueur): jouer a un pv=1, réponse attendue False")
    t_kojoueur={'pion':'X', 'pos':'A1', 'pv':1, 'cartes':['8C', 'RC', 'VK', '1T', 'J2']}
    if KO(t_kojoueur)==False:
        print("ok\n")
    else:
        print("probl: nombre de vies mal compté, ici on doit avoir 'False' vu que pv!=0\n")
    
    print("Test nb_KO(L_joueurs): joueur1 a un pv=1, joueur2 pv=0 et jouueur 3 pv=0, donc valeur attendue 2")
    t_nbko=[{'pion':'X', 'pos':'A1', 'pv':1, 'cartes':['VP', 'RT', 'DK', '9P', '10T']},{'pion':'Y', 'pos': 'E5', 'pv':0, 'cartes':['8C','RC','VK','1T','J2' ]},{'pion':'Z', 'pos':'A5', 'pv':0, 'cartes':['10C','DT','J1','DC','RT']}]
    if nb_KO(t_nbko)==2:
        print('ok\n')
    else:
        print('probl: nombre de vies mal comptées\n')
    
    print("Test voisins(direction,case)")
    d1="ortho"
    d2="diag"
    c1="A3"
    c2='C4'
    d1c1=['A2','A4','B3']
    d1c2=['C3','C5','B4','D4']
    d2c1=['B4','B2']
    d2c2=['B3','B5','D3','D5']
    print("-test1:\ndirection: orthogonale, case: A3, voisins attendus: A2, A4 et B3")
    for i in d1c1:
        if i in voisins(d1,c1):
            print('ok')
        else:
            print('probl')
    if len(d1c1)==len(voisins(d1,c1)):
        print("OK, les voisins attendus sont bien retournés et la longueur de la liste est correcte")
    else:
        print("probl: toutes les cartes apparaissent dans la liste retournée mais la longueur de a liste ne correspond pas au nombre de voisins")
    print("-test2:\ndirection: orthogonale, case: C4, voisins attendus: C3, C5, B4 et D4")
    for i in d1c2:
        if i in voisins(d1,c2):
            print('ok')
        else:
            print('probl')
    if len(d1c2)==len(voisins(d1,c2)):
        print("OK, les voisins attendus sont bien retournés et la longueur de la liste est correcte")
    else:
        print("probl: toutes les cartes apparaissent dans la liste retournée mais la longueur de a liste ne correspond pas au nombre de voisins")        
    print("-test3:\ndirection: diagonale, case: A3, voisins attendus: B4 et B2")
    for i in d2c1:
        if i in voisins(d2,c1):
            print('ok')
        else:
            print('probl')
    if len(d2c1)==len(voisins(d2,c1)):
            print("OK, les voisins attendus sont bien retournés et la longueur de la liste est correcte")
    else:
        print("problème: toutes les cartes apparaissent dans la liste retournée mais la longueur de a liste ne correspond pas au nombre de voisins")
    print("-test4:\ndirection: diagonale, case: C4, voisins attendus: B3, B5, D3 et D5")
    for i in d2c2:
        if i in voisins(d2,c2):
            print('ok')
        else:
            print('probl')
    if len(d2c2)==len(voisins(d2,c2)):
        print("OK, les voisins attendus sont bien retournés et la longueur de la liste est correcte")
    else:
        print("probl: toutes les cartes apparaissent dans la liste retournée mais la longueur de a liste ne correspond pas au nombre de voisins")
    print('')
    
    print("Test est_voisin(j1,j2,direction)")
    j1={'pion':'X', 'pos':'D3', 'pv':5, 'cartes':['VP', 'RT', 'DK', '9P', '10T']}
    j2={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}
    print("-test1: direction=diagonale joueur1 est dans la case D3 et le joueur2 est dans la case E4, réponse attendue True")
    if est_voisin(j1,j2,"diag")==True:
        print('ok')
    else:
        print('probl')
    print("-test1: direction=orth joueur1 est dans la case D3 et le joueur2 est dans la case E4, réponse attendue False")
    if est_voisin(j1,j2,"ortho")==False:
        print('ok')
    else:
        print('probl')
    print('')
    
    print("Test init_pioche(): on a toutes les cartes de la pioche: 1C,7C,8C,9C,0C,RC,VC,DC,1K,7K,8K,9K,0K,VK,DK,RK,1T,7T,8T,9T,0T,VT,DT,RT,1P,7P,8P,9P,0P,VP,DP,RP,J1,J2\nrésultat attendu: cartes melangées")
    L=['1C','7C','8C','9C','0C','RC','VC','DC','1K','7K','8K','9K','0K','VK','DK','RK','1T','7T','8T','9T','0T','VT','DT','RT','1P','7P','8P','9P','0P','VP','DP','RP','J1','J2']
    if init_pioche()==L:
        print("probl: la liste n'as pas été modifiée\n")
    else:
        print(init_pioche())
        print("ok\n")
    
    print('Test init_defausse(): résultat attendu: liste vide')
    if init_defausse()==[]:
        print("ok\n")
    else:
        print("probl\n")
    
    print("Test de est_vide(paquet)")
    print("Test1: avec []: réponse attendue True")
    if est_vide([])==True:
        print('ok')
    else:
        print('probl')
    print("Test2: avec ['VC', 'VP', 'RC', 'RT', '9K', '1C', 'J1']: réponse attendue False")
    if est_vide(['VC', 'VP', 'RC', 'RT', '9K', '1C', 'J1'])==False:
        print('ok\n')
    else:
        print('probl\n')
    
    print("Test pioche_cartes(n,L_cartes): avec n=3 et L=['VC', 'VP', 'RC', 'RT', '9K', '1C', 'J1], résultat attendu: ['9K', '1C', 'J1'] et L=['VC', 'VP', 'RC', 'RT'] modifiée!!" )
    L=['VC', 'VP', 'RC', 'RT', '9K', '1C', 'J1']
    if pioche_cartes(3,L)==['9K', '1C', 'J1'] and L==['VC', 'VP', 'RC', 'RT']:
        print('ok\n')
    else:
        print('probl: élements pas supprimés de la liste initiale ou liste L pas modifiée\n')
    
    print("Test init_joueurs(n,pioche): on a n=2 et pioche=['1C','7C','8C','9C','0C','RC','VC','DC','1K','7K','8K','9K','0K','VK','DK','RK','1T','7T','8T','9T','0T','VT','DT','RT','1P','7P','8P','9P','0P','VP','DP','RP','J1','J2']\nRésultat attendu: deux joueurs chacun représenté par un pion placé dans un coin, 10 pv et 5 cartes de la pioche")
    pioche=['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
    if init_joueurs(2,pioche)==[{'pion': 'X','pos': 'A1','pv': '10','cartes': ['0','0','0','0','0']},{'pion': 'Y','pos': 'E1','pv': '10','cartes': ['0','0','0','0','0']},{'pion': 'Z','pos': 'E5','pv': '10','cartes': ['0','0','0','0','0']}]:
        print('ok')
    else: 
        print("problème: position, nombre de pv, cartes mal choisies ou répétées")
    print("On test aussi que chaque joueur ait des cartes différentes et que la pioche ne contiennent plus les cartes prises par les joueurs\nCe test doit être effectué directement par l'utilisateur (pas moyen de prévoir les cartes tirées pas chque joueur): vérifier que les mains de chaque joueur soient ditinctes et que pioche ne les ait pas")


    #fontcions de plus
    
    print("Test de start(pioche,jeu): pour savoir qui commence les joueurs tirent une carte de la pioche, si les cartes sont de même valeurs ils recommencent")
    print("On test avec la pioche qui contient toutes les cartes du jeu et deux joueurs:")
    pioche=['1C','7C','8C','9C','0C','RC','VC','DC','1K','7K','8K','9K','0K','VK','DK','RK','1T','7T','8T','9T','0T','VT','DT','RT','1P','7P','8P','9P','0P','VP','DP','RP','J1','J2']
    jeu=init_joueurs(2,pioche)
    print(start(pioche,jeu))
    print("A vérifier directement par l'utilisateur\n")
    
    print("Test cartes_couleur(main): on veut savoir combien de cartes de chaque couleur (joker,attaque,mouvement) un joueur a en main")
    print("On test avec la main : 8C, RT, J1, J2, 9K. Le résultat attendu est la liste [2,2,1] ")
    r=[2,2,1]
    if cartes_couleur(['8C','RT','J1','J2','9K'])==r:
        print('ok\n')
    else:
        print("probl: mauvais comptage ou éléments de la liste dans un ordre incorrecte\n")
    
    print('Test cartes_attaque(joueur): retourne le nombre de coeurs et ce carreaux que le joueur a' )
    print("On réalise le test avec un joueur  joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}, le résultat attendu est [2,1]")
    joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}
    if cartes_attaque(joueur)==[2,1]:
        print('ok\n')
    else:
        print('probl\n')
    
    print("Test cartes_mvt(joueur): retourne le nombre de piques et de trèfles que le joueur a")
    print("On réalise le test avec un joueur  joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}, le résultat attendu est [0,1]")
    joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}
    if cartes_mvt(joueur)==[0,1]:
        print('ok\n')
    else:
        print('probl\n')
    
    print("Test carte_utilisée(style,joueur,defausse): retourne la carte utilisée par le joueur selon le type de carte qu'on veut")
    print("On réalise le test avec style='K', joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]} et  defausse=['1C','7C','9C','VC','DC','7K','8K','9K','DK','RK','8T','9T','DT'] ")
    joueur={'pion':'Y', 'pos': 'E4', 'pv':3, 'cartes':['8C','RC','VK','1T','J2' ]}
    defausse=['1C','7C','9C','VC','DC','7K','8K','9K','DK','RK','8T','9T','DT']
    if carte_utilisée('K',joueur,defausse)=='VK':
        print("ok\n")
    else:
        print("probl\n")
    
    print("Test priorité_mvt(joueur,voisin,defausse,CJ): retourne la position qu'un joueur va occuper qprès son déplacement ")
    print("On réalise un test avec deux joueurs voisins j1, j2, c'est le tour de j1 et les deux joueurs sont à une case en diagonale du centre C3, le déplacement prioritaire pour les deux est vers le centre")
    print("Le j1 a cette main: ['8C','RC','VK','0T','J2' ] ")
    j1={'pion':'X', 'pos':'C4', 'pv':'10','cartes':['8C','RC','VK','0T','J2' ] }
    j2={'pion':'Y', 'pos':'D4', 'pv':'10','cartes':['VT', '0P', 'J1', '1T', '0C'] }
    defausse=['1C','7C','9C','VC','DC','7K','8K','9K','DK','RK','8T','9T','DT']
    if priorité_mvt(j1,[j2],defausse,['8C','0T'])=='C3':
        print('ok\n')
    else: 
        print('probl\n')   