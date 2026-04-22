from PyQt6.QtWidgets import QApplication

class cpu:
    
    def __init__(self):
        self.ram=[0]*1024
        self.registres={"A": 0, "B": 0, "C":0,"PC": 0,"SP": 800,"FLAGS":0}
        self.nom=["A","B","C"]
        self.notifier_systeme=None
        self.running=True

    def add(self,val1,val2):
        return self.registres[self.nom[val1]]+self.registres[self.nom[val2]]
    
    def sub(self,val1,val2):
        return self.registres[self.nom[val1]]-self.registres[self.nom[val2]]
    
    def mult(self,val1,val2):
        return self.registres[self.nom[val1]]*self.registres[self.nom[val2]]
    
    def div(self,val1,val2):
        return self.registres[self.nom[val1]]//self.registres[self.nom[val2]]
    
    def push(self,code_reg,affichage):
        self.registres["SP"]+=1
        registre_nom=self.nom[code_reg]
        valeur=self.registres[registre_nom]
        self.ram[self.registres["SP"]]=valeur
        affichage.append(f"STK : {self.nom[code_reg]} ({valeur}) enregistré à l'adresse {self.registres['SP']}")
    
    def load(self,code_reg,valeur,affichage):
        registre_cible=self.nom[code_reg]
        self.registres[registre_cible]=valeur
        affichage.append(f"LOAD : {valeur} chargé dans Reg {registre_cible}")

    def jump(self,destination):
        self.registres["PC"]=destination
    
    def jump_zero(self,destination):
        if self.registres["A"]==0:
            self.registres["PC"]=destination

    def exit(self,affichage):
        affichage.append(">>> Fin du programme.")
        self.running=False
    
    def cmp(self,reg_1,reg_2):
        val1=self.registres[self.nom[reg_1]]
        val2=self.registres[self.nom[reg_2]]
        if val1==val2:
            self.registres["FLAGS"]=0
        elif val1<val2:
            self.registres["FLAGS"]=1
        elif val1>val2:
            self.registres["FLAGS"]=2

    def JEQ(self,adresse):
        if self.registres["FLAGS"]==0:
            self.registres["PC"]=adresse
    
    def JLT(self,adresse):
        if self.registres["FLAGS"]==1:
            self.registres["PC"]=adresse
    
    def JGT(self,adresse):
        if self.registres["FLAGS"]==2:
            self.registres["PC"]=adresse
    
    def pop(self,code_reg,affichage):
        registre_nom=self.nom[code_reg]
        valeur=self.ram[self.registres["SP"]]
        self.registres["SP"]-=1
        self.registres[registre_nom]=valeur
        affichage.append(f"POP : ({valeur}) enregistré dans le registre {registre_nom}")
    
    def loadvr(self,nb,affichage):
        self.ram[797]=1
        self.ram[798]=100 
        self.ram[799]=0
        self.notifier_systeme(affichage)
        for i in range(nb):
            source_addr=self.registres["SP"]-i
            if source_addr < 1024:
                valeur=self.ram[source_addr]
                self.ram[797]=1
                self.ram[798]=15
                self.ram[799]=valeur
                self.notifier_systeme(affichage)

    def gpuon(self,affichage):
        self.ram[797]=1
        self.ram[798]=16
        self.ram[799]=1
        self.notifier_systeme(affichage)
    
    def gpuop(self, op, para, affichage):
        self.ram[796]=para
        self.ram[797]=1
        self.ram[798]=17
        self.ram[799]=op
        self.notifier_systeme(affichage)

    def gpustart(self,start,affichage):
        self.ram[797]=1
        self.ram[798]=19
        self.ram[799]=start
        self.notifier_systeme(affichage)

    def gpulim(self,lim,off_b,off_c,affichage):
        ordres=[(18, lim),(51, off_b),(52, off_c)]
        for code, valeur in ordres:
            self.ram[797]=1
            self.ram[798]=code
            self.ram[799]=valeur
            self.notifier_systeme(affichage)

    def wait(self,temps,affichage):
        self.ram[797]=1
        self.ram[798]=20
        self.ram[799]=temps
        self.notifier_systeme(affichage)

    def call(self,adresse_actuelle,affichage):
        self.ram[self.registres["SP"]]=adresse_actuelle
        self.registres["PC"]=self.ram[self.registres["PC"]]
        affichage.append(f"CALL : la fonction à l'adresse {self.registres['PC']} est exécutée")

    def ret(self,affichage):
        adresse_retour=self.ram[self.registres["SP"]]
        self.registres["SP"]-=1
        self.registres["PC"]=adresse_retour
        affichage.append(f"RET : retour à l'adresse {self.registres['PC']}")

    def mov(self,affichage,source,desti):
        self.registres[self.nom[desti]]=self.registres[self.nom[source]]
        affichage.append(f"MOV : registre{self.registres[self.nom[source]]} enregistrer dans le registre {self.registres[self.nom[desti]]}")

    def store(self,registre_a_store,adresse_d_enregistrement,affichage):
        self.ram[adresse_d_enregistrement]=self.registres[self.nom[registre_a_store]]
        affichage.append(f"STORE : {self.registres[self.nom[registre_a_store]]} enregistrer à l'adresse {adresse_d_enregistrement}")

    def storeind(self,source,desti,affichage):
        self.ram[self.registres[self.nom[desti]]]=self.registres[self.nom[source]]
        affichage.append(f"STORE_INDIRECT : {self.registres[self.nom[source]]} enregistrer dans l'adresse {self.registres[self.nom[desti]]}")

    def peek(self,source,desti,affichage):
        self.registres[self.nom[desti]]=self.ram[self.registres[self.nom[source]]]
        affichage.append(f"PEEK : Valeur enregistrer dans l'adresse {self.registres[self.nom[source]]} enregistrer dans le registre {self.nom[desti]}")

    def executer(self,affichage):
        self.running=True
        while self.running and self.registres["PC"] < len(self.ram):
            instruction_actuelle=self.registres["PC"]
            IR=self.ram[instruction_actuelle]
            self.registres["PC"]+=1
            match(IR):
                case(0):
                    affichage.append("FIN RAM atteinte")
                    break
                case(1):
                    d, s1, s2 = self.ram[self.registres["PC"]], self.ram[self.registres["PC"]+1], self.ram[self.registres["PC"]+2]
                    self.registres["PC"]+=3
                    self.registres[self.nom[d]] = self.add(s1, s2)
                    affichage.append(f"ADD:{self.nom[d]}={self.nom[s1]}+{self.nom[s2]} ({self.registres[self.nom[d]]})")
                case(2):
                    d, s1, s2 = self.ram[self.registres["PC"]], self.ram[self.registres["PC"]+1], self.ram[self.registres["PC"]+2]
                    self.registres["PC"]+=3
                    self.registres[self.nom[d]]=self.sub(s1, s2)
                    affichage.append(f"SUB:{self.nom[d]}={self.nom[s1]}-{self.nom[s2]} ({self.registres[self.nom[d]]})")
                case(3):
                    d, s1, s2 = self.ram[self.registres["PC"]], self.ram[self.registres["PC"]+1], self.ram[self.registres["PC"]+2]
                    self.registres["PC"]+=3
                    self.registres[self.nom[d]] = self.mult(s1, s2)
                    affichage.append(f"MULT:{self.nom[d]}={self.nom[s1]}*{self.nom[s2]} ({self.registres[self.nom[d]]})")
                case(4):
                    d, s1, s2 = self.ram[self.registres["PC"]], self.ram[self.registres["PC"]+1], self.ram[self.registres["PC"]+2]
                    self.registres["PC"]+=3
                    if self.registres[self.nom[s2]]==0:
                        affichage.append("ERR: Div par zero")
                        break
                    else:
                        self.registres[self.nom[d]] = self.div(s1, s2)
                        affichage.append(f"DIV:{self.nom[d]}={self.nom[s1]}//{self.nom[s2]} ({self.registres[self.nom[d]]})")
                case(5):
                    code_reg=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    if code_reg not in (0,1,2):
                        affichage.append("Registre invalide pour STK")
                        break
                    if self.registres["SP"]>=len(self.ram):
                        affichage.append("Stack overflow")
                        break
                    self.push(code_reg,affichage)
                case(6):
                    valeur=self.ram[self.registres["PC"]]
                    code_reg=self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    self.load(code_reg,valeur,affichage)
                case(7):
                    destination=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.jump(destination)
                case(8):
                    adresse=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.jump_zero(adresse)
                case(9):
                    self.exit(affichage)
                    return
                case(10):
                    code_reg1=self.ram[self.registres["PC"]]
                    code_reg2=self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    self.cmp(code_reg1,code_reg2)
                case(11):
                    adresse=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.JEQ(adresse)
                case(12):
                    adresse=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.JLT(adresse)
                case(13):
                    adresse=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.JGT(adresse)
                case(14):
                    code_reg=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    if code_reg >= len(self.nom):
                        affichage.append("Registre invalide pour POP")
                        break
                    if self.registres["SP"]<=800:
                        affichage.append("Stack underflow")
                        self.running=False
                    self.pop(code_reg,affichage)
                case(15):
                    nombre_a_copier=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.loadvr(nombre_a_copier,affichage)
                case(16):
                    self.gpuon(affichage)
                case(17):
                    operation_gpu=self.ram[self.registres["PC"]]
                    parametre_gpu=self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    self.gpuop(operation_gpu,parametre_gpu,affichage)
                case(18):
                    gpu_limit=self.ram[self.registres["PC"]]
                    gpu_offset_b=self.ram[self.registres["PC"]+1]
                    gpu_offset_c=self.ram[self.registres["PC"]+2]
                    self.registres["PC"]+=3
                    self.gpulim(gpu_limit,gpu_offset_b,gpu_offset_c,affichage)
                case(19):
                    start=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.gpustart(start,affichage)
                case(20):
                    ms=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    self.wait(ms,affichage)
                case(21):
                    adresse_actuelle=self.registres["PC"]
                    self.registres["SP"]+=1
                    self.call(adresse_actuelle,affichage)
                case(22):
                    if self.registres["SP"]>800:
                        self.ret(affichage)
                    else:
                        affichage.append("Stackunderflow")
                case(23):
                    source,desti=self.ram[self.registres["PC"]],self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    self.mov(affichage,source,desti)
                case(24):
                    registre_a_store=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    adresse_d_enregistrement=self.ram[self.registres["PC"]]
                    self.registres["PC"]+=1
                    if adresse_d_enregistrement < len(self.ram) and registre_a_store < len(self.nom) and adresse_d_enregistrement >= 0:
                        self.store(registre_a_store,adresse_d_enregistrement,affichage)
                    elif registre_a_store >= len(self.nom):
                        affichage.append("Registre invalide")
                    elif adresse_d_enregistrement >= len(self.ram) or adresse_d_enregistrement<0:
                        affichage.append("Adresse invalide")
                case(25):
                    source,desti=self.ram[self.registres["PC"]],self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    if source < len(self.nom) and desti < len(self.nom):
                        self.storeind(source,desti,affichage)
                    elif source >= len(self.nom) or desti >= len(self.nom):
                        affichage.append("Registre invalide")
                case(26):
                    source,desti=self.ram[self.registres["PC"]],self.ram[self.registres["PC"]+1]
                    self.registres["PC"]+=2
                    if source >= len(self.nom) or desti >= len(self.nom):
                        affichage.append("Registre invalide")
                    elif self.registres[self.nom[source]]<0 or self.registres[self.nom[source]]> len(self.ram):
                        affichage.append("Adresse invalide")
                    else:
                        self.peek(source,desti,affichage)

                    


                    

                    

                    


