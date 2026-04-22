from cpu_poo import*
from gpu_poo import*
from PCIe import*

class Systeme:

    def __init__(self,nom_du_gpu):
        self.pcie=PCIe()
        self.gpu=gpu()
        self.nom_gpu=nom_du_gpu
        self.pcie.connecter(nom_du_gpu,self.gpu)
        self.cpu=cpu()
        self.cpu.notifier_systeme=self.verification
    
    def charger_programme(self,programme):
        self.cpu.ram[:]=[0] * 1024
        self.cpu.registres.update({"A": 0, "B": 0, "C":0,"PC": 0,"SP":800,"FLAGS":0})
        for i in range (len(programme)):
            self.cpu.ram[i]=programme[i]

    def reset(self):
        self.gpu.effacer_canvas()
        self.cpu.ram = [0]*1024
        self.cpu.registres.update({"A": 0, "B": 0, "C": 0, "PC": 0, "SP": 800, "FLAGS": 0})

    def pilot_gpu(self,instruction,donnee,affichage):
        instruction_gpu={
            15 : "VRAM_DATA",
            16 : "GPU_STATE",
            17 : "GPU_OP",
            18 : "GPU_LIMIT",
            19 : "GPU_START",
            50 : "GPU_PARA",
            51 : "GPU_OFFSET_B",
            52 : "GPU_OFFSET_C"
            }
        if instruction==20: 
            import time
            from PyQt6.QtWidgets import QApplication
            time.sleep(donnee/1000)
            if self.gpu.fenetre_ref:
                QApplication.processEvents()
            affichage.append(f"DRIVER : Pause de {donnee}ms effectuée")
        elif instruction==100:
            self.pcie.transmission(self.nom_gpu,"LOADVR",donnee,affichage)
        elif instruction==17:
            parametre=self.cpu.ram[796]
            self.pcie.transmission(self.nom_gpu, "GPU_OP", donnee, affichage)
            self.pcie.transmission(self.nom_gpu, "GPU_PARA", parametre, affichage)
        elif instruction in instruction_gpu:
            self.pcie.transmission(self.nom_gpu,instruction_gpu[instruction],donnee,affichage)
        else:
            affichage.append(f"Erreur Driver : L'Opcode {instruction} est inconnu !")
            

    def verification(self,affichage):
        if self.cpu.ram[797]==1:
            instruction=self.cpu.ram[798]
            donnee=self.cpu.ram[799]
            self.pilot_gpu(instruction,donnee,affichage)
            self.cpu.ram[797]=0