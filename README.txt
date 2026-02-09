Mini assembleur et CPU virtuelle en Python:

Présentation du projet:

Mon projet consiste en un CPU virtuel créé en Python, accompagné de son langage assembleur qui est traduit en langage machine.
Le projet est composé de 3 fichiers : le premier contient le code du CPU, le deuxième contient l’assembleur et le dernier le main, qui permet de créer une interface graphique avec Tkinter. Celle-ci contient une zone de texte pour écrire le code et un terminal pour voir toutes les étapes réalisées par le CPU.


Objectifs du projet:

Ce travail a été mené dans un objectif de compréhension du fonctionnement interne d’un ordinateur et des principes de base de l’architecture des processeurs.

Jeu d’instructions:

Le langage assembleur supporte notamment les instructions suivantes :

LOAD : chargement d’une valeur dans un registre
ADD, SUB, MULT, DIV : opérations arithmétiques
AREG, MREG : opérations entre registres
CMP : comparaison entre registres
JUMP, JZ, JEQ, JLT, JGT : instructions de saut
OUT / STACK : stockage de valeurs
EXIT : arrêt du programme

Exemple de programme assembleur:

LOAD 5 0
LOAD 3 1
AREG
OUT
EXIT

