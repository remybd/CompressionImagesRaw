/**
 * Created by rémy on 09/11/2015.
 */
public class Main {
    public static void main(String[] args) {
        Compression c = new Compression("../Florent/images/images/Baboon.raw");
        System.out.println("taille image au debut : " + c.getM());
        System.out.println("nb max d'iterations : " + c.getM() * 8 * 255 );
//        int cout = c.c_recursif();
        int cout = c.c_iteratif();
        System.out.println("taille image apres compression : " + cout);
    }
}
