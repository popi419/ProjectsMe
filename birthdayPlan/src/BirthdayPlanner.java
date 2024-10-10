import java.util.List;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class BirthdayPlanner {
	protected ActivityStore activities;
	protected CafeStore cafes;
	protected RestaurantStore restaurants;
	
	public BirthdayPlanner() throws IOException {
		this.activities = new ActivityStore("main-activities.txt");
		this.cafes = new CafeStore("cafes.txt");
		this.restaurants = new RestaurantStore("restaurants.txt");
	}
	
	public BirthdayPlanner(int prefix) {
		this.activities = new ActivityStore("main-activities.txt",prefix);
		this.cafes = new CafeStore("cafes.txt",prefix);
		this.restaurants = new RestaurantStore("restaurants.txt",prefix);
	}
	
	public int[] restaurantChecker(int[] events) {
		Random choice = new Random();
		boolean restaurantCheck = false;
		for (int i = 1; i < events.length; i++) { // populates the array with numbers corresponding to activities, also adheres to restaurant rule and ensures not more than one restaurant is on the plan
			if (restaurantCheck) {
				events[i] = choice.nextInt(2);
			}
			else {
				events[i] = choice.nextInt(3);
				if (events[i] == 2){
					restaurantCheck = true;
				}
			}
		}
		return events;
	}
	
	public boolean checkActivityRule(int[] events) {
		boolean checkActivity = true;
		for (int i = 0; i < events.length-2; i++) { // checks if more than two activities occur in a row in the array
			if (events[i] == 0 && events[i+1] == 0 && events[i+2] == 0) {
				checkActivity = false;
				break;
			}
			
		}
		return checkActivity;
	} 
	
	public boolean checkFoodRule(int[] events) {
		boolean checkFoodRule = true;
		for (int i = 0; i < events.length-1;i++) { // checks if a row of elements in the array has an order of cafe, cafe, or cafe, restaurant, or restaurant, cafe
			if (events[i] == 1 && events[i+1] == 1) {
				checkFoodRule = false;
				break;
			}
			if (events[i] == 1 && events[i+1] == 2) {
				checkFoodRule = false;
				break;
			}
			if (events[i] == 2 && events[i+1] == 1) {
				checkFoodRule = false;
				break;
			}
		}
		return checkFoodRule;
	}
	public int[] buildRandomDay(int events, boolean cafeStart) {
		int[] randomDay = null; // initializes the return array that has the list of activities, corresponding in numbers 0 = main activity, 1 = cafe, 2 = restaurant
		boolean isValid = false; 
		while (isValid == false) { // goes through checks before being considered valid
			//System.out.println("retry");
			randomDay = new int[events]; // amount of events that the array should hold
			if (cafeStart == true) { // starts with a cafe or activity
				randomDay[0] = 1;
			}
			else {
				randomDay[0] = 0;
			}
			randomDay = restaurantChecker(randomDay); // fills the array as according to the restaurant rule given, aka there is at most one restaurant activity.

			//activity checks
			boolean checkActivity = checkActivityRule(randomDay); // checks the array to see if it adheres to the activity rule, main activities appear at most twice in a row (but can appear alone);
			
			boolean checkFoodRule = checkFoodRule(randomDay); // checks the array to see if it adheres to the food rule, eating activities do not occur twice in a row;
			
			if (checkActivity == true && checkFoodRule == true) { // if both are true, then the loop can be broken, and the array returned, else generate a new random array of integers and go through checks again
				isValid = true;
			}

		}
		return randomDay;
	}
	
	public List<String> generate(String input){
		Random choice = new Random(); // random choice generator
		String[] inputArr = input.split(""); // splits the input into characters in an array
		
		int[] randomChoices = null; // holder for what activities is chosen for the birthday

	    List<String> listofActivities = new ArrayList<String>(); // activities to be iterated over after being filled
		int i = choice.nextInt(2); // choose between 0 = start with an activity, 1 = start with a cafe
		if (i == 0) { 
			randomChoices = buildRandomDay(inputArr.length, false);
		}
		else if (i == 1) {
			randomChoices = buildRandomDay(inputArr.length, true);
		}
		for (int j = 0; j<randomChoices.length;j++) { // populates the list of activities based on the randomChoice array, and numbers corresponding to types of activities
			if (randomChoices[j] == 0) {
				listofActivities.add(activities.getRandomItem(inputArr[j]));
			}
			if (randomChoices[j] == 1) {
				listofActivities.add(cafes.getRandomItem(inputArr[j]));
			}
			if (randomChoices[j] == 2) {
				listofActivities.add(restaurants.getRandomItem(inputArr[j]));
			}
		}
		return listofActivities;
	}

	// attempts at building prefix generator
	public List<String> generate(String input, int prefix){
		
		String inputString = input;
	
		List<String> listofStringsChecked = new ArrayList<String>();
		String startString = "";
		 while (inputString.isEmpty() != true) {
		        int endIndex = Math.min(prefix, inputString.length());  // ensures endIndex doesn't exceed length of the remaining string
		        startString = wrapUp(inputString.substring(0, endIndex));
		        listofStringsChecked.add(startString);
		        inputString = inputString.substring(endIndex);
		    }
		List<String> listofActivitiesGenerated = new ArrayList<String>();
		for (String i : listofStringsChecked) {
			listofActivitiesGenerated.add(wrapUpActivity(i));
		}
		return listofActivitiesGenerated;
	}

	public String wrapUpActivity(String input) {
		Random choice = new Random();
		// initializes various checks based on if input correlates to an activity, cafe or restaurant
		boolean activityCheck = activities.getRandomItem(input) != null;
		boolean cafeCheck = cafes.getRandomItem(input) != null;
		boolean restaurantCheck = restaurants.getRandomItem(input) != null;
		// prepares strings to hold activities, cafes and restaurants
		String activityString = "";
		String cafeString = "";
		String restaurantString = "";
		if (activityCheck == true) { // if true, add capitalized input of a random activity that correlates to input
			activityString = activities.getRandomItem(input);
			activityString = activityString.substring(0,input.length()).toUpperCase() + activityString.substring(input.length());
		}
		if (cafeCheck == true) { // if true, add capitalized input of a random cafe that correlates to input
			cafeString += cafes.getRandomItem(input);
			cafeString = cafeString.substring(0,input.length()).toUpperCase() + cafeString.substring(input.length());
		}
		if (restaurantCheck == true) {  // if true, add capitalized input of a random restaurant that correlates to input
			restaurantString += restaurants.getRandomItem(input);
			restaurantString = restaurantString.substring(0,input.length()).toUpperCase() + restaurantString.substring(input.length());
		}
		
		String[] arrOfActivities = {activityString,cafeString,restaurantString};
		List<String> activityChoices = new ArrayList<String>(); 
		
		for (int index = 0; index < arrOfActivities.length; index++) { // iterate over strings made that arent null, add them to list
			if (arrOfActivities[index].isEmpty() != true) {
				activityChoices.add(arrOfActivities[index]);
			}
		}
		int randomChoice = choice.nextInt(activityChoices.size()); // choose a random activity from list, return it
		return activityChoices.get(randomChoice);
	}
	
	public String wrapUp(String input) {
		// if the input has any of the following truth values, return it
		if (activities.getRandomItem(input) != null || cafes.getRandomItem(input) != null || restaurants.getRandomItem(input) != null) {
			return input;
		}
		else {
			// slice the string, from length to 0 and try again
			return wrapUp(input.substring(0,input.length()-1));
		}	
	}
	

		

	public static void main(String[] args) {
		try {
			if (args.length == 0) {
				System.out.println("no command args");
			}
			else if (args.length == 1) {
				// q3 cmd line generator
				BirthdayPlanner planner = new BirthdayPlanner();
				List<String> activityList = planner.generate(args[0]);
				for (String i : activityList) {
					System.out.println(i);
				}
			}
			else if (args.length == 2) {
				// q4 cmd line generator
				int argsNumber = Integer.parseInt(args[1]);
				BirthdayPlanner planner = new BirthdayPlanner(argsNumber);
				List<String> activityList = planner.generate(args[0],argsNumber);
				for (String i : activityList) {
					System.out.println(i);
				}
			}
			
	
		}
		catch (Exception e) {
			System.out.println(e);
		}

	}
}

	
	


