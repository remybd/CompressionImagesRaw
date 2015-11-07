import struct

class GestionBinaire:

    def __init__(self):
        self.tab = []
    
    def readFile(self, fileName):
        self.tab = []
        with open(fileName,'rb') as image:
            octet = image.read(1)
            while octet :
                self.tab.append(octet)
                octet = image.read(1)

    def nbBits(self, pixel):                
        return len(bin(struct.unpack('<B', pixel)[0])) - 2
    
    def addNumberToBinary(self, octet, number):
        octet = struct.unpack('<B', octet)[0] + number
        octet = struct.pack('<B', octet)
        return octet
        
    def getPixels(self):
        return self.tab

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
        header = header << 3
        header = header + b
        header = header << 5
        return header
    
    
gb = GestionBinaire()
gb.readFile('images/images/Baboon.raw')
tab = gb.getPixels()
#gb.addNumberToBinary(tab[0], 1)
#gb.createHeaderSequence(1,3)