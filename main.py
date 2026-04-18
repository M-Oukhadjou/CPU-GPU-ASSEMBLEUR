import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from assembleur import*
from cpu import*
import gpu

def simulation():
    console.clear()
    code_texte=zone_txt.toPlainText()
    if code_texte == "":
        console.append("<span style='color: red;'>Champ vide, rien à compiler.</span>")
    else:
        code_machine=decouper(code_texte)
        charger_programme(code_machine)
        executer(console)



app=QApplication(sys.argv)

layout_principal=QHBoxLayout()
layout_gauche=QVBoxLayout()

fenetre=QWidget()
fenetre.setWindowTitle("IDE")
fenetre.resize(1200, 700)

bouton=QPushButton("COMPILER")
bouton.setFixedSize(100, 30)
bouton.clicked.connect(simulation)

bouton_reset=QPushButton("EFFACER ÉCRAN")
bouton_reset.setFixedSize(120, 30)
bouton_reset.setStyleSheet("background-color: #7f8c8d; color: white;")
bouton_reset.clicked.connect(gpu.effacer_canvas)

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

gpu.fenetre_ref=fenetre
gpu.ecran_ref=canvas_label

layout_gauche.addWidget(zone_txt)
layout_gauche.addWidget(bouton, alignment=Qt.AlignmentFlag.AlignCenter)
layout_gauche.addWidget(bouton_reset, alignment=Qt.AlignmentFlag.AlignCenter)
layout_gauche.addWidget(console)

layout_principal.addLayout(layout_gauche)
layout_principal.addWidget(canvas_label, alignment=Qt.AlignmentFlag.AlignTop)

fenetre.setLayout(layout_principal)
fenetre.show()
sys.exit(app.exec())







