import java.io.IOException;

public class RestaurantStore  extends ActivityStore {
	
	public RestaurantStore() {
		super(); // calls the parent class, activitystore for its constructor
	}
	public RestaurantStore(String filename) throws IOException {
		super(filename); // calls the parent class, activitystore for its constructor
	}
	
	public RestaurantStore(String filename, int prefix) {
		super(filename,prefix); // calls the parent class, activitystore for its constructor
		
	}
	
	public String getRandomItem(String key) {
		// calls its parent class for the getRandomItem method, appends (restaurant) to item as specified by the assignmentment brief
		String result = super.getRandomItem(key);
		if (result == null) {
			return null;
		}
		result += " (restaurant)";
		return result;
	}
}
