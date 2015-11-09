import java.util.Objects;

/**
 * Created by rémy on 08/11/2015.
 */
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
        return this.n == (((HeaderSequence)(obj)).getN()) && this.b == (((HeaderSequence)(obj)).getB());
    }
}
