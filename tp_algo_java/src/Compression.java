import java.util.ArrayList;
import java.util.HashMap;

public class Compression {
    private int m;
    private ArrayList<Byte> tab;
    private Binaire binaire;
    private ArrayList<HashMap<HeaderSequence,Integer>> memIteration;
    private ArrayList<Integer> memCout;
    private ArrayList<Integer> memSignificatif;

    int cpt = 0;

    public Compression(String fichier){
        this.binaire = new Binaire(fichier);

        this.m = binaire.getTaille();
        this.tab = binaire.getPixels();
        this.memIteration = new ArrayList<HashMap<HeaderSequence,Integer>>();
        this.memCout = new ArrayList<Integer>();
        this.memSignificatif = new ArrayList<Integer>();
        this.initMemorisation();
    }

    private void initMemorisation(){
    	memCout.clear();
    	memIteration.clear();
        memSignificatif.clear();

        memCout.add(Integer.MAX_VALUE);
        memIteration.add(new HashMap<HeaderSequence,Integer>());
        for(int i =0; i < m; i++){
            memCout.add(Integer.MAX_VALUE);
            memIteration.add(new HashMap<HeaderSequence,Integer>());
            memSignificatif.add(binaire.nbBits(tab.get(i)));
        }
    }

    public int c_recursif(){
    	this.initMemorisation();
        return cout_recursif(0,0,0);
    }

    private int cout_recursif(int i, int n, int b){
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
            int aj = memSignificatif.get(i);

            //si la séquence est remplie ou qu'il n'y en a pas :
            if(n == 0 || n >= 255){
                memIteration.get(i).put(h, new Integer(cout_recursif(i + 1, 1, aj) + 11 + aj));
            }
            //si le pixel est parfait pour la séquence :
            else if(b == aj){
                memIteration.get(i).put(h, new Integer(cout_recursif(i + 1, n + 1, aj) + aj));
            }
            //si le pixel est plus petit :
            else if(b > aj){
                int garde = cout_recursif(i+1, n+1, b) + b;
                int ferme = cout_recursif(i+1, 1, aj) + 11 + aj;
                memIteration.get(i).put(h, new Integer(Math.min(garde, ferme)));
            }
            //si le pixel est plus grand :
            else{
                int garde = cout_recursif(i+1, n+1, aj) + aj + (n-1)*(aj-b);
                int ferme = cout_recursif(i+1, 1, aj) + 11 + aj;
                memIteration.get(i).put(h, new Integer(Math.min(garde, ferme)));
            }
        }

        return memIteration.get(i).get(h);
    }
    
    public int c_iteratif(){
    	return cout_iteratif();
    }


    private int cout_iteratif() {
    	
    	this.memCout.set(this.m, 0);
    	this.memIteration.get(this.m).put(new HeaderSequence(0, 0), 0);
    	
    	for(int i=this.m-1; i>-1; i--){
    		HashMap<HeaderSequence,Integer> precedents = this.memIteration.get(i+1);
    		int a = memSignificatif.get(i);
    		
    		for (HeaderSequence k : precedents.keySet()){
    			int n = k.getN();
    			int b = k.getB();
    			int coutPrec = precedents.get(k);
    			
    			if ( n>=255 || n==0){
    				int newCout = coutPrec + 11 + a;
                    int newB = a;
                    int newN = 1;
                    
                    HeaderSequence h = new HeaderSequence(newN, newB);
                    if (this.memIteration.get(i).containsKey(h))
                        this.memIteration.get(i).put(h,Math.min(this.memIteration.get(i).get(h),newCout));
                    else
                        this.memIteration.get(i).put(h,newCout); 
    			}
    			else if(a == b){
    			    int newCout = coutPrec + a;
                    int newB = a;
                    int newN = n + 1;
                    
                    HeaderSequence h = new HeaderSequence(newN, newB);
                    if (this.memIteration.get(i).containsKey(h))
                        this.memIteration.get(i).put(h,Math.min(this.memIteration.get(i).get(h),newCout));
                    else
                        this.memIteration.get(i).put(h,newCout); 

    			}
    			else{
    				if (a<b){
    					int garde = coutPrec + b;
    					int ferme = coutPrec + a + 11;

    					int newCoutGarde = garde;
    					int newBGarde = b;
    					int newNGarde = n + 1;
    					int newCoutFerme = ferme;
    					int newBFerme = a;
    					int newNFerme = 1;
    					
    					HeaderSequence hGarde = new HeaderSequence(newNGarde, newBGarde);
    					HeaderSequence hFerme = new HeaderSequence(newNFerme, newBFerme);
    					
    					if (this.memIteration.get(i).containsKey(hGarde))
                            this.memIteration.get(i).put(hGarde,Math.min(this.memIteration.get(i).get(hGarde), newCoutGarde));
                        else
                            this.memIteration.get(i).put(hGarde, newCoutGarde);

                        if (this.memIteration.get(i).containsKey(hFerme))
                        	this.memIteration.get(i).put(hFerme,Math.min(this.memIteration.get(i).get(hFerme), newCoutFerme));
                        else
                        	this.memIteration.get(i).put(hFerme, newCoutFerme);
    				}
    				else if (a>b){
    					int garde = coutPrec + a + n*(a-b);
						int ferme = coutPrec + a + 11;

						int newCoutGarde = garde; 
						int newBGarde = a;
						int newNGarde = n + 1;
						int newCoutFerme = ferme;
						int newBFerme = a;
						int newNFerme = 1;
                        
                        HeaderSequence hGarde = new HeaderSequence(newNGarde, newBGarde);
    					HeaderSequence hFerme = new HeaderSequence(newNFerme, newBFerme);
    					
    					if (this.memIteration.get(i).containsKey(hGarde))
                            this.memIteration.get(i).put(hGarde,Math.min(this.memIteration.get(i).get(hGarde), newCoutGarde));
                        else
                            this.memIteration.get(i).put(hGarde, newCoutGarde);

                        if (this.memIteration.get(i).containsKey(hFerme))
                        	this.memIteration.get(i).put(hFerme,Math.min(this.memIteration.get(i).get(hFerme), newCoutFerme));
                        else
                        	this.memIteration.get(i).put(hFerme, newCoutFerme);
    					
    				}
    			}
                         
    		}
    		this.setMinimumPixel(i);
    	}
    	
		return this.memCout.get(0);
	}

	private void setMinimumPixel(int i) {
		Integer minvalue = Integer.MAX_VALUE;
		
		for (Integer value : this.memIteration.get(i).values()){
			if (minvalue > value){
				minvalue = value;
			}
		}
		
		this.memCout.set(i, minvalue.intValue());
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
