import java.util.HashSet;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

public class ActivityStore {
	
	protected HashMap<String, HashSet<String>> mapping; // all items for the activity store and their corresponding letters
	
	public ActivityStore() { // constructor
		mapping = new HashMap<String, HashSet<String>>(); 
	}
	
	public ActivityStore(String filename) throws IOException {
		BufferedReader reader = null;
		try { // reads file via bufferedreader, line by line
			File file = new File(filename);
			reader = new BufferedReader(new FileReader(file));
			mapping = new HashMap<String, HashSet<String>>();
			String line;
			while ((line = reader.readLine()) != null) { // for each line, it takes the first letter and uses add(key,line) to make a mapping for said line/activity
				String key = line.substring(0,1); 
				line = key.toUpperCase() + line.substring(1);
				add(key,line);
			}
		}
		catch (IOException e) { // raises exception file is not found
			e.printStackTrace();
			System.out.println("File not found!");
		}
		finally { // runs regardless of input above, to close the reader
			if (reader != null) {
				try {
					reader.close();
				} 
				catch (IOException e) {
					
				}
				
			}
		}
		
	}
	public ActivityStore(String filename, int prefix) {
		BufferedReader reader = null;
		try { // reads file via bufferedreader, line by line
			File file = new File(filename);
			reader = new BufferedReader(new FileReader(file));
			mapping = new HashMap<String, HashSet<String>>();
			String line;
			while ((line = reader.readLine()) != null) {
				for (int i = 1; i <= prefix ; i++) { // for each line, it takes an int prefix amount of letters from said line and uses add(key,line) to make a mapping for said line/activity
					if (i >= line.length()) {
						continue;
					}
					String key = line.substring(0,i);
					String value = key + line.substring(i);
					add(key,value);
				}
				
			}
		}
		catch (IOException e) { // raises exception file is not found
			e.printStackTrace();
			System.out.println("File not found!");
		}
		finally { // runs regardless of input above, to close the reader
			if (reader != null) {
				try {
					reader.close();
				} 
				catch (IOException e) {
					
				}
				
			}
		}
		
	}
	
	public void add(String key,String item) { 
		// creates a key/value pair via a hashset, and adds said pair to the mapping of the store
		if (mapping.containsKey(key)) {
			mapping.get(key).add(item); // if one such mapping already exists for a different item, add that to the key/value pair too
		}
		else {
			// else create a new pair and add it to mapping
			HashSet<String> set = new HashSet<String>();
			set.add(item);
			mapping.put(key, set);
		}
	}
	public String getRandomItem(String key) {
		// creates a key and attempts to find a value for it
		key = key.toLowerCase();
		if (mapping.containsKey(key) != false) {
			Random random = new Random();
			// gets the key/value pair for the given key, picks a random index from said pair
			String[] value = mapping.get(key).toArray(new String[mapping.get(key).size()]);
			int L = random.nextInt(value.length);
			
			// return that random index in the array, make sure its capitalized properly, append the rest of the string and return it
			return value[L].substring(0,1).toUpperCase()+value[L].substring(1);
		}
		else {
			//return null if such a pair doesnt exist
			return null;
		}
	}

}
