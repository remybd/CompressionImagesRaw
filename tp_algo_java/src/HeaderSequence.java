/**
 * Created by rémy on 08/11/2015.
 */
public class HeaderSequence {
    private int n;
    private int b;

    public HeaderSequence(int n, int b){
        this.n = n;
        this.b = b;
    }

    public int getN() {
        return n;
    }

    public int getB() {
        return b;
    }

    public boolean equals(HeaderSequence h){
        return this.n == h.getN() && this.b == h.getB();
    }
}
