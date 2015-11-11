
public class Main {
    public static void main(String[] args) {
        //Compression c = new Compression("../Florent/images/images/Baboon.raw");
        TryRebuild t = new TryRebuild("../Florent/images/images/Baboon.raw");
        System.out.println("taille image au debut : " + t.getM());
        System.out.println("nb max d'iterations : " + t.getM() * 8 * 255 );
        int cout = t.coutRecursif();
//      int cout = c.c_recursif();
//        int cout = c.c_iteratif();

        System.out.println("taille image apres compression : " + cout + " bites soit : " + cout/8 + " octets" );
    }
}
