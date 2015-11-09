import java.io.*;
import java.util.ArrayList;

/**
 * Created by rémy on 08/11/2015.
 */
public class Binaire {
    private ArrayList<Byte> tab;
    private ArrayList<Byte> tabLinearise;

    public Binaire(String fileName){
        super();
        tab = new ArrayList<Byte>();
        try {
            File file = new File(fileName);
            DataInputStream r = new DataInputStream(new BufferedInputStream (new FileInputStream(file)));

            double lengthLine = Math.sqrt(file.length());

            for(int i = 0; i < lengthLine; i++){
                for(int j = 0; j < lengthLine; j++){
                    tab.add(r.readByte());
                }
            }

            r.close();
            
            this.linearise();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public void linearise(){
    	ArrayList<Byte> tabLin = new ArrayList<>();
        int taille = this.getTaille();
        int i = 0;
        
        while (i < taille){
        	for (int j=0;j<taille; j++){
                tabLin.add(tab.get(j+(i*taille)));
	            i = i+1;
	            
	            if (i < taille) {
	            	for (j=0;j<taille; j++)
	                    tabLin.add(tab.get(((i+1)*taille-1)-j));
	                i = i+1;	
	            }                
        	}
        }
            
        this.tabLinearise=tabLin;
    }
                		
    public int nbBits(Byte pixel){
        Double v = pixel.doubleValue()+128;

        Double value = Math.floor(Math.log(v) / Math.log(2));
        return value.intValue();
    }

    public Byte addNumberToBinary(Byte octect, int number){
        Integer value =  (octect.intValue() + number);
        return value.byteValue();
    }

    public ArrayList<Byte> getPixels(){
        return tabLinearise;
    }

    public int getTaille(){
        return tab.size();
    }

    public Byte[] createHeader(HeaderSequence headerSequence){
        Byte[] header = new Byte[2];
        header [0] = new Integer(headerSequence.getN()).byteValue();
        header[1] = new Integer(headerSequence.getB()).byteValue();

        return header;
    }
}
