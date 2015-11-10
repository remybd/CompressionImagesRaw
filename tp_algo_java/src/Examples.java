import java.util.ArrayList;

/**
 * Created by rémy on 10/11/2015.
 */
public class Examples {

    //tableau de 16 cases avec chaque case à 7 bits significatifs
    //taille initiale : 16 * 8 = 128
    //taille finale : 7*16 + 11 = 123
    private static byte exemple1[] = {(byte)-1,(byte)-1,(byte)-1,(byte)-1,
                            (byte)-1,(byte)-1,(byte)-1,(byte)-1,
                            (byte)-1,(byte)-1,(byte)-1,(byte)-1,
                            (byte)-1,(byte)-1,(byte)-1,(byte)-1};


    //tableau de 300 cases avec chaque case à 7 bits significatifs
    //taille initiale : 300 * 8 = 2400
    //taille finale : 7*300 + 2*11 = 2122
    private static byte[] exemple2(){
        byte[] tab = new byte[300];

        for(int i =0; i < 300; i++){
            tab[i] = (byte)-1;
        }
        return tab;
    }

    //tableau de 16 cases avec chaque case à 7 bits significatifs sauf la 6ème à 6
    //taille initiale : 16 * 8 = 128
    //taille finale :
    private static byte exemple3[] = {(byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)-65,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-1,(byte)-1};


    //tableau de 16 cases avec chaque case à 7 bits significatifs sauf la 6ème à 8
    //taille initiale : 16 * 8 = 128
    //taille finale :
    private static byte exemple4[] = {(byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)2,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-1,(byte)-1};


    //tableau de 16 cases avec chaque case à 7 bits significatifs sauf la 6ème et l'avant dernière à 6
    //taille initiale : 16 * 8 = 128
    //taille finale :
    private static byte exemple5[] = {(byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)-65,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-1,(byte)-1,
            (byte)-1,(byte)-1,(byte)-65,(byte)-1};



    public static byte[][] tabExemple = {exemple1, exemple2(), exemple3, exemple4, exemple5};

}

