import struct
import math

class GestionBinaire:

    def __init__(self):
        self.tab = []
    
    def readFile(self, fileName):
        tab = []
        
        with open(fileName,'rb') as image:
            octet = image.read(1)
            while octet :
                tab.append(octet)
                octet = image.read(1)
        
        self.tab = self.linearise(tab)        
        
    def linearise(self, tab):
        
        tabLin = []

        m = int(math.sqrt(len(tab)))
        i = 0
        while i < m :
            for j in range(0, m):
                tabLin.append(tab[j+(i*m)])
            i = i+1
            
            if i < m :
                for j in range(0, m):
                    tabLin.append(tab[((i+1)*m-1)-j])
                i = i+1

        return tabLin
                
    def nbBits(self, pixel):                
        return len(bin(struct.unpack('<B', pixel)[0])) - 2
    
    def addNumberToBinary(self, octet, number):
        octet = struct.unpack('<B', octet)[0] + number
        octet = struct.pack('<B', octet)
        return octet
        
    def getPixels(self):
        return self.tab
    
    def getTaille(self):
        return int(math.sqrt(len(self.tab)))

    #return 16 bits header (just cut the 5th last bits for a 11 bit header)
    # TO CHECK that function works
    def createHeaderSequence(self, n, b):
        print('CARE OF THIS FUNCTION RESULT')
        header = n << (8-n)
        header = header << 3
        header = header + b
        header = header << 5
        header = struct.pack('<H',header)
        return header
    
    #return n on 8 bits
    def createNHeader(self, n):
        header = struct.pack('<B',n)
        return header
    
    #return b on 8 bits (ex : b = 3, return 01100000) 
    def createBHeader(self, b) :
        header = 0
        header = header << 3
        header = header + b
        header = header << 5
        return header
    
gb = GestionBinaire()
gb.readFile('images/images/Baboon.raw')
tab = gb.getPixels()
#gb.addNumberToBinary(tab[0], 1)
#gb.createHeaderSequence(1,3)