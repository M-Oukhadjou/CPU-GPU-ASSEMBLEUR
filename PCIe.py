class PCIe:

    def __init__(self):
        self.appareils={}
    
    def connecter(self,nom, instance_du_composant):
        self.appareils[nom]=instance_du_composant

    def transmission(self,destinataire, instruction, donnee,affichage):
        if destinataire in self.appareils:
            appareils=self.appareils[destinataire]
            return appareils.recevoir(instruction, donnee)
        else:
            affichage.append((f"[PCIe] Erreur : Le destinataire '{destinataire}' n'existe pas."))
