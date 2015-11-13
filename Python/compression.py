import struct
import sys
from binaire import GestionBinaire

class Compression:
    
    def __init__(self, fichier):        
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
        print "Algorithme iteratif :"
        print "fichier de depart : ",(self.m**2), " octets soit ", (self.m**2)*8, " bits"
        cout = self.__cout_iteratif()
        print "fichier apres compression : ",cout/8, " octets soit ", cout, " bits"
        self.solution()
    
    def __cout_iteratif(self):
        
        #Initialisation de la derniere case du tableau (juste apres le dernier pixel)
        self.memCout[self.m**2] = 0
        self.memIteration[self.m**2][0,0] = 0

        # Iteration sur les pixels
        for i in range((self.m**2)-1,-1, -1):
            
            precedents = self.memIteration[i+1]
            a = self.binaire.nbBits(self.tab[i])
            
            # Iteration sur les combinaisons (i,n,b) de la case precedemment calculee
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
                elif n != nPrec-1 or b > bPrec :
                    del self.memIteration[i][keys]
            
            #Iteration sur les combinaisons qui correspondent au n de la meilleur solution
            self.memCout[i] = min(value for value in self.memIteration[i].values())
            for keys, coutPrec in self.memIteration[i].items():
                if self.memCout[i] != coutPrec:
                    del self.memIteration[i][keys]
                else:
                    nPrec = keys[0]
                    bPrec = keys[1]
                    
    def __cout_recursif(self, i, n, b):

        # On a deja parcouru cette arbre
        if (n,b) in self.memIteration[i] :
            return self.memIteration[i][n,b]

        # Condition d'arret
        if (self.m**2) == i :
            self.memIteration[i][n,b] = 0
        else :
            aj = self.binaire.nbBits(self.tab[i])

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
            
            
    def uncompresse(self):
		print "decompression initialisee"
		self.tab = self.binaire.readFileToUncompress(self.filePath)
		tab = self.tab
		result = []
		
		i=0
		#parcours de tous les bytes du fichier a decompresser

		#recuperation des variables dans l'entete du segment
		#n = struct.unpack('<B',octet)
		n = tab[i]
		i+=1
		b = tab[i] >> 5
		nbBitRestant = 5
		
		while i < len(tab) and n > 0:
			if n == 0:
				#recuperation des variables dans l'entete du segment
				n = tab[i]
				i+=1
				b = tab[i] >> 5
				nbBitRestant = 5
				
				if nbBitRestant == 8:
					n = tab[i]
					nbBitRestant = 8
				else:
					octet = tab[i]
					i+=1
					if(i >= len(tab)):
						break
					nbBitEnPlus = 8 - nbBitRestant
					
					octet1 = octet << nbBitEnPlus
					octet2 = tab[i] >> (8-nbBitEnPlus)
					n = octet1 or octet2
					nbBitRestant = 8-nbBitEnPlus

				#Recupere le b
				if(i >= len(tab)):
					break
				if nbBitRestant == 3:
					b = tab[i]
					nbBitRestant = 8
				elif nbBitRestant > 3:
					octetUnCompress = tab[i] >> nbBitRestant-3
					nbBitRestant = nbBitRestant-3
				else:
					octet = tab[i]
					i+=1
					if(i >= len(tab)):
						break
					nbBitEnPlus = 3 - nbBitRestant
					
					octet1 = octet << nbBitEnPlus
					octet2 = tab[i] >> (8-nbBitEnPlus)
					b = octet1 or octet2
					nbBitRestant = 8-nbBitEnPlus

			
			else:
				#traitement des octets de la sequence
			
				#garde que les bits non traites de l'octet
				octet = tab[i] and ((2^nbBitRestant)-1)
				if nbBitRestant == b:
					octetUnCompress = octet
					nbBitRestant = 8
				elif nbBitRestant > b:
					octetUnCompress = octet >> nbBitRestant-b
					nbBitRestant = nbBitRestant-b
				else:
					i+=1
					if(i >= len(tab)):
						break
					
					nbBitEnPlus = b - nbBitRestant
					
					octet1 = octet << nbBitEnPlus
					octet2 = tab[i] >> (8-nbBitEnPlus)
					octetUnCompress = octet1 or octet2
					nbBitRestant = 8-nbBitEnPlus
			
				result.append(octetUnCompress)
				n -=1
			i +=1
			
		print "decompression terminee"
		print "creation du fichier decompresse"
		self.binaire.createUnCompressFile(self.filePath ,result)
		print "votre fichier est disponible"
        
    def shouldWeCompressTheFile(self):
        listCutFile = self.filePath.split('.')
        length = len(listCutFile)
        if listCutFile[length-1] == 'seg':
            return False
        else:
            return True
        
filePath = sys.argv[1]
print filePath
compression = Compression(filePath)
if(compression.shouldWeCompressTheFile()):
    compression.c()
else:
    compression.uncompresse()    
    
    
    
    
