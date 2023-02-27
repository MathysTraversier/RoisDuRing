# -*- coding: utf-8 -*-
from utils import *
import time

pioche=init_pioche()
defausse=init_defausse()
n=int(input("Nombre de joueurs ? "))
print("\n")
print("Mise en place des joueurs et distribution des cartes... \n")
time.sleep(3)
jeu=init_joueurs(n, pioche)
for i in range(0,n):
    print("Le joueur {} jouera avec le pion {}".format(i+1,jeu[i]['pion']))
    time.sleep(1)
time.sleep(2)
print("\n")
print("Qui commence ?")
print("\n")
time.sleep(3)
start(pioche,jeu)
time.sleep(5)
print("\nAffichage du plateau...\n")
affiche_plateau(jeu)
time.sleep(3)
print("\n")
while nb_KO(jeu)!=(len(jeu)-1):
    cartes_tour(jeu,defausse,pioche)
print("C'est la fin de la partie ; nous avons un gagnant")
time.sleep(2)
print("Roulement de tambours........\n")
time.sleep(3)
for j in jeu:
    if j['pos']!="00":
        print("Félicitations à {} qui remporte cette partie de manière bluffante ! Bravo !".format(j['pion']))
        break
        
