import java.math.BigInteger;
import java.util.*;

public class factorize {
    public static void main(String[] args) {
        task2();
    }
    
    static void task1() {
        BigInteger N = new BigInteger("179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581");
        BigInteger A = sqrt(N).add(BigInteger.ONE);
        BigInteger x = sqrt(A.multiply(A).subtract(N));
        System.out.println(A.subtract(x));
	}

    static void task2() {
        BigInteger N = new BigInteger("648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877");
        BigInteger A = sqrt(N).add(BigInteger.ONE);
        BigInteger two = new BigInteger("2");
        BigInteger lim = A.add(two.pow(20));
        for (; A.compareTo(lim) == -1; A = A.add(two)) {
            BigInteger aMinusN = A.multiply(A).subtract(N);
            BigInteger x = sqrt(A.multiply(A).subtract(N));
            System.out.println("x = ");
            System.out.println(x);
            if (x.multiply(x).compareTo(aMinusN) != 0) {
                continue;
            }
            BigInteger p = A.subtract(x);
            BigInteger q = A.add(x);
            System.out.println("testing");
            System.out.println(p);
            if (!p.isProbablePrime(100) || !q.isProbablePrime(100)) {
                continue;
            }
            if (p.multiply(q).compareTo(N) == 0) {
                System.out.println(p);
                return;
            }
        }       
    }

    static void initPows(BigInteger value) {
        if (myPows.isEmpty()) {
            myPows.add(BigInteger.ONE);
        }
        
        BigInteger two = new BigInteger("2");
        BigInteger lim = myPows.get(myPows.size() - 1);
        while (lim.multiply(lim).compareTo(value) == -1) {
            lim = lim.multiply(two);
            myPows.add(lim); 
        }
    }

    static BigInteger sqrt(BigInteger value) {
        initPows(value);
        int i = myPows.size() - 1;
        while (myPows.get(i).multiply(myPows.get(i)).compareTo(value) == 1) {
            i--;
        }
        BigInteger sq = BigInteger.ZERO;
        while (i >= 0) {
            BigInteger nextSq = sq.add(myPows.get(i));
            if (nextSq.multiply(nextSq).compareTo(value) == 0) {
                return nextSq;
            }
            if (nextSq.multiply(nextSq).compareTo(value) == -1) {
                sq = nextSq;
            }
            i--;
        }
        return sq;
    }

    static List<BigInteger> myPows = new ArrayList<BigInteger>();
}
