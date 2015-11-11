import java.util.ArrayList;
import java.util.HashMap;

public class TryRebuild {
    private Binaire binaire;
    private int m;
    private ArrayList<Integer> memBitsSignificatifs;
    private HashMap<String,Integer> memIteration;

    private int cpt = 0;

    public TryRebuild(String fichier){
        this.binaire = new Binaire(fichier);

        this.m = binaire.getTaille();
        this.memIteration = new HashMap<String,Integer>();

        this.memBitsSignificatifs = new ArrayList<Integer>();
        ArrayList<Byte> tab = binaire.getPixels();
        for(int i =0; i < m; i++){
            memBitsSignificatifs.add(binaire.nbBits(tab.get(i)));
        }
    }

    public TryRebuild(int numExemple){

        this.memIteration = new HashMap<String,Integer>();

        byte[] tab = Examples.tabExemple[numExemple-1];
        this.m = tab.length;

        this.memBitsSignificatifs = new ArrayList<Integer>();
        for(int i =0; i < m; i++){
            memBitsSignificatifs.add(Binaire.nbBits(tab[i]));
        }
    }

    public int coutRecursif(){
        System.out.println("debut recursion");
        int cout =  cRecursif(0,0,0);
        System.out.println("fin recursion");
        System.out.println("nombre de fois que l'on fait les vrai calculs : " + cpt);
        return cout;
    }


    private int cRecursif(int i, int n, int b){

        if(memIteration.get(i + "." + n + "." + b) == null){
            cpt ++;//compte le nombre de fois que l'on fait les vrai calculs

            //condition d'arret
            if(i >= m){
                memIteration.put(i + "." + n + "." + b,0);
            } else {
                int cout;

                //si la séquence est remplie ou qu'il n'y en a pas :
                if(n == 0 || n > 255){
                    cout = 11 + memBitsSignificatifs.get(i) + cRecursif(i+1, 1, memBitsSignificatifs.get(i));
                }
                //si le pixel est parfait pour la séquence :
                else if(b == memBitsSignificatifs.get(i)){
                    cout = b + cRecursif(i+1, n+1, b);
                }
                //si le pixel est plus petit :
                else if(b > memBitsSignificatifs.get(i)){
                    int garde = b + cRecursif(i+1, n+1, b);
                    int ferme = 11 + memBitsSignificatifs.get(i) + cRecursif(i+1, 1, memBitsSignificatifs.get(i));
                    cout = Math.min(garde,ferme);
                }
                //si le pixel est plus grand :
                else{
                    int garde = n*(memBitsSignificatifs.get(i)-b) + memBitsSignificatifs.get(i) + cRecursif(i+1, n+1, memBitsSignificatifs.get(i));
                    int ferme = 11 + memBitsSignificatifs.get(i) + cRecursif(i+1, 1, memBitsSignificatifs.get(i));
                    cout = Math.min(garde,ferme);
                }

                memIteration.put(i + "." + n + "." + b,cout);
            }
        }

        return memIteration.get(i + "." + n + "." + b);
    }

    public int getM(){
        return m;
    }
}
