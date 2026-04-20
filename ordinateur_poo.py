from cpu_poo import*
from gpu_poo import*

class Systeme:

    def __init__(self):
        self.gpu=gpu()
        self.cpu=cpu(self.gpu)
    
    def charger_programme(self,programme):
        self.cpu.ram[:]=[0] * 1024
        self.cpu.registres.update({"A": 0, "B": 0, "C":0,"PC": 0,"SP":800,"FLAGS":0})
        for i in range (len(programme)):
            self.cpu.ram[i]=programme[i]

    def reset(self):
        self.gpu.effacer_canvas()
        self.cpu.ram = [0]*1024
        self.cpu.registres.update({"A": 0, "B": 0, "C": 0, "PC": 0, "SP": 800, "FLAGS": 0})