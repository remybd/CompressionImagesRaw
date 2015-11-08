import struct
import sys
from binaire import GestionBinaire

class Compression:
    
    def __init__(self, fichier):        
        sys.setrecursionlimit(260000)
        
        # helper binaire
        self.binaire = GestionBinaire()
        self.binaire.readFile(fichier)
        
        # Taille de l'image carre en largeur/longueur
        self.m = self.binaire.getTaille()
        
        # Tableau linearise
        self.tab = self.binaire.getPixels()
        
        # Tableau memoisation
        self.memCout = []
        self.memIteration = []
        
        #Initialisation des tableaux de memoisation
        self.initMem()
        self.compteur = 0
        
    def initMem(self):
        for i in range(0,(self.m**2)+1):
            self.memCout.append(-1)
            self.memIteration.append({})
    
    def c(self):
#        self.__cout(0,0,0)
        print(self.__cout_iteratif())

    def __cout(self, i, n, b):
        self.compteur = self.compteur + 1
        print(self.compteur)
        # On a deja parcouru cette arbre
        if (n,b) in self.memIteration[i] :
            return self.memIteration[i][n,b]
        
        # Condition d'arret
        if (self.m**2) == i :
            self.memIteration[i][n,b] = 0
        else :
            aj = self.binaire.nbBits(self.tab[i])

            # Si la sequence est rempli ou qu’il n’y en a pas :
            if n == 0 or n >= 255 :
                self.memIteration[i][n,b] = self.__cout(i+1, 1, aj) + 11 + aj

            # Si le pixel est parfait pour la sequence :
            elif b == aj:
                self.memIteration[i][n,b] = aj + self.__cout(i+1, n+1, aj)

            # Si le pixel est plus petit : 
            elif b > aj:

                garde = self.__cout(i+1, n+1, b) + b
                ferme = self.__cout(i+1, 1, aj) + aj + 11
                self.memIteration[i][n,b] = min(garde, ferme)

            # Si le pixel est plus grand :
            else :

                garde = self.__cout(i+1, n+1, aj) + aj + (n-1)*(aj-b)
                ferme = self.__cout(i+1, 1, aj) + aj + 11
                self.memIteration[i][n,b] = min(garde, ferme)

        if self.memCout[i] == -1 or self.memIteration[i][n,b] < self.memCout[i] :
            self.memCout[i] = self.memIteration[i][n,b]
            
        return self.memIteration[i][n,b]
                
    def __cout_iteratif(self):
        
        a = []
        for i in range(0, (self.m**2)):
            a.append(self.binaire.nbBits(self.tab[i]))
                
        b = 0
        n = 0
        
        for i in range((self.m**2)-1,-1, -1):
            coutPrec = self.memCout[i+1]
            
            if n == 0 or n >= 255 :
                self.memCout[i] = coutPrec + 11 + a[i]
                b = a[i]
                n = 1
            
            # Si le pixel est parfait pour la sequence :
            elif a[i] == b :
                self.memCout[i] = coutPrec + a[i]
                b = a[i]
                n = n + 1
            
            # Si le pixel est plus petit : 
            elif a[i] < b :
                garde = coutPrec + b
                ferme = coutPrec + a[i] + 11
                self.memCout[i] = min(garde,ferme)
                if self.memCout[i] == garde :
                    b = b
                    n = n + 1
                else:
                    b = a[i]
                    n = 1
                
            # Si le pixel est plus grand :
            elif a[i] > b :
                garde = coutPrec + a[i] + n*(a[i]-b)
                ferme = coutPrec + a[i] + 11
                self.memCout[i] = min(garde,ferme) 
                if self.memCout[i] == garde :
                    b = a[i]
                    n = n + 1
                else:
                    b = a[i]
                    n = 1
                    
        return self.memCout[0]
                
                
        
compression = Compression('images/images/Barbara.raw')
compression.c()
print(compression.memCout[0])