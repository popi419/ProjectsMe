import java.io.IOException;
import java.util.List;

public class BirthdayPlannerTest {
	
	public static void main(String[] args) {
		ActivityStore store = new ActivityStore();
		store.add("b", "Ball");
		assert store.getRandomItem("b").equals("Ball") : "test 1 failed";
		System.out.println("test 1 passed");
		
		RestaurantStore store2 = new RestaurantStore();
		store2.add("a", "apples and creme");
		assert store2.getRandomItem("a").equals("Apples and creme (restaurant)") : "test 2 failed";
		System.out.println("test 2 passed");
		
		
	    CafeStore store3 = new CafeStore();
	    store3.add("c", "cookies and caramel");
	    assert store3.getRandomItem("c").equals("Cookies and caramel (cafe)") : "test 3 failed";
	    System.out.println("test 3 passed");
		
	    
	    
	    try {
			ActivityStore storeFileRead = new ActivityStore("main-activities.txt");
			ActivityStore store2FileRead = new RestaurantStore("restaurants.txt");
			ActivityStore store3FileRead = new CafeStore("cafes.txt");
			assert storeFileRead.getRandomItem("a").isEmpty() == false : "test 4 failed";
			assert store2FileRead.getRandomItem("a").isEmpty() == false : "test 5 failed";
			assert store3FileRead.getRandomItem("a").isEmpty() == false : "test 6 failed";
			System.out.println("--read file test pass 1");
			
			ActivityStore storeFileReadMulti = new ActivityStore("main-activities.txt",2);
			ActivityStore store2FileReadMulti = new RestaurantStore("restaurants.txt",2);
			ActivityStore store3FileReadMulti = new CafeStore("cafes.txt",2);
			assert storeFileReadMulti.getRandomItem("bu").isEmpty() == false : "test 7 failed";
			assert store2FileReadMulti.getRandomItem("na").isEmpty() == false : "test 8 failed";
			assert store3FileReadMulti.getRandomItem("co").isEmpty() == false : "test 9 failed";
			System.out.println("--read file test pass 2");
			
			BirthdayPlanner birthdayPlanner = new BirthdayPlanner();
			List<String> activityList = birthdayPlanner.generate("spaghetti");
			assert activityList.isEmpty() == false : "birthday test 1 failed";
			assert activityList.size() == 9 : "birthday test 1 failed";
			System.out.println("birthday test 1 passed");
			
			BirthdayPlanner birthdayPlannerIndex = new BirthdayPlanner(3);
			List<String> activityListIndex = birthdayPlannerIndex.generate("Matthew",3);
			assert activityListIndex.isEmpty() == false : "birthday test 2 failed";
			assert activityListIndex.size() == 3 : "birthday test 2 failed";
			System.out.println("birthday test 2 passed");
			
			
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	    
		
	}

}
