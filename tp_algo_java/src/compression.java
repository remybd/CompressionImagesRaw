import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by rémy on 08/11/2015.
 */
public class Compression {
    private int m;
    private Byte tab[];
    private Binaire binaire;
    private ArrayList<HashMap<HeaderSequence,Integer>> memIteration;
    private ArrayList<Integer> memCout;

    public void init(String fichier){
        this.binaire = new Binaire();
        binaire.readFile(fichier);

        this.m = binaire.getTaille();
        this.tab = binaire.getPixels();
        this.memIteration = new ArrayList<HashMap<HeaderSequence,Integer>>();
        this.memCout = new ArrayList<Integer>();
    }


    public int c(){
        return cout(0,0,0);
    }

    public int cout(int i, int n, int b){
        HeaderSequence h = new HeaderSequence(n,b);

        //on deja parcouru cet arbre
        if(!memIteration.get(i).isEmpty()){
            return memIteration.get(i).get(new HeaderSequence(n,b));
        }

        HashMap<HeaderSequence,Integer> value = new HashMap<HeaderSequence,Integer>();
        //condition d'arret
        if(m*m == i) {
            value.put(h, new Integer(0));
        }
        else{
            int aj = binaire.nbBits(tab[i]);

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

        if(!(memCout.get(i) != null) && memCout.get(i).intValue() < value.get(h).intValue()){
            memCout.set(i, value.get(h));
        }

        memIteration.set(i, value);
        return memIteration.get(i).get(h);
    }
    
}
