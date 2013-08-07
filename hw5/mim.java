import java.math.BigInteger;
import java.util.*;

public class mim {
    
    public static void main(String[] args) {
        BigInteger bi1 = new BigInteger("11");
        /*BigInteger h = new BigInteger("3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333");
        BigInteger g = new BigInteger("11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568");
        BigInteger p = new BigInteger("13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171");
        */
        BigInteger h = new BigInteger("16");
        BigInteger x = new BigInteger("12");
        BigInteger g = new BigInteger("16");
        BigInteger p = new BigInteger("8796093022207");
        /*System.out.println("hello");
        System.out.println(bi1);
        System.out.println(extEuclidean(new BigInteger("120"), new BigInteger("23")));
        */
        Map<BigInteger, BigInteger> hToX1Map = new TreeMap<BigInteger, BigInteger>();
        BigInteger limit = new BigInteger("2");
        limit = limit.pow(20);
        BigInteger one = new BigInteger("1");
        BigInteger x1 = one;
        long mapSize = 0;
        BigInteger key;
        while (x1.compareTo(limit) == -1) {
            //BigInteger key = h.modPow(x1.modInverse(p), p);
            try {
                x1 = x1.add(one);
                key = h.multiply(g.modPow(x1.modInverse(p), p)).mod(p);
                hToX1Map.put(key, x1);
                if (hToX1Map.size() - mapSize == 1000) {
                    mapSize = hToX1Map.size();
                    System.out.println(mapSize);
                    System.out.println(key);
                }
            } catch(java.lang.ArithmeticException ex) {
            } finally {
            }
        }
        System.out.println("hash created");
        long counter = 0;
        BigInteger x2 = new BigInteger("2");
        BigInteger gPowB = g.modPow(new BigInteger("20"), p);
        key = gPowB;
        while (x2.compareTo(limit) == -1) {
            key = key.multiply(gPowB).mod(p);//h.modPow(x2, p);
            if (hToX1Map.containsKey(key)) {
                System.out.println("x = ");
                x = x2.multiply(hToX1Map.get(key));
                System.out.println(x);
                System.out.println(g.modPow(x, p));
                return;
            }
            x2 = x2.add(one);
            
            counter += 1;
            if (counter % 100000 == 0) {
                System.out.println(counter);
            }
        }
    }
    
    /*private static Pair<BigInteger, BigInteger> extEuclidean(BigInteger a, BigInteger b) {
        if (b.compareTo(a) == 1) {
            return extEuclidean(b, a);
        }
        
        Pair<BigInteger, BigInteger> p = new Pair<BigInteger, BigInteger>(new BigInteger("11"), new BigInteger("42"));
        //System.out.println(p);
        
        List<BigInteger> xs = new ArrayList<BigInteger>();
        xs.add(new BigInteger("1"));
        xs.add(new BigInteger("0"));
        List<BigInteger> ys = new ArrayList<BigInteger>();
        ys.add(new BigInteger("0"));
        ys.add(new BigInteger("1"));
        List<BigInteger> ds = new ArrayList<BigInteger>();
        ds.add(a);
        ds.add(b);
        List<BigInteger> ks = new ArrayList<BigInteger>();
        ks.add(new BigInteger("42"));
        ks.add(a.divide(b));
        
        int i = 2;
        do {
            xs.add(xs.get(i-2).subtract(ks.get(i-1).multiply(xs.get(i-1))));
            ys.add(ys.get(i-2).subtract(ks.get(i-1).multiply(ys.get(i-1))));
            ds.add(ds.get(i-2).mod(ds.get(i-1)));
            ks.add(ds.get(i-1).divide(ds.get(i)));
            i += 1;
        } while (ds.get(ds.size() - 1).compareTo(new BigInteger("1")) != 0);
    
        return new Pair<BigInteger, BigInteger>(xs.get(xs.size() - 1), ys.get(ys.size() - 1));
    }*/
}