import struct
import sys
from binaire import GestionBinaire

class Compression:
    
    def __init__(self, fichier):
        sys.setrecursionlimit(1500)
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
        
    def initMem(self):
        for i in range(0,(self.m**2)):
            self.memCout.append(-1)
            self.memIteration.append(-1)
    
    def c(self):
        self.__cout(0,0,0)

    def __cout(self, i, n, b):
               
        # On a deja parcouru cette arbre
        if self.memIteration[i] != -1 and self.memIteration[i].hasKey((n,nbBitSequence)) :
            return self.memIteration[i].get((n,b))

        if self.memIteration[i] == -1 :
            self.memIteration[i] = []
        
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
                  
#     def cout(self, i, n, b):
#
#                
#        # Condition d'arret
#        if (self.m**2) == i :
#            return 0
#
#        aj = self.nbBits(i)
#        
#        # Si la sequence est rempli ou qu’il n’y en a pas :
#        if n == 0 or n >= 255 :
#            return self.cout(i+1, 1, aj) + 11 + aj
#
#        # Si le pixel est parfait pour la sequence :
#        if b == aj:
#            return aj + self.cout(i+1, n+1, aj)
#
#        # Si le pixel est plus petit : 
#        if b > aj:
#
#            garde = self.cout(i+1, n+1, b) + b
#            ferme = self.cout(i+1, 1, aj) + aj + 11
#            return min(garde, ferme)
#
#        # Si le pixel est plus grand :
#        else :
#
#            garde = self.cout(i+1, n+1, aj) + aj + (n-1)*(aj-b)
#            ferme = self.cout(i+1, 1, aj) + aj + 11
#            return min(garde, ferme)

compression = Compression('images/images/Baboon.raw')
compression.c()
print(compression.memCout[0])