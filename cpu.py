import sys

ram=[0]*1024
registres={"A": 0, "B": 0, "C":0,"PC": 0,"SP": 800,"FLAGS":0,"GPU_OP":0,"GPU_PARA":0,"GPU_LIMIT":0,"GPU_OFFSET_B":0,"GPU_OFFSET_C":0,
           "GPU_STATE":0,"GPU_START":0}

registres["SP"]=800
def charger_programme(programme):
    global ram, registres
    ram[:]=[0] * 1024
    registres.update({"A": 0, "B": 0, "C":0,"PC": 0,"SP":800,"FLAGS":0})
    for i in range (len(programme)):
        ram[i]=programme[i]

def executer(affichage):
    from gpu import vram, dispatcher
    nom=["A","B","C"]
    while registres["PC"] < len(ram):
        instruction_actuelle=registres["PC"]
        IR=ram[instruction_actuelle]
        registres["PC"]+=1
        match(IR):
            case(1):#addition
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                registres[nom[d]]=registres[nom[s1]]+registres[nom[s2]]
                affichage.append(f"ADD:{nom[d]}={nom[s1]}+{nom[s2]} ({registres[nom[d]]})")
            case(2):#soustraction
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                registres[nom[d]]=registres[nom[s1]]-registres[nom[s2]]
                affichage.append(f"SUB:{nom[d]}={nom[s1]}-{nom[s2]} ({registres[nom[d]]})")
            case(3):#multiplication
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                registres[nom[d]]=registres[nom[s1]]*registres[nom[s2]]
                affichage.append(f"MULT:{nom[d]}={nom[s1]}*{nom[s2]} ({registres[nom[d]]})")
            case(4):#division
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                if registres[nom[s2]]==0:
                    affichage.append("ERR: Div par zero")
                    sys.exit()
                registres[nom[d]]=registres[nom[s1]]//registres[nom[s2]]
                affichage.append("end",f"DIV: {nom[d]}={nom[s1]}/{nom[s2]}({registres[nom[d]]})")
            case(5):#push
                code_reg = ram[registres["PC"]]
                registres["PC"]+=1
                if code_reg not in (0,1,2):
                    affichage.append("Registre invalide pour STK")
                    break
                if registres["SP"]>=len(ram):
                    affichage.append("Stack overflow")
                    sys.exit()
                registres["SP"]+=1
                registre_nom=nom[code_reg]
                valeur=registres[registre_nom]
                ram[registres["SP"]]=valeur
                affichage.append(f"STK : {registre_nom} ({valeur}) enregistré à l'adresse {registres['SP']}")
            case(6):#load
                valeur=ram[registres["PC"]]
                code_reg=ram[registres["PC"]+1]
                registres["PC"]+=2
                if code_reg==0:
                    registres["A"]=valeur
                elif code_reg==1:
                    registres["B"]=valeur
                elif code_reg==2:
                    registres["C"]=valeur
                affichage.append(f"LOAD : {valeur} chargé dans Reg {nom[code_reg]}")
            case(7):#jump
                destination=ram[registres["PC"]]
                registres["PC"]+=1
                registres["PC"]=destination
            case(8):#jump_zero
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["A"]==0:
                    registres["PC"]=adresse
            case(9):#exit
                affichage.append(">>> Fin du programme.")
                break
            case(10):#comparaison
                code_reg1=ram[registres["PC"]]
                code_reg2=ram[registres["PC"]+1]
                registres["PC"]+=2
                match code_reg1:
                    case 0: val1=registres["A"]
                    case 1: val1=registres["B"]
                    case 2: val1=registres["C"]
                match code_reg2:
                    case 0: val2=registres["A"]
                    case 1: val2=registres["B"]
                    case 2: val2=registres["C"]
                if val1==val2:
                    registres["FLAGS"]=0
                elif val1<val2:
                    registres["FLAGS"]=1
                elif val1>val2:
                    registres["FLAGS"]=2
            case(11):#JEQ
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==0:
                    registres["PC"]=adresse
            case(12):#JLT
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==1:
                    registres["PC"]=adresse
            case(13):#JGT
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==2:
                    registres["PC"]=adresse
            case(14):#POP
                code_reg=ram[registres["PC"]]
                registres["PC"]+=1
                if code_reg not in (0,1,2):
                    affichage.append("end", "Registre invalide pour POP")
                    break
                if registres["SP"]<=800:
                    affichage.append("end", "Stack underflow")
                    sys.exit()
                registre_nom=nom[code_reg]
                valeur=ram[registres["SP"]]
                registres["SP"]-=1
                registres[registre_nom]=valeur
                affichage.append(f"POP : ({valeur}) enregistré dans le registre {registre_nom}")
            case(15):#LOADVR
                nombre_a_copier=ram[registres["PC"]]
                registres["PC"]+=1
                for i in range(nombre_a_copier):
                    source_addr=registres["SP"] - i
                    if source_addr>800 and i<1024:
                        vram[i]=ram[source_addr]
                affichage.append(f"LOADVR : {nombre_a_copier} valeurs copiées vers VRAM")
            case(16):#GPUON
                registres["GPU_STATE"]=1
                dispatcher()
            case(17):#GPUOP
                registres["GPU_OP"]=ram[registres["PC"]]
                registres["GPU_PARA"]=ram[registres["PC"]+1]
                registres["PC"]+=2
            case(18):#GPULIM
                registres["GPU_LIMIT"]=ram[registres["PC"]]
                registres["GPU_OFFSET_B"]=ram[registres["PC"]+1]
                registres["GPU_OFFSET_C"]=ram[registres["PC"]+2]
                registres["PC"]+=3
            case(19):#GPUSTART
                registres["GPU_START"]=ram[registres["PC"]]
                registres["PC"]+=1
            case(20):#wait
                ms=ram[registres["PC"]]
                registres["PC"]+=1
                import time
                time.sleep(ms / 1000)
                from gpu import fenetre_ref
                from PyQt6.QtWidgets import QApplication
                if fenetre_ref:
                    QApplication.processEvents()
            case(21):#CALL
                adresse_actuelle=registres["PC"]
                registres["SP"]+=1
                ram[registres["SP"]]=adresse_actuelle
                registres["PC"]=ram[registres["PC"]]
                affichage.append(f"CALL : la fonction à l'adresse {registres['PC']} est exécutée")
            case(22):#RET
                if registres["SP"]>800:
                    adresse_retour=ram[registres["SP"]]
                    registres["SP"]-=1
                    registres["PC"]=adresse_retour
                    affichage.append(f"RET : retour à l'adresse {registres['PC']}")
                else:
                    affichage.append("Stackunderflow")
            case(23):#mov
                source,desti=ram[registres["PC"]],ram[registres["PC"]+1]
                registres["PC"]+=2
                registres[nom[desti]]=registres[nom[source]]
                affichage.append(f"MOV : registre{registres[nom[source]]} enregistrer dans le registre {registres[nom[desti]]}")
            case(24):#STORE
                registre_a_store=ram[registres["PC"]]
                registres["PC"]+=1
                adresse_d_enregistrement=ram[registres["PC"]]
                registres["PC"]+=1
                if adresse_d_enregistrement < len(ram) and registre_a_store < len(nom) and adresse_d_enregistrement >= 0:
                    ram[adresse_d_enregistrement]=registres[nom[registre_a_store]]
                    affichage.append(f"STORE : {registres[nom[registre_a_store]]} enregistrer à l'adresse {adresse_d_enregistrement}")
                elif registre_a_store >= len(nom):
                    affichage.append("Registre invalide")
                elif adresse_d_enregistrement >= len(ram) or adresse_d_enregistrement < 0:
                    affichage.append("Adresse invalide")
            case(25):#STOREIND
                source,desti=ram[registres["PC"]],ram[registres["PC"]+1]
                registres["PC"]+=2
                if source < len(nom) and desti < len(nom):
                    ram[registres[nom[desti]]]=registres[nom[source]]
                    affichage.append(f"STORE_INDIRECT : {registres[nom[source]]} enregistrer dans l'adresse {registres[nom[desti]]}")
                elif source >= len(nom) or desti >= len(nom):
                    affichage.append("Registre invalide")
            case(26):#peek
                source,desti=ram[registres["PC"]],ram[registres["PC"]+1]
                registres["PC"]+=2
                if source >= len(nom) or desti >= len(nom):
                    affichage.append("Registre invalide")
                elif registres[nom[source]]<0 or registres[nom[source]]> len(ram):
                    affichage.append("Adresse invalide")
                else:
                    registres[nom[desti]]=ram[registres[nom[source]]]
                    affichage.append(f"PEEK : Valeur enregistrer dans l'adresse {registres[nom[source]]} enregistrer dans le registre {nom[desti]}")


