Assembleur et CPU Virtuel en Python

PRESENTATION:

Ce projet simule le fonctionnement d'un processeur réel. Le code assembleur
écrit par l'utilisateur est traduit en langage machine, chargé en RAM, puis exécuté
instruction par instruction par le CPU virtuel. Une interface graphique Tkinter permet
d'écrire, compiler et observer l'exécution du code.

Le projet est né après des recherches sur l'architecture d'un PC, j'ai voulu voir si j'étais capable
d'en créer un moi-même.

LIEN UTILE :

Le projet nécessite au moins la version 3.11 de Python en raison de l'utilisation des match/case. 
Pour remédier à toute erreur liée à cela, voici ci-dessous un lien pour télécharger une version récente 
de Python ou d'EduPython :

Python : https://www.python.org/downloads/
EduPython : https://edupython.tuxfamily.org/

ARCHITECTURE DU PROJET:

cpu_assembleur/
    assembler.py = Traduction du code assembleur en "langage machine"
    cpu.py       = Exécution des instructions, gestion des registres et de la RAM
    gpu.py       = GPU virtuelle avec VRAM et kernels simuler
    main.py      = Interface graphique PyQt6

Registres disponibles :
    A, B, C    : registres généraux
    PC         : compteur de programme(permet de me situer dans la ram ainsi que de la parcourire)
    SP         : pointeur de pile(limite l'emplacement destiner a stocker des info de celui qui permet de stocker le code compiler)
    FLAGS      : résultat des comparaisons (égal / inférieur / supérieur)

Mémoire :
    RAM  : 1024 octets
    VRAM : 256 octets (écran 16x16 pixels)
    Pile : adresses 900 à 1024

JEU D'INSTRUCTIONS

Chargement :
    LOAD valeur registre            Charge une valeur dans un registre (0=A, 1=B, 2=C)

Calcule :
    ADD  dest src1 src2     destination = source1 + source2
    SUB  dest src1 src2     destination = source1 - source2
    MULT dest src1 src2     destination = source1 * source2
    DIV  dest src1 src2     destination = source1 / source2

Comparaison et sauts :
    CMP  reg1 reg2          Compare deux registres, met à jour FLAGS
    JUMP label              Saut inconditionnel
    JZ   label              Saut si A==0
    JEQ  label              Saut si FLAGS == égal
    JLT  label              Saut si FLAGS == inférieur
    JGT  label              Saut si FLAGS == supérieur

Pile :
    STK registre                 Empile la valeur d'un registre
    POP registre                 Dépile une valeur dans un registre
    CALL addr(label utilisable)  Empile l'adresse de retour actuelle et saute à l'adresse de la fonction
    RET                          Dépile l'adresse de retour et replace le registre PC à cette position pour quitter la fonction.

GPU :
    GPUOP   op para         Définit l'opération GPU et son paramètre
    GPULIM  limit offB offC Nombre d'itérations et offsets
    GPUSTART addr           Adresse de départ dans la VRAM
    GPUON                   Lance le dispatcher GPU

Mémoire :
    STORE  reg addr         Enregistre la valeur d'un registre à une adresse mémoire spécifique.
    STOREIND  src dest      Enregistre la valeur d'un registre à l'adresse contenue dans un autre registre.
    PEEK      src dest      Lit la valeur située à une adresse mémoire (contenue dans un registre) et la stocke dans un registre de destination.

Divers :
    WAIT ms                 Pause en millisecondes
    EXIT                    Arrêt du programme
    MOV src dest            Copie le contenu du registre src vers le registre dest


EXEMPLES DE PROGRAMMES

Suite de Fibonacci :
LOAD 600 0
LOAD 10 1
LOAD 1 2

STOREIND 2 0
ADD 0 0 2
STOREIND 2 0
ADD 0 0 2

main_loop:
    STK 1
    CALL calculer_suivant
    STOREIND 2 0
    LOAD 1 2
    ADD 0 0 2
    POP 1
    LOAD 1 2
    SUB 1 1 2
    CMP 1 2
    JGT main_loop
    EXIT

calculer_suivant:
    STK 0
    LOAD 1 2
    SUB 0 0 2
    PEEK 0 1
    SUB 0 0 2
    PEEK 0 2
    ADD 2 2 1
    POP 0
    RET

Résultat : 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...

Animation coeur (GPU) :
Dessine un coeur qui bat sur l'écran 16x16 grâce
aux instructions GPU et à WAIT.

GPUOP 3 0
GPULIM 256 0 0
GPUSTART 0
GPUON
GPUOP 9 0
GPULIM 1 0 0
GPUOP 3 0
GPULIM 256 0 0
GPUSTART 0
GPUON
GPUOP 9 0
GPULIM 1 0 0
GPUSTART 68
GPUON
GPUSTART 69
GPUON
GPUSTART 70
GPUON
GPUSTART 74
GPUON
GPUSTART 75
GPUON
GPUSTART 76
GPUON
GPUSTART 83
GPUON
GPUSTART 84
GPUON
GPUSTART 85
GPUON
GPUSTART 86
GPUON
GPUSTART 87
GPUON
GPUSTART 88
GPUON
GPUSTART 89
GPUON
GPUSTART 90
GPUON
GPUSTART 91
GPUON
GPUSTART 92
GPUON
GPUSTART 93
GPUON
GPUSTART 99
GPUON
GPUSTART 100
GPUON
GPUSTART 101
GPUON
GPUSTART 102
GPUON
GPUSTART 103
GPUON
GPUSTART 104
GPUON
GPUSTART 105
GPUON
GPUSTART 106
GPUON
GPUSTART 107
GPUON
GPUSTART 108
GPUON
GPUSTART 109
GPUON
GPUSTART 116
GPUON
GPUSTART 117
GPUON
GPUSTART 118
GPUON
GPUSTART 119
GPUON
GPUSTART 120
GPUON
GPUSTART 121
GPUON
GPUSTART 122
GPUON
GPUSTART 123
GPUON
GPUSTART 124
GPUON
GPUSTART 133
GPUON
GPUSTART 134
GPUON
GPUSTART 135
GPUON
GPUSTART 136
GPUON
GPUSTART 137
GPUON
GPUSTART 138
GPUON
GPUSTART 139
GPUON
GPUSTART 150
GPUON
GPUSTART 151
GPUON
GPUSTART 152
GPUON
GPUSTART 153
GPUON
GPUSTART 154
GPUON
GPUSTART 167
GPUON
GPUSTART 168
GPUON
GPUSTART 169
GPUON
GPUSTART 184
GPUON
WAIT 400
GPUOP 3 0
GPULIM 256 0 0
GPUSTART 0
GPUON
WAIT 400
EXIT


INTERFACE GRAPHIQUE

    - Zone d'édition pour écrire le code assembleur
    - Bouton COMPILER pour lancer l'exécution
    - Bouton EFFACER ECRAN pour vider le canva
    - Terminal affichant chaque instruction exécutée pas à pas
    - Ecran 16x16 pour visualiser la VRAM en temps réel


LANCEMENT

    -python main.py(assurez vous que PyQt6 est installé pip install PyQt6)




