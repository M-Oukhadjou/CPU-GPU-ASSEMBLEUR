from PyQt6.QtGui import QPainter,QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class gpu:
    def __init__(self):
        self.vram=[0]*1024
        self.registres_gpu={"GPU_OP":0,"GPU_PARA":0,"GPU_LIMIT":0,"GPU_OFFSET_B":0,"GPU_OFFSET_C":0,"GPU_STATE":0,"GPU_START":0,"VRAM_INDEX":0}
        self.fenetre_ref=None
        self.ecran_ref=None
    
    def kernel(self,id):
        parametre=self.registres_gpu["GPU_PARA"]
        operation=self.registres_gpu["GPU_OP"]
        valeurA=self.vram[id]
        valeurB=self.vram[id+self.registres_gpu["GPU_OFFSET_B"]]
        valeurC=self.vram[id+self.registres_gpu["GPU_OFFSET_C"]]
        match(operation):
            case(1):
                self.vram[id]=valeurA+parametre
            case(2):
                self.vram[id]=valeurA-parametre
            case(3):
                self.vram[id]=valeurA*parametre
            case(4):
                if parametre!=0:
                    self.vram[id]=valeurA//parametre
            case(5):
                self.vram[id+self.registres_gpu["GPU_OFFSET_C"]]=valeurA+valeurB
            case(6):
                self.vram[id+self.registres_gpu["GPU_OFFSET_C"]]=valeurA-valeurB
            case(7):
                self.vram[id+self.registres_gpu["GPU_OFFSET_C"]]=valeurA*valeurB
            case(8):
                if valeurB!=0:
                    self.vram[id+self.registres_gpu["GPU_OFFSET_C"]]=valeurA//valeurB
            case(9):
                self.vram[id]=1

    def dessine_ecran(self):
        if self.ecran_ref is None:
            return
        pixmap = self.ecran_ref.pixmap()
        if pixmap is None:
            return
        pixmap=self.ecran_ref.pixmap()
        painter=QPainter(pixmap)
        taille=20
        for i in range(len(self.vram)):
            x=i%16
            y=i//16
            x1=x*taille
            y1=y*taille
            couleur=Qt.GlobalColor.white if self.vram[i] != 0 else Qt.GlobalColor.black
            painter.fillRect(x1, y1, taille, taille, couleur)
        painter.end()
        self.ecran_ref.setPixmap(pixmap)

    def effacer_canvas(self):
        if self.ecran_ref is not None:
            pixmap=self.ecran_ref.pixmap()
            if self.ecran_ref.pixmap():
                pixmap = QPixmap(320, 320)
                pixmap.fill(Qt.GlobalColor.black)
                self.ecran_ref.setPixmap(pixmap)
        self.vram = [0] * 1024

    def dispatcher(self):
        if self.registres_gpu["GPU_STATE"]==1:
            nb_boucle=self.registres_gpu["GPU_LIMIT"]
            start=self.registres_gpu["GPU_START"]
            for i in range(start, start + nb_boucle):
                if i < 256:
                    self.kernel(i)
            self.dessine_ecran()
            self.registres_gpu["GPU_STATE"]=0
            if self.fenetre_ref:
                QApplication.processEvents()
    

    def recevoir(self,instruction,donnee):
        if instruction=="VRAM_DATA":
            index=self.registres_gpu["VRAM_INDEX"]
            if index<1024:
                self.vram[index]=donnee
                self.registres_gpu["VRAM_INDEX"]+=1
        elif instruction=="LOADVR":
            self.registres_gpu["VRAM_INDEX"]=0
        elif instruction in self.registres_gpu:
            self.registres_gpu[instruction]=donnee
        if instruction=="GPU_STATE" and donnee==1:
            self.dispatcher()
