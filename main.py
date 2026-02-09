from tkinter import*
from assembler import*
from cpu import*

def simulation():
    affichage.delete("1.0","end")
    code_texte=txt.get("1.0", "end-1c")
    code_machine=decouper(code_texte)
    charger_programme(code_machine)
    executer(affichage)


fenetre=Tk()
fenetre.title("ASSEMBLEUR")
fenetre.geometry("600x650")
txt=Text(fenetre, bg="white")
txt.pack(expand=True,fill=BOTH,padx=10,pady=5)
bouton=Button(fenetre,text="COMPILER",command=simulation)
bouton.pack(pady=5)
affichage=Text(fenetre,bg="black",fg="green")
affichage.pack(expand=True, fill=BOTH, padx=10, pady=5)
fenetre.mainloop()