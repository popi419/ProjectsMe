import java.util.HashSet;
import java.util.TreeSet;

public class CardTest {

	public static void main(String[] args) {
		
	    assert (new Card(1, "card1", Rank.COMMON).compareTo(new Card(2, "card2", Rank.COMMON)) == -1) : "Test 1 failed";

	    assert (new Card(1,"card1",Rank.RARE).compareTo(new Card(1,"card2",Rank.COMMON)) == 1) : "Test 1 failed";

	    assert (new Card(1,"card11",Rank.COMMON).compareTo(new Card(1,"card1",Rank.COMMON)) == -1) : "Test 1 failed";
	    
	    assert (new Card(1,"card1",Rank.COMMON)).toString().equals("1 card1 COMMON 0") : "Test 1 failed";
	    
	    System.out.println("Test 1 passed");
	    
	    HashSet<Card> hashset = new HashSet<Card>();
	    hashset.add(new Card(1,"card1",Rank.COMMON));
	    hashset.add(new Card(1,"card11",Rank.COMMON));
	    hashset.add(new Card(1,"card111",Rank.COMMON));
	    hashset.add(new Card(1,"card1111",Rank.COMMON));
	    hashset.add(new Card(1,"card11111",Rank.COMMON));
	    
	    hashset.add(new Card(1,"card1",Rank.COMMON));
	    
	    assert (hashset.size() == 5) : "Test 2 failed";
	    
	    TreeSet<Card> treeset = new TreeSet<Card>();
	    treeset.add(new Card(1,"card1",Rank.COMMON));
	    treeset.add(new Card(2,"card2",Rank.COMMON));
	    treeset.add(new Card(3,"card3",Rank.COMMON));
	    treeset.add(new Card(4,"card4",Rank.COMMON));
	    
	    assert (treeset.toString().equals("[1 card1 COMMON 0, 2 card2 COMMON 0, 3 card3 COMMON 0, 4 card4 COMMON 0]")) : "Test 2 failed";
	    System.out.println("Test 2 passed");

	}

}
