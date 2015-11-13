import struct
import sys
from binaire import GestionBinaire

class Compression:
    
    def __init__(self, fichier):        
#        sys.setrecursionlimit(260000)
        
        self.filePath = fichier        
        
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
        print("Algorithme iteratif :")
        cout = self.__cout_iteratif()
        print "fichier de depart : ",(self.m**2), " octets soit ", (self.m**2)*8, " bits"
        print "fichier apres compression : ",cout/8, " octets soit ", cout, " bits"
        print "Compression de ", (1-(cout/((self.m**2)*8)))*100, " %" 
        self.solution()
    
    def __cout_iteratif(self):
        
        #Initialisation de la derniere case du tableau (juste apres le dernier pixel)
        self.memCout[self.m**2] = 0
        self.memIteration[self.m**2][0,0] = 0

        # Iteration sur les pixels
        for i in range((self.m**2)-1,-1, -1):
            
            precedents = self.memIteration[i+1]
            a = self.binaire.nbBits(self.tab[i])
            
            # Iteration sur les combinaison (i,n,b) de la case precedemment calculee
            for keys, coutPrec in precedents.items() :
                n = keys[0]
                b = keys[1]
                
                # sequence rempli ou aucune sequence
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
    
    def solution(self):
        nPrec = 0
        bPrec = 0
        # Initialise n et b de la premiere case
        for keys, coutPrec in self.memIteration[0].items():
            if self.memCout[0] == coutPrec :
                nPrec = keys[0]
                bPrec = keys[1]
        
        # Iteration sur le tableau des combinaisons
        for i in range(1,(self.m**2)+1):
            #Iteration sur les combinaisons
            for keys, coutPrec in self.memIteration[i].items():
                n = keys[0]
                b = keys[1]
                
                if i == 5619 and n == 5 and b==8 :
                    print self.memIteration[i]
                # si on doit ouvrir une nouvelle sequence
                if nPrec == 1:
                    if (self.memCout[i-1] != coutPrec + 11 + bPrec):
                        del self.memIteration[i][keys]
                # si le n ne correspond pas, on supprime les mauvaises valeurs
                elif n != nPrec-1 or b != bPrec :
                    del self.memIteration[i][keys]
            
            #Iteration sur les combinaisons qui correspondent au n de la meilleur solution
            self.memCout[i] = min(value for value in self.memIteration[i].values())
            for keys, coutPrec in self.memIteration[i].items():
                if self.memCout[i] != coutPrec:
                    del self.memIteration[i][keys]
                else:
                    nPrec = keys[0]
                    bPrec = keys[1]
        
            print i, " " ,self.memIteration[i]
            
            
            
            
    def uncompresse(self):
        print "decompression"
            
            
            
            
            
            
            
            
    def shouldWeCompressTheFile(self):
        listCutFile = self.filePath.split('.')
        length = len(listCutFile)
        if listCutFile[length-1] == 'seg':
            return False
        else:
            return True
            
        
        
print "print"
filePath = 'images/images/Lena.raw'
compression = Compression(filePath)
print "test"
if(compression.shouldWeCompressTheFile()):
    compression.c()
else:
    compression.uncompresse()    
    
    
    
    