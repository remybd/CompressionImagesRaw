import java.util.Objects;

public class HeaderSequence {
    private int n;
    private int b;

    public HeaderSequence(int n, int b){
        super();
        this.n = n;
        this.b = b;
    }

    public int getN() {
        return n;
    }

    public int getB() {
        return b;
    }

    @Override
    public boolean equals(Object obj) {
        HeaderSequence h = (HeaderSequence)obj;
        return (this.n == h.getN()) && (this.b == h.getB());
    }

    @Override
    public int hashCode() {
        int result = n;
        result = 255 * result + b;
        return result;
    }
}
