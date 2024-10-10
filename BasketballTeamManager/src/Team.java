public class Team {
	private int[] players;
	private String[] playerInfo = {null,"Nicholas","Danny","Joyce","Farhad","Ariana","Hamza","Gwen","Shoji","Seema"}; // players 1-9
	
	public Team(int[] players) {
		this.players = new int[players.length];
		for (int i = 0; i < players.length;i++) { // fill team object with int[] 
			this.players[i] = players[i];
		}
	}
	public String getPlayerInfo(int playerNumber) {
		if (playerNumber < playerInfo.length || playerNumber > 1) { // if number in range 1-9
			return playerInfo[playerNumber];
		}
		return null;
		
	}
	public int getPlayer(int i) {
		return this.players[i];
	}
	public int[] getPlayers() {
		return this.players;
	}
	public String toString() {
		String playersString = "";
		for (int i = 0; i < players.length;i++) {
			playersString += players[i]; // iterate through array to add names to a string
			if (i < players.length-1) {
				playersString += " "; // add spaces in-between
			}
		}
		
		return playersString;
	}
//	public static void main(String[] args) {
//		int[] arr = {1,2,3};
//		Team team = new Team(arr);
//		System.out.println(team.getPlayerInfo(1));
//	}
}
