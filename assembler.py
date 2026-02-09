
INSTRUCTIONS_SET={
    "ADD":  (1, 2),
    "SUB":  (2, 1),
    "MULT": (3, 2),
    "DIV":  (4, 2),
    "OUT":  (5, 0),
    "LOAD": (6, 2),
    "AREG": (7, 0),
    "MREG": (8, 0),
    "JUMP": (9, 1),
    "EXIT": (10, 0),
    "JZ":   (11, 1),
    "CMP":  (12, 2),
    "JEQ":  (13, 1),
    "JLT":  (14, 1),
    "JGT":  (15, 1),
}

def decouper(donnee):
    lignes = donnee.splitlines()
    l=[]
    for phrase in lignes:
        val = phrase.split()
        if val:
            mot = val[0].upper()
            if mot in INSTRUCTIONS_SET:
                l.append(INSTRUCTIONS_SET[mot][0])
                for arg in val[1:]:
                    try:
                        l.append(int(arg))
                    except:
                        l.append(0)
    return l



