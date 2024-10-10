import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class CardInputStream extends InputStream {
	BufferedReader reader; 
	
	public CardInputStream(InputStream input) { // constructor for reader, input is meant for a socket inputstream
		this.reader = new BufferedReader(new InputStreamReader(input));
	}
	
	public Card readCard() {
		try {
			String readerLine;
			readerLine = reader.readLine();
			if (readerLine.startsWith("CARD") == false) { // if reader returns "CARD" then continue, thats the identifier for card sent
				return null;
			}
			if (readerLine.startsWith("CARD")) { // as long as the string starts with "CARD", which is identifier for a card being sent
				String longID = reader.readLine();
				long ID = Long.valueOf(longID).longValue(); // takes long value as a string, converts to long
				
				String nameValue = reader.readLine(); // takes name of given card
				
				String rankValue = reader.readLine(); // takes rank of given card
				
				Rank rank = Rank.valueOf(rankValue); // takes rank of given card
				
				String longPrice = reader.readLine(); // takes price of given card as string, converts it to long
				long Price = Long.valueOf(longPrice).longValue();
				
				return new Card(ID,nameValue,rank,Price); // returns new card with all following variables
			}
			return null; 
			
		
		} catch (IOException e) {
			e.printStackTrace(); // catch, print exception if raised
			return null;
		}
		
		
	}
	
	public String readResponse() throws IOException {
		return reader.readLine(); // returns a line from reader, throws exception if anything goes wrong
	}
		


	@Override
	public void close() throws IOException{
		reader.close(); // closes reader, throws exception if anything goes wrong
	}


	@Override
	public int read() throws IOException {
		// TODO Auto-generated method stub
		return reader.read();
	}

}
