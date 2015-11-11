import java.io.*;
import java.util.ArrayList;

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
            this.tabLinearise=tab;
//            this.linearise();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public void linearise(){
    	ArrayList<Byte> tabLin = new ArrayList<>();
        int taille = (int)Math.sqrt(this.getTaille());
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
                		
    public static int nbBits(Byte pixel){
        Double v = pixel.doubleValue()+128;
        Double value = Math.floor(Math.log(v) / Math.log(2));
        return value.intValue()+1;
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

    public ArrayList<Byte> createFinalArray (String s){
        int nbByte = s.length() / 8;
        int lastByteToComplete = s.length() % 8;
        ArrayList<Byte> result = new ArrayList<Byte>();

        int start = 0;
        int fin = 0;
        String octet;
        for(int i =0; i < nbByte; i++){
            start = i*8;
            fin = (i+1)*8;
            octet = s.substring(start,fin);
            result.add(new Byte(Byte.parseByte(octet,2)));
        }

        return result;
    }
}
