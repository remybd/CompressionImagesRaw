import struct

#tableau de valeurs
tab=[]

with open('images/images/Baboon.raw','rb') as image:
    octet = image.read(1)
    while octet :
#        tab.append(bin(struct.unpack('<B', octet)[0]))
        tab.append(octet)
        octet = image.read(1)
    
#print("0x%x" % int(tab[0], 2))
#print(tab[1])
#print(dec2bin(struct.unpack('<B', tab[1])[0]))

print(bin(struct.unpack('<B', tab[1])[0]))
print(len(bin(struct.unpack('<B', tab[1])[0])) - 2)

class Compression:
    
    def __init__(self, taille, data):
        # Taille de l'image carre en largeur/longueur
        self.m = taille
        
        # Tableau linearise
        self.tab = data
        
        # Tableau memoisation
        self.memCout = []
        self.memIteration = []
        
    def initMem(self):
        for i in range(0,(self.m**2)):
            self.memCout[i] = -1
            self.memIteration[i] = -1
        
    
    
    def cout(self, i, n, nbBitsSequence):
               
        # On a deja parcouru cette arbre
        if self.memIteration[i] != -1 and self.memIteration[i].hasKey((n,nbBitSequence)) :
            return self.memIteration[i].get((n,nbBitsSequence))

        if self.memIteration[i] == -1 :
            self.memIteration[i].dict()
        
        # Condition d'arret
        if (self.m**2) == i :
            self.memIteration[i][n,nbBitsSequence] = 0
        else :
            aj = self.nbBits(i)

            # Si la sequence est rempli ou qu’il n’y en a pas :
            elif n == 0 or n >= 255 :
                self.memIteration[i][n,nbBitsSequence] = self.cout(i+1, 1, aj) + 11 + aj

            # Si le pixel est parfait pour la sequence :
            elif nbBitsSequence == aj:
                self.memIteration[i][n,nbBitsSequence] = aj + self.cout(i+1, n+1, aj)

            # Si le pixel est plus petit : 
            elif nbBitsSequence > aj:

                garde = self.cout(i+1, n+1, nbBitsSequence) + nbBitsSequence
                ferme = self.cout(i+1, 1, aj) + aj + 11
                self.memIteration[i][n,nbBitsSequence] = min(garde, ferme)

            # Si le pixel est plus grand :
            else :

                garde = self.cout(i+1, n+1, aj) + aj + (n-1)*(aj-nbBitsSequence)
                ferme = self.cout(i+1, 1, aj) + aj + 11
                self.memIteration[i][n,nbBitsSequence] = min(garde, ferme)

        if self.memCout[i] == -1 or self.memIteration[i][n,nbBitsSequence] < self.memCout[i] :
            self.memCout[i] = self.memIteration[i][n,nbBitsSequence]
        
#     def cout(self, i, n, nbBitsSequence):
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
#        if nbBitsSequence == aj:
#            return aj + self.cout(i+1, n+1, aj)
#
#        # Si le pixel est plus petit : 
#        if nbBitsSequence > aj:
#
#            garde = self.cout(i+1, n+1, nbBitsSequence) + nbBitsSequence
#            ferme = self.cout(i+1, 1, aj) + aj + 11
#            return min(garde, ferme)
#
#        # Si le pixel est plus grand :
#        else :
#
#            garde = self.cout(i+1, n+1, aj) + aj + (n-1)*(aj-nbBitsSequence)
#            ferme = self.cout(i+1, 1, aj) + aj + 11
#            return min(garde, ferme)