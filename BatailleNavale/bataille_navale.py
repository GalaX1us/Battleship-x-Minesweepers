import time

class navire():
    def __init__(self,valeur,coords,sens,name):
        self.nom = name
        self.abscisse={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
        self.taille = valeur
        self.vie = valeur
        self.coordonne = [int(coords[1]),self.abscisse[coords[0]]]
        self.direction = sens
        self.occupe = self.Case_occupe()
    
    def Get_vie(self):
        return self.vie
    
    def Get_nom(self):
        return self.nom
    
    def Get_taille(self):
        return self.taille
    
    def Get_case_occcupe(self):
        return self.occupe
    
    def Test_placement(self,deja_place):
        for x in self.occupe:
            if not(0<=x[0]<=9) or not(0<=x[1]<=9):
                return False
            for bat in deja_place:
                if x in bat.Get_case_occcupe():
                    return False
        return True

    def Retire_vie(self):
        if self.vie>=1:
            self.vie-=1

    def Case_occupe(self):
        occupe = []
        if self.direction == "DROITE":
            x=0
            y=1
        else:
            x=1
            y=0
        for z in range(self.taille):
            occupe.append([self.coordonne[0]+x*z,self.coordonne[1]+y*z])
        return occupe
    
    def Placer(self,plateau):
        for x in self.occupe:
            plateau[x[0]][x[1]]=self.nom[0].upper()
    
class plateau():

    def __init__(self):
        self.tableau= []
        for i in range(10):
            self.tableau.append(list([" "] * 10))
        self.tableau_cache=[]
        for i in range(10):
            self.tableau_cache.append(list([" "] * 10))

    def Get_plateau(self):
        return self.tableau
    
    def Get_plateau_cache(self):
        return self.tableau_cache

    def Afficher_plateau(self,option=1):
        if option == 1:
            plat=self.tableau_cache
        else:
            plat=self.tableau
        
        abscisse=["A","B","C","D","E","F","G","H","I","J"]
        plateau_str = "\n   | " + " | ".join(str(item) for item in abscisse) + " |"
        plateau_str += "\n--------------------------------------------\n"
        
        for ligne in range(10):
            plateau_str+= " {} |".format(ligne)
            for colonne in range(10):
                plateau_str += " {} |".format(plat[ligne][colonne])

            plateau_str += "\n--------------------------------------------\n"
        plateau_str+= "            X : touché | O : coulé\n"
        
        print(plateau_str)

class player():
    def __init__(self,name):
        self.nom = name
        self.liste_navire=[]
        self.liste_a_placer={"Porte avion":5,"Croiseur":4,"Torpilleur":3,"Sous-marin":3,"Mini":2}
        self.plateau=plateau()
        self.abscisse={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}     

    def Get_name(self):
        return self.nom

    def Get_navire(self):
        return self.liste_navire

    def Choisir_emplacements(self):
        for bateau in self.liste_a_placer.items():
            print("\nVous devez placer un {} qui fait {} cases !".format(bateau[0],bateau[1]))
            self.plateau.Afficher_plateau(0)
            
            coords=input("Entrez les coordonnees de votre navire (ex:A7) : ").upper()
            while coords[1]not in "0123456789" or len(coords)!=2 or (coords[0] not in self.abscisse) or not(0<=int(coords[1])<=9):
                print("Erreur : coordonnees invalide !")
                coords=input("Entrez les coordonnees de votre navire (ex:A7) : ").upper()
            
            direction=input("Entrez la direction de votre navire Droite/Bas : ").upper()
            while direction!="DROITE" and direction!="BAS":
                print("Erreur : direction invalide !")
                direction=input("Entrez la direction de votre navire Droite/Bas : ").upper()
            
            test = navire(bateau[1],coords,direction,bateau[0])
            while not test.Test_placement(self.liste_navire):
                print("\nErreur : placement impossible !")
                print("\nVous devez placer un {} qui fait {} cases !".format(bateau[0],bateau[1]))
                self.plateau.Afficher_plateau(0)
                
                coords=input("Entrez les coordonnees de votre navire (ex:A7) : ").upper()
                while coords[1]not in "0123456789" or len(coords)!=2 or (coords[0] not in self.abscisse) or not(0<=int(coords[1])<=9):
                    print("Erreur : coordonnees invalide !")
                    coords=input("Entrez les coordonnees de votre navire (ex:A7) : ").upper()
                
                direction=input("Entrez la direction de votre navire Droite/Bas : ").upper()
                while direction!="DROITE" and direction!="BAS":
                    print("Erreur : direction invalide !")
                    direction=input("Entrez la direction de votre navire Droite/Bas : ").upper()
                
                test = navire(bateau[1],coords,direction,bateau[0])
            
            test.Placer(self.plateau.Get_plateau())
            self.liste_navire.append(test)
        print("\n======================================")        
        print("Tous les navires de {} sont places".format(self.nom))
        print("======================================\n")
    
    def Tir(self,coords_tir,victime):
        touche=0
        for bateau in victime.Get_navire():
            if coords_tir in bateau.Get_case_occcupe():
                if bateau.Get_vie()==1:
                    for pos in bateau.Get_case_occcupe():
                        victime.plateau.Get_plateau_cache()[pos[0]][pos[1]]="O"
                    bateau.Retire_vie()
                    print("\nVous venez de couler le {} ennemi ({} cases) bateau !".format(bateau.Get_nom(),bateau.Get_taille()))
                    victime.Get_navire().remove(bateau)
                    touche=1
                elif bateau.Get_vie()==0:
                    print("\nCe bateau a déjà coule dommage !")
                    touche=1
                else:
                    victime.plateau.Get_plateau_cache()[coords_tir[0]][coords_tir[1]]="X"
                    print("\nVotre tir a touche un bateau !")
                    bateau.Retire_vie()
                    touche=1
                break
        if touche==0:
            print("\nVous n'avez touche aucun bateau !")

        

def tour_joueurs(joueur,nb,dico):
    
    joueur_actuel=joueur[nb % 2]
    joueur_victime=joueur[(nb+1) % 2]
    
    print("\n================================")
    print("Au tour de {} de tirer !".format(joueur_actuel.Get_name()))
    print("================================\n")
    
    joueur_victime.plateau.Afficher_plateau(1)
    input_tir=input("Entrez les coordonnees pour votre tir (ex:A7) : ").upper()
    while input_tir[1]not in "0123456789" or len(input_tir)!=2 or (input_tir[0] not in dico) or not(0<=int(input_tir[1])<=9):
        print("Erreur : coordonnees invalide !")
        input_tir=input("Entrez les coordonnees pour votre tir (ex:A7) : ").upper()
    coords_tir=[int(input_tir[1]),dico[input_tir[0]]]
    
    joueur_actuel.Tir(coords_tir,joueur_victime)
    joueur_victime.plateau.Afficher_plateau(1)
    time.sleep(3)
    
    if len(joueur_victime.Get_navire())==0:
        fin_partie(joueur_actuel,nb)
    nb+=1
    tour_joueurs(joueur,nb,dico)

def debut_partie():
    print("\n================================")
    print("Bataille Navale by BONADA Nathan")
    print("================================\n")
    
    nombre_tour=0
    abscisse={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
    
    nom1 = input("Comment s'appelle le premier joueur ? :")
    joueur1 = player(nom1)
    nom2 = input("Comment s'appelle le deuxième joueur ? :")
    joueur2 = player(nom2)
    joueurs = [joueur1,joueur2]
    
    joueur1.Choisir_emplacements()
    joueur2.Choisir_emplacements()
    
    print("\nTous les Navires des deux joueurs ont été placés !\n")
    print("========================================================")
    print("Debut de la partie, puisse le sort vous être favorable ! ")
    print("========================================================\n")
    
    tour_joueurs(joueurs,nombre_tour,abscisse)

def fin_partie(gagnant,tours):
    print("Bravo à {} qui remporte la victoire en {} rounds".format(gagnant.Get_name(),tours))

if __name__ == "__main__":
    debut_partie()