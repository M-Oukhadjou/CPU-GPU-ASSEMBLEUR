import sys

ram=[0]*256
registres={"A": 0, "B": 0, "C":0,"PC": 0,"SP":230,"FLAGS":0}

registres["SP"]=230
def charger_programme(programme):
    global ram, registres
    ram[:]=[0]*256
    registres.update({"A": 0, "B": 0, "C":0,"PC": 0,"SP":230,"FLAGS":0})
    for i in range (len(programme)):
        ram[i]=programme[i]

def executer(affichage):
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
                affichage.insert("end", f"ADD:{nom[d]}={nom[s1]}+{nom[s2]} ({registres[nom[d]]})\n")
            case(2):#soustraction
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                registres[nom[d]]=registres[nom[s1]]-registres[nom[s2]]
                affichage.insert("end", f"SUB:{nom[d]}={nom[s1]}-{nom[s2]} ({registres[nom[d]]})\n")
            case(3):#multiplication
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                registres[nom[d]]=registres[nom[s1]]*registres[nom[s2]]
                affichage.insert("end", f"MULT:{nom[d]}={nom[s1]}*{nom[s2]} ({registres[nom[d]]})\n")
            case(4):#division
                d,s1,s2=ram[registres["PC"]],ram[registres["PC"]+1],ram[registres["PC"]+2]
                registres["PC"]+=3
                if registres[nom[s2]]==0:
                    affichage.insert("end","ERR: Div par zero\n")
                    sys.exit()
                registres[nom[d]]=registres[nom[s1]]//registres[nom[s2]]
                affichage.insert("end",f"DIV: {nom[d]}={nom[s1]}/{nom[s2]}({registres[nom[d]]})\n")
            case(5):#stock
                code_reg = ram[registres["PC"]]
                registres["PC"]+=1
                if code_reg not in (0,1,2):
                    affichage.insert("end", "Registre invalide pour STK\n")
                    break
                if registres["SP"] <= 0:
                    affichage.insert("end", "Stack overflow\n")
                    sys.exit()
                registres["SP"]+=1
                registre_nom=nom[code_reg]
                valeur=registres[registre_nom]
                ram[registres["SP"]]=valeur
                affichage.insert("end",
                    f"STK : {registre_nom} ({valeur}) enregistré à l'adresse {registres['SP']}\n")
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
                affichage.insert("end", f"LOAD : {valeur} chargé dans Reg {nom[code_reg]}\n")
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
                affichage.insert("end", ">>> Fin du programme.\n")
                break
            case(10):
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
            case(11):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==0:
                    registres["PC"]=adresse
            case(12):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==1:
                    registres["PC"]=adresse
            case(13):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==2:
                    registres["PC"]=adresse
        affichage.see("end")
