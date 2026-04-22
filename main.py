import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt,QTimer
from assembleur import*
from ordinateur_poo import*

ordi=Systeme("gpu_1")

def simulation():
    console.clear()
    code_texte=zone_txt.toPlainText()
    if code_texte == "":
        console.append("<span style='color: red;'>Champ vide, rien à compiler.</span>")
    else:
        code_machine=decouper(code_texte)
        ordi.charger_programme(code_machine)
        ordi.cpu.executer(console)

timer=QTimer()

app=QApplication(sys.argv)

layout_principal=QHBoxLayout()
layout_gauche=QVBoxLayout()
layout_droit=QVBoxLayout()
layout_tableau_de_bord=QFormLayout()


etat_des_registres=QGroupBox("ÉTAT DES REGISTRES")
etat_des_registres.setMaximumHeight(170)
etat_des_registres.setLayout(layout_tableau_de_bord)

label_A=QLabel("0")
label_B=QLabel("0")
label_C=QLabel("0")
label_PC=QLabel("0")
label_SP=QLabel("0")
label_FLAGS=QLabel("0")

layout_tableau_de_bord.addRow("Registre A :", label_A)
layout_tableau_de_bord.addRow("Registre B :", label_B)
layout_tableau_de_bord.addRow("Registre C :", label_C)
layout_tableau_de_bord.addRow("Registre PC :", label_PC)
layout_tableau_de_bord.addRow("Registre SP :", label_SP)
layout_tableau_de_bord.addRow("Registre FLAGS :", label_FLAGS)

def rafraichir_affichage():
    label_A.setText(str(ordi.cpu.registres["A"]))
    label_B.setText(str(ordi.cpu.registres["B"]))
    label_C.setText(str(ordi.cpu.registres["C"]))
    label_PC.setText(str(ordi.cpu.registres["PC"]))
    label_SP.setText(str(ordi.cpu.registres["SP"]))
    label_FLAGS.setText(str(ordi.cpu.registres["FLAGS"]))

timer.timeout.connect(rafraichir_affichage)

timer.start(700)

fenetre=QWidget()
fenetre.setWindowTitle("IDE")
fenetre.resize(1200, 700)

bouton=QPushButton("COMPILER")
bouton.setFixedSize(100, 30)
bouton.clicked.connect(simulation)

bouton_reset=QPushButton("EFFACER ÉCRAN")
bouton_reset.setFixedSize(120, 30)
bouton_reset.setStyleSheet("background-color: #7f8c8d; color: white;")
bouton_reset.clicked.connect(ordi.reset)

console=QTextEdit()
console.setReadOnly(True)
console.setStyleSheet("""
    background-color: #1e1e1e; 
    color: #00ff00; 
    font-family: 'Consolas', 'Monospace';
    font-size: 14px;
    border: 1px solid #333;""")

zone_txt=QTextEdit()

canvas_label=QLabel()
canvas_label.setFixedSize(320, 320)
canvas_label.setStyleSheet("""
    background-color: black; 
    border: 1px solid gray;
""")

pixmap=QPixmap(320, 320)
pixmap.fill(Qt.GlobalColor.black)
canvas_label.setPixmap(pixmap)

ordi.gpu.fenetre_ref=fenetre
ordi.gpu.ecran_ref=canvas_label

layout_gauche.addWidget(zone_txt)
layout_gauche.addWidget(bouton,alignment=Qt.AlignmentFlag.AlignCenter)
layout_gauche.addWidget(bouton_reset,alignment=Qt.AlignmentFlag.AlignCenter)
layout_gauche.addWidget(console)

layout_droit.addWidget(etat_des_registres)
layout_droit.addWidget(canvas_label, alignment=Qt.AlignmentFlag.AlignTop)

layout_principal.addLayout(layout_gauche)
layout_principal.addLayout(layout_droit)


fenetre.setLayout(layout_principal)
fenetre.show()
sys.exit(app.exec())







