
INSTRUCTIONS_SET={
    "ADD":  (1, 3),
    "SUB":  (2, 3),
    "MULT": (3, 3),
    "DIV":  (4, 3),
    "STK":  (5, 1),
    "LOAD": (6, 2),
    "JUMP": (7, 1),
    "JZ":   (8, 1),
    "EXIT": (9, 0),
    "CMP":  (10, 2),
    "JEQ":  (11, 1),
    "JLT":  (12, 1),
    "JGT":  (13, 1),
    "POP":  (14, 1),
}
def label(donnee):
    adresse=0
    lignes=donnee.splitlines()
    dico_label={}
    for i in range (len(lignes)):
        mot=lignes[i].split()
        for j in range(len(mot)):
            if mot[j] in INSTRUCTIONS_SET:
                adresse=adresse+1+INSTRUCTIONS_SET[mot[j]][1]
            elif mot[j].endswith(":"):
                dico_label[mot[j][:-1]]=adresse
    return dico_label



def decouper(donnee):
    dico_label=label(donnee)
    lignes=donnee.splitlines()
    l=[]
    for phrase in lignes:
        val=phrase.split()
        if val:
            mot=val[0].upper()
            if mot in INSTRUCTIONS_SET:
                l.append(INSTRUCTIONS_SET[mot][0])
                for arg in val[1:]:
                    try:
                        l.append(int(arg))
                    except:
                        l.append(dico_label[arg])
    return l

