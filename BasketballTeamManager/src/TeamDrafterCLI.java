import java.util.Scanner;

public class TeamDrafterCLI {
	
	public static void playGame(TeamDrafter game) {
		boolean gameLoop = true;
		Scanner scanner = new Scanner(System.in);
		while (gameLoop == true) { // game loop active until solution is found
			System.out.println("Previous attempts:");
			
			if (game.getPreviousSuggestions() != null) {
				System.out.println(game.getPreviousSuggestions()); // prints previous attempts
			}
			else {
				System.out.println("No previous attempts.");
			}
			
			System.out.println("Enter new team:");
			int[] newTeam = new int[game.getSolution().getPlayers().length];
			boolean loopStop = false;
			
			for (int i = 0; i < newTeam.length;i++) {
				int numberRead = scanner.nextInt();
				if (numberRead <= 0 || numberRead > 9) { // if number isnt in range 1-9
                    System.out.println("Invalid team!");
                    loopStop = true;
                    break; // break loop
                }
				for (int j = 0; j < newTeam.length; j++) {
					if (numberRead == newTeam[j]) { // if duplicate elements found in input
						System.out.println("Invalid team!");
	                    loopStop = true;
	                    break; // break loop
					}
				}
				newTeam[i] = numberRead;
			}
			if (loopStop == false) { // if flag isnt raised and array passes checks
				Team team1 = new Team(newTeam);
				if (game.checkSuggestedTeam(team1)) {
					System.out.println("The final team is:");
					for (int i = 0; i < newTeam.length; i++) {
					    System.out.println(team1.getPlayerInfo(newTeam[i])); // print out names of players
					}
					gameLoop = false; // ends game
				}
			}
			scanner.nextLine(); // moves to empty line for next input
		}
		scanner.close(); // closes scanner
	}
	public static void main(String[] args) {
		int[] testCase = {9,3,4,7,1};
		Team team = new Team(testCase);
		TeamDrafter testGame = new TeamDrafter(team);
		playGame(testGame);
		
		
		
	}

}
