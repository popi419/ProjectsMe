public class Card implements Comparable<Card> {
	long ID;
	String name;
	Rank rank;
	long price;
	
	public Card(long id, String name, Rank rank) { // constructor for card with no price
		this.ID = id;
		this.name = name;
		this.rank = rank;
		this.price = 0;
	}
	
	public Card(long id, String name, Rank rank, long price) { // constructor for card with price
		this.ID = id;
		this.name = name;
		this.rank = rank;
		this.price = price;
	}
	
	@Override
	public int hashCode() { // makes hashcode consisting of values ID, name and rank
		final int prime = 31;
		int result = 1;
		result = prime * result + (int) (ID ^ (ID >>> 32));
		result = prime * result + ((name == null) ? 0 : name.hashCode());
		result = prime * result + ((rank == null) ? 0 : rank.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) { // various checks to see if this card == other card
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Card other = (Card) obj;
		if (ID != other.ID)
			return false; // checks id
		if (name == null) {
			if (other.name != null) // checks name
				return false;
		} else if (!name.equals(other.name)) 
			return false;
		if (rank != other.rank) // checks rank
			return false;
		return true;
	}

	public String toString() {
		return (ID + " " + name + " " + rank + " " + price); // returns string representation of the card
	}


	@Override
	public int compareTo(Card o) { // see if this card is smaller, equal or bigger than card compared to
		
		// compares rank values from enum class, smaller values are bigger/more rare in this scenario
		if (this.rank.ordinal() > o.rank.ordinal()) {
	        return -1; 
	    } 
		else if (this.rank.ordinal() < o.rank.ordinal()) {
	        return 1;
	    }

	    // Ranks are equal, proceed to compare name lengths
	    if (this.name.length() > o.name.length()) {
	        return -1;
	    } 
	    else if (this.name.length() < o.name.length()) {
	        return 1;
	    }

	    // Ranks and name lengths are equal, compare IDs
	    if (this.ID > o.ID) {
	        return 1;
	    } 
	    else if (this.ID < o.ID) {
	        return -1;
	    }
		return 0;
	}

}
