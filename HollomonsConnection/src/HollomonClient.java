import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class HollomonClient {
	BufferedReader reader;
	BufferedWriter writer;
	Socket socket;
	
	public HollomonClient(String server, int port) {
		// instantiates the client with the server socket, a bufferedreader to the socket inputstream to read input and a 
		// bufferedwriter to the outputstream to write to the server
		
		try {
			socket = new Socket(server,port);
			reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
		} catch (IOException e) {
			e.printStackTrace(); // catch, print exception if raised
		}
	}
	
	public long getCredits() {
		// writes the command "credits" to the server, gets response with the reader,
		// expects a long value of current "credits"
		try {
			writer.write("CREDITS");
			writer.newLine();
			writer.flush(); // flush required at the end of writer output to send to socket
			String longValue = reader.readLine();
			reader.readLine();
			if (longValue != null) {
				long credits = Long.valueOf(longValue).longValue(); // reads line of (Str)longValue if not null, turns it into long value
				return credits;
			}
			else {
				return 0; // return 0 if something went wrong
			}
		} catch (IOException e) {
			e.printStackTrace(); // catch, print exception if raised
			return 0;
		}
	}
	
	public List<Card> getOffers(){
		// writes command OFFERS to the server, reads response with reader
		// expects a list of cards on sale by other players
		try {
			writer.write("OFFERS");
			writer.newLine();
			writer.flush(); // flush required at the end of writer output to send to socket
			CardInputStream cardinputstream = new CardInputStream(socket.getInputStream()); // inputstream for reading cards
        	List<Card> cards = new ArrayList<Card>();
        	Card card; // putting cardinputstream results into card object
        	while ((card = cardinputstream.readCard()) != null) { // if the card read is not null
        		cards.add(card); // add it to arraylist of cards
        	}
        	Collections.sort(cards); // sort the card list via collections 
        	return cards;
			
		}
		catch (IOException e) {
			e.printStackTrace(); // catch, print exception if raised
			return null;
		}
	}
	
	public boolean buyCard(Card card) {
		// checks first if card is purchasable with current credit amount, then writes command BUY to server, reads response with reader
		// expects a confirmation that the card has been bought
		try {
			if (getCredits() < card.price) {
				System.out.println("no funds"); // if inadequate funds 
				return false;
			}
			writer.write("BUY " + card.ID);
			writer.newLine();	
			writer.flush(); // flush required at the end of writer output to send to socket
			
			if (reader.readLine().equals("ERROR")) {
				return false; // if the server returns "ERROR", something went wrong. return false
			}
			return true;
			
			
		}
		catch (IOException e){
			e.printStackTrace(); // catch, print exception if raised
			return false;
		}
	}
	
	public boolean sellCard(Card card, long price) {
		// writes command SELL to server, reads response with reader
		// expects a confirmation that the card has been put up for sale 
		try {

			writer.write("SELL " + card.ID + " " + price);
			writer.newLine();	
			writer.flush(); // flush required at the end of writer output to send to socket
			
			if (reader.readLine().equals("ERROR")) {
				return false; // if the server returns "ERROR", something went wrong. return false
			}
			return true;
		}
		catch (IOException e){
			e.printStackTrace(); // catch, print exception if raised
			return false;
		}
	}
	
	public List<Card> getCards(){
		// writes command CARDS to server, reads response with reader
		// expects a list of cards that the user owns
		try {
			writer.write("CARDS");
			writer.newLine();
			writer.flush(); // flush required at the end of writer output to send to socket
			CardInputStream cardinputstream = new CardInputStream(socket.getInputStream()); // inputstream for reading cards
        	List<Card> cards = new ArrayList<Card>();
        	Card card; // putting cardinputstream results into card object
        	while ((card = cardinputstream.readCard()) != null) { // if the card read is not null
        		cards.add(card); // add it to arraylist of cards
        	}
        	Collections.sort(cards); // sort the card list via collections
        	return cards;
			
		}
		catch (IOException e) {
			e.printStackTrace(); // catch, print exception if raised
			return null;
		}
	}
	public List<Card> login(String username, String password){
		// attempts to login to the Hollomon server with the given username and password in its args
		// if login is successful, list of cards is populated with currently owned cards
		// if login fails, returns the list as null
		try {
			
			// writes username and password, separated by newlines
			writer.write(username.toLowerCase());
			writer.newLine();
			writer.write(password);
			writer.newLine();
			writer.flush(); // flush required at the end of writer output to send to socket
			
			String lineRead = reader.readLine(); // reads the new line given by the server via reader

            // Check if login is successful
            if (lineRead != null && lineRead.contains("User")) { // if returned line is "User <yourusername> logged in successfully."
            	CardInputStream cardInputStream = new CardInputStream(socket.getInputStream()); // inputstream for reading cards
            	List<Card> cards = new ArrayList<Card>(); 
            	Card card; // putting cardinputstream results into card object
            	while ((card = cardInputStream.readCard()) != null) {  // if the card read is not null
            		cards.add(card); // add it to arraylist of cards
            	}
            	Collections.sort(cards); // sort the card list via collections 
            	return cards; // successful login, return list of cards
            } else {
                return null; // Unsuccessful login
            }
		}
		catch (IOException e){
			e.printStackTrace(); // catch, print exception if raised
			return null;
		}
		
	}
	
	public void close() {
		// closes the reader, writer, and socket, used usually when connection needs to be terminated
		try {
			writer.close();
			reader.close();
			socket.close();
		}
		catch (IOException e){
			e.printStackTrace();
		}
	}
	

}
