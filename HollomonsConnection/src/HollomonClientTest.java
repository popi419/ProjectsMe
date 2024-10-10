import java.util.ArrayList;

public class HollomonClientTest {

	public static void main(String[] args) {
		HollomonClient hc0 = new HollomonClient("netsrv.cim.rhul.ac.uk",1812);
		assert (new ArrayList<Card>(hc0.login("story", "cellexistrest")) != null) : "Test 1 failed";
		assert (new ArrayList<Card>(hc0.getCards()) != null) : "Test 1 failed";
		
		System.out.println("Test 1 passed");
		
		assert (hc0.getCredits() != 0) : "Test 2 failed";
		
		assert (hc0.getOffers() != null) : "Test 2 failed";
		
		hc0.close();
		
		System.out.println("Test 2 passed");

	}

}
