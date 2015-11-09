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
        }
    }


    public int c(){
        return cout(0,0,0);
    }

    public int cout(int i, int n, int b){
        HeaderSequence h = new HeaderSequence(n,b);

        //on a deja parcouru cet arbre
        if(memIteration.get(i).containsKey(h)){
            //System.out.println(memIteration.get(i));
            return memIteration.get(i).get(h);
        }

        cpt++;
        if(cpt >= m * 8 * 255)
            System.out.println("STOPPPPPPPPPPPPPPPP cpt");

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
