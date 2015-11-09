import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by rémy on 08/11/2015.
 */


public class Compression {
    private int m;
    private ArrayList<Byte> tab;
    private Binaire binaire;
    private ArrayList<HashMap<HeaderSequence,Integer>> memIteration;
    private ArrayList<Integer> memCout;

    int cpt = 0;

    public  Compression(String fichier){
        this.binaire = new Binaire(fichier);

        this.m = binaire.getTaille();
        this.tab = binaire.getPixels();
        this.memIteration = new ArrayList<HashMap<HeaderSequence,Integer>>();
        this.memCout = new ArrayList<Integer>();

        for(int i =0; i <= m; i++){
            memCout.add(Integer.MAX_VALUE);
            memIteration.add(new HashMap<HeaderSequence,Integer>());
            memoisation.add(null);
        }
    }


    public int c(){
        return coutV2(m-1);
    }

    public int cout(int i, int n, int b){
        HeaderSequence h = new HeaderSequence(n,b);

        //on a deja parcouru cet arbre
        if(memIteration.get(i).containsKey(h)){
            //System.out.println(memIteration.get(i));
            return memIteration.get(i).get(h);
        }

        //condition d'arret
        if(m <= i) {
            memIteration.get(i).put(h, 0);
            //System.out.println("fin " + b  + "   " + n);
        }
        else{
            int aj = binaire.nbBits(tab.get(i));

            //si la séquence est remplie ou qu'il n'y en a pas :
            if(n == 0 || n >= 255){
                memIteration.get(i).put(h, new Integer(cout(i + 1, 1, aj) + 11 + aj));
            }
            //si le pixel est parfait pour la séquence :
            else if(b == aj){
                memIteration.get(i).put(h, new Integer(cout(i + 1, n + 1, aj) + aj));
            }
            //si le pixel est plus petit :
            else if(b > aj){
                int garde = cout(i+1, n+1, b) + b;
                int ferme = cout(i+1, 1, aj) + 11 + aj;
                memIteration.get(i).put(h, new Integer(Math.min(garde, ferme)));
            }
            //si le pixel est plus grand :
            else{
                int garde = cout(i+1, n+1, aj) + aj + (n-1)*(aj-b);
                int ferme = cout(i+1, 1, aj) + 11 + aj;
                memIteration.get(i).put(h, new Integer(Math.min(garde, ferme)));
            }
        }

        return memIteration.get(i).get(h);
    }


    private ArrayList<Integer> memoisation = new ArrayList<Integer>();

    public int coutV2(int i){

        if(memoisation.get(i) != null){
            return memoisation.get(i);
        }
        //condition d'arret
        if(i <= 0) {
            memoisation.set(i,0);
        }
        else{
            int aj = binaire.nbBits(tab.get(i));


            int val = 0;
            int min = Integer.MAX_VALUE;
            for(int j = 1; j <= i ; j++){
                for(int n = 0; n < 256; n++){
                    val = coutV2(i-j) + n*Math.max(aj,binaire.nbBits(tab.get(i-j+1))) ;
                    if(val < min)
                        min = val;
                }
            }
            memoisation.set(i,min + 11);
        }

        return memoisation.get(i);
    }


    public int getM(){
        return m;
    }


    /*
        public int cout(int i, int n, int b){
        HeaderSequence h = new HeaderSequence(n,b);

        //on a deja parcouru cet arbre
        if(memIteration.get(i) != null && memIteration.get(i).containsKey(h)){
            return memIteration.get(i).get(h);
        }

        HashMap<HeaderSequence,Integer> value;
        if(memIteration.get(i) != null)
            value = memIteration.get(i);
        else{
            value = new HashMap<HeaderSequence,Integer>();
            memIteration.set(i, value);
        }

        //condition d'arret
        if(m <= i) {
            value.put(h, new Integer(0));
        }
        else{
            int aj = binaire.nbBits(tab.get(i));

            //si la séquence est remplie ou qu'il n'y en a pas :
            if(n == 0 || n >= 255){
                value.put(h, new Integer(cout(i+1, 1, aj) + 11 + aj));
            }
            //si le pixel est parfait pour la séquence :
            else if(b == aj){
                    value.put(h, new Integer(cout(i+1, n+1, aj) + aj));
            }
            //si le pixel est plus petit :
            else if(b > aj){
                int garde = cout(i+1, n+1, b) + b;
                int ferme = cout(i+1, 1, aj) + 11 + aj;
                value.put(h, new Integer(Math.min(garde,ferme)));
            }
            //si le pixel est plsu grand :
            else{
                int garde = cout(i+1, n+1, aj) + aj + (n-1)*(aj-b);
                int ferme = cout(i+1, 1, aj) + 11 + aj;
                value.put(h, new Integer(Math.min(garde,ferme)));
            }
        }
         */
}
