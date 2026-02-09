import sys

ram=[0]*256
registres={"A": 0, "B": 0, "C":0,"PC": 0,"SP":230,"FLAGS":0}

# INITIALISATION
registres["SP"] = 230



def charger_programme(programme):
    global ram, registres
    ram[:]=[0]*256
    registres.update({"A": 0, "B": 0, "C":0,"PC": 0,"SP":230,"FLAGS":0})
    for i in range (len(programme)):
        ram[i]=programme[i]

def executer(affichage):
    while registres["PC"] < len(ram):
        instruction_actuelle=registres["PC"]
        IR=ram[instruction_actuelle]
        registres["PC"]+=1
        match(IR):
            case(1):#addition
                instruction_avtuelle=registres["PC"]
                registres["B"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                instruction_avtuelle=registres["PC"]
                registres["C"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                registres["A"]= registres["B"]+registres["C"]
                affichage.insert("end",f"Addition : {registres['B']}+{registres['C']}={registres['A']}\n")
            case(2):#soustraction
                val1=ram[registres["PC"]]
                registres["PC"]+=1
                val2=ram[registres["PC"]]
                registres["PC"]+=1
                registres["A"]=val1-val2
                affichage.insert("end",f"Soustraction : {val1} - {val2} = {registres['A']}\n")
            case(3):#multiplication
                instruction_avtuelle=registres["PC"]
                registres["B"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                instruction_avtuelle=registres["PC"]
                registres["C"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                registres["A"]= registres["B"]*registres["C"]
                affichage.insert("end", f"Multiplication : {registres['B']}*{registres['C']} = {registres['A']}\n")
            case(4):#division
                instruction_avtuelle=registres["PC"]
                registres["B"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                instruction_avtuelle=registres["PC"]
                registres["C"]=ram[instruction_avtuelle]
                registres["PC"]+=1
                if registres["C"] == 0:
                    affichage.insert("end","Erreur : division par zéro")
                    sys.exit()
                else:
                    registres["A"]= registres["B"]//registres["C"]
                    affichage.insert("end",f"Division : {registres['B']}//{registres['C']}={registres['A']}\n")
            case(5):#stock
                    if registres["SP"] >= len(ram):
                        affichage.insert("end","Stack overflow")
                        sys.exit()
                    else:
                        ram[registres["SP"]]=registres["A"]
                        registres["SP"]+=1
                        affichage.insert("end",f"STK : Valeur {registres['A']} enregistrée à l'adresse {registres['SP']-1}\n")
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
                affichage.insert("end", f"LOAD : {valeur} chargé dans Reg {code_reg}\n")
            case(7):#add_reg
                registres["A"]=registres["B"]+registres["C"]
                affichage.insert("end", f"AREG : Reg B + Reg C = {registres['A']}\n")
            case(8):#mult_reg
                registres["A"]=registres["B"]*registres["C"]
                affichage.insert("end",f"MREG : {registres['B']} * {registres['C']} = {registres['A']}\n")
            case(9):#jump
                destination=ram[registres["PC"]]
                registres["PC"]+=1
                registres["PC"]=destination
            case(11):#jump_zero
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["A"]<=0:
                    registres["PC"]=adresse
            case(10):#exit
                affichage.insert("end", ">>> Fin du programme.\n")
                break
            case(12):
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
            case(13):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==0:
                    registres["PC"]=adresse
            case(14):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==1:
                    registres["PC"]=adresse
            case(15):
                adresse=ram[registres["PC"]]
                registres["PC"]+=1
                if registres["FLAGS"]==2:
                    registres["PC"]=adresse
        affichage.see("end")
