from PyQt6.QtGui import QPainter,QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
vram = [0]*1024
fenetre_ref=None
ecran_ref=None

def kernel(id):
    from cpu import registres
    parametre=registres["GPU_PARA"]
    operation=registres["GPU_OP"]
    valeurA=vram[id]
    valeurB=vram[id+registres["GPU_OFFSET_B"]]
    valeurC=vram[id+registres["GPU_OFFSET_C"]]
    match(operation):
        case(1):
            vram[id]=valeurA+parametre
        case(2):
            vram[id]=valeurA-parametre
        case(3):
            vram[id]=valeurA*parametre
        case(4):
            if parametre!=0:
                vram[id]=valeurA//parametre
        case(5):
            vram[id+registres["GPU_OFFSET_C"]]=valeurA+valeurB
        case(6):
            vram[id+registres["GPU_OFFSET_C"]]=valeurA-valeurB
        case(7):
            vram[id+registres["GPU_OFFSET_C"]]=valeurA*valeurB
        case(8):
            if valeurB!=0:
                vram[id+registres["GPU_OFFSET_C"]]=valeurA//valeurB
        case(9):
            vram[id]=1

def dessine_ecran():
    if ecran_ref.pixmap() is None: 
        return
    pixmap=ecran_ref.pixmap()
    painter=QPainter(pixmap)
    taille=20
    for i in range(len(vram)):
        x=i%16
        y=i//16
        x1=x*taille
        y1=y*taille
        couleur=Qt.GlobalColor.white if vram[i] != 0 else Qt.GlobalColor.black
        painter.fillRect(x1, y1, taille, taille, couleur)
    painter.end()
    ecran_ref.setPixmap(pixmap)

def effacer_canvas():
    if ecran_ref.pixmap():
        pixmap=QPixmap(320, 320)
        pixmap.fill(Qt.GlobalColor.black)
        ecran_ref.setPixmap(pixmap)
        global vram
        vram=[0]*1024

def dispatcher():
    from cpu import registres
    if registres["GPU_STATE"]==1:
        nb_boucle=registres["GPU_LIMIT"]
        start=registres.get("GPU_START", 0)
        for i in range(start, start + nb_boucle):
            if i < 256:
                kernel(i)
        dessine_ecran()
        registres["GPU_STATE"]=0
        if fenetre_ref:
            QApplication.processEvents()
