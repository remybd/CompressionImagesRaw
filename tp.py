# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:06:40 2015

@author: rémy
"""
import math
NBB = 8
nbbi = 8

def open_file(file_name):

    imageIni = []
    f = open(file_name, "rb")
    try:
        i = 0
        byte = f.read(1)
        while byte != b"":
            imageIni[i] = byte
            i += 1
            byte = f.read(1)
    
    finally:
        f.close()

    return imageIni


#functions use by the recursiv algorithme
def where_the_value_start(byte):
    return math.ceil(math.log(byte,2))
    
    
def delete_0_in_start_of_bit_string(string,start):
    return string[2+(NBB-start):] #on enlève le 2b et les premiers 0
    
    
    
def create_new_sequence(byte,imageFinal,nbbi):
    length = len(imageFinal)
    stringPixel = delete_0_in_start_of_bit_string(bin(byte),nbbi) #convertit l'entier byte en bites
    
    #écrit le pixel en binaire à l'enver
    for i in range(NBB):
        imageFinal[length] = stringPixel[NBB-1-i]
        length += 1
    
    #début de l'entête à l'enver
    #écrit la taille des pixels de la séquence à l'enver
    stringNumberOfBites = bin(nbbi)[2+(3-where_the_value_start(nbbi)):]
    for i in range(3):
        imageFinal[length] = stringNumberOfBites[3-1-i]
        length += 1
    
    #écrit la taille de la séquence à l'envers
    stringNumberOfPixels = bin(n)[2+(11-where_the_value_start(nbbi)):]
    for i in range(11):
        imageFinal[length] = stringNumberOfPixels[11-1-i]
        length += 1
        
    return imageFinal;
    
    
def refactor_sequence(byte,imageFinal,nbbi,tailleSeq):
    
    return imageFinal;
    
    
def insert_in_sequence(byte,imageFinal,nbbi):
    length = len(imageFinal)
    stringPixel = delete_0_in_start_of_bit_string(bin(byte),nbbi) #convertit l'entier byte en bites
    
    for i in range(NBB):
        imageFinal[length] = stringPixel[NBB-1-i]
        length += 1
    return imageFinal



#c(i) : coût en nombre de bits entre i et m^2
#b : nombre de bits d’un pixel dans la séquence courante
#i : pixel numéro i
#n : la taille de la séquence courante
#nbbi : nombre de bits du pixel i réduit
#NBB : nombre de bits initial par pixel : 8
#condition d’arret : i = (m^2) +1 => c(i) = 0
#imageFinal : tableau de bites contenant l'image finale
#imageIni : tableau d'octet contenant l'image au format raw

def cout_recursif(i, imageIni, n, b):
    m = len(imageIni)
    imageFinal = [];
    
    if(i >= m^2 +1):
        return 0
    else:
        pixel = imageIni[i]
        nbbi = where_the_value_start(pixel)
        createNewSequence = 11 + nbbi + cout_recursif(i+1, imageIni, 1, nbbi)
        
        if(n > 255 or n <= 0):
            res = createNewSequence
        else:
            putDirectInSequence = b + cout_recursif(i+1, imageIni, n+1, b)
            
            if(nbbi < b):
                if(putDirectInSequence < createNewSequence):
                    res = putDirectInSequence
                    imageFinal = insert_in_sequence(pixel,imageFinal,nbbi)
                else:
                    res = createNewSequence
                    imageFinal = create_new_sequence(pixel,imageFinal,nbbi)

            else:
                modifSequence = n*(nbbi - b) + nbbi + cout_recursif(i+1, imageIni, n+1, nbbi)
                
                if(putDirectInSequence <= modifSequence and putDirectInSequence <= createNewSequence):
                    res = putDirectInSequence
                elif(modifSequence <= putDirectInSequence and modifSequence <= createNewSequence):
                    res = modifSequence
                else:
                    res = createNewSequence
                
        return res
                
                
    
    
    