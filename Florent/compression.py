import struct
import sys
from binaire import GestionBinaire

class Compression:
    
    def __init__(self, fichier):        
#        sys.setrecursionlimit(260000)
        
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
        for i in range(0,(self.m**2)+1):
            self.memCout.append(-1)
            self.memIteration.append({})
    
    def c(self):
#        self.__cout(0,0,0)
        print(self.__cout_iteratif()/8)
                
    def __cout_iteratif(self):
        
        #Initialize last index
        self.memCout[self.m**2] = 0
        self.memIteration[self.m**2][0,0] = 0

        # Iterate on pixels
        for i in range((self.m**2)-1,-1, -1):
            
            precedents = self.memIteration[i+1]
            a = self.binaire.nbBits(self.tab[i])
            
            #iterate on many combinaisons on each index
            for keys, coutPrec in precedents.items() :
                n = keys[0]
                b = keys[1]
                
                # full sequence or no opened sequence
                if n >= 255 or n == 0 :                
                    
                    if (1,a) in self.memIteration[i] :
                        self.memIteration[i][1,a] = min(self.memIteration[i][1,a],coutPrec + 11 + a)
                    else :
                        self.memIteration[i][1,a] = coutPrec + 11 + a 

                    
                # Si le pixel est parfait pour la sequence :
                elif a == b :
                    
                    if (n+1,a) in self.memIteration[i] :
                        self.memIteration[i][n+1,a] = min(self.memIteration[i][n+1,a],coutPrec + a)
                    else :
                        self.memIteration[i][n+1,a] = coutPrec + a

 
                else:
                        
                    # Si le pixel est plus petit :
                    if a < b :                
                        garde = coutPrec + b
                        ferme = coutPrec + a + 11

                        if (n+1,b) in self.memIteration[i] :
                            self.memIteration[i][n+1,b] = min(self.memIteration[i][n+1,b],garde)
                        else :
                            self.memIteration[i][n+1,b] = garde 

                        if (1,a) in self.memIteration[i] :
                            self.memIteration[i][1,a] = min(self.memIteration[i][1,a],ferme)
                        else :
                            self.memIteration[i][1,a] = ferme 
                    
                    # Si le pixel est plus grand :
                    elif a > b :
                        garde = coutPrec + a + n*(a-b)
                        ferme = coutPrec + a + 11

                        if (n+1,a) in self.memIteration[i] :
                            self.memIteration[i][n+1,a] = min(self.memIteration[i][n+1,a],garde)
                        else :
                            self.memIteration[i][n+1,a] = garde 

                        if (1,a) in self.memIteration[i] :
                            self.memIteration[i][1,a] = min(self.memIteration[i][1,a],ferme)
                        else :
                            self.memIteration[i][1,a] = ferme 

            self.memCout[i] = min(value for value in self.memIteration[i].values())

        return self.memCout[0]
    

#    def __cout(self, i, n, b):
#        self.compteur = self.compteur + 1
#        print(self.compteur)
#        # On a deja parcouru cette arbre
#        if (n,b) in self.memIteration[i] :
#            return self.memIteration[i][n,b]
#        
#        # Condition d'arret
#        if (self.m**2) == i :
#            self.memIteration[i][n,b] = 0
#        else :
#            aj = self.binaire.nbBits(self.tab[i])
#
#            if n == 0 or n >= 255 :
#                self.memIteration[i][n,b] = self.__cout(i+1, 1, aj) + 11 + aj
#
#            # Si le pixel est parfait pour la sequence :
#            elif b == aj:
#                self.memIteration[i][n,b] = aj + self.__cout(i+1, n+1, aj)
#
#            # Si le pixel est plus petit : 
#            elif b > aj:
#
#                garde = self.__cout(i+1, n+1, b) + b
#                ferme = self.__cout(i+1, 1, aj) + aj + 11
#                self.memIteration[i][n,b] = min(garde, ferme)
#
#            # Si le pixel est plus grand :
#            else :
#
#                garde = self.__cout(i+1, n+1, aj) + aj + (n-1)*(aj-b)
#                ferme = self.__cout(i+1, 1, aj) + aj + 11
#                self.memIteration[i][n,b] = min(garde, ferme)
#
#        if self.memCout[i] == -1 or self.memIteration[i][n,b] < self.memCout[i] :
#            self.memCout[i] = self.memIteration[i][n,b]
#            
#        return self.memIteration[i][n,b]
                
        
compression = Compression('images/images/Lena.raw')
compression.c()