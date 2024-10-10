
public class SuggestedTeam {
	private Team suggestedTeam;
	private Team solutionTeam;
	
	public SuggestedTeam (Team suggestion, Team solution) {
		this.suggestedTeam = suggestion;
		this.solutionTeam = solution;
	}
	public Team getTeam() {
		return this.suggestedTeam;
	}
	
	public int getNumGood() {
		int[] suggestTeam = suggestedTeam.getPlayers();
		int[] correctSolTeam = solutionTeam.getPlayers();
		int numberCorrectSpot = 0;
		for (int i = 0; i < suggestTeam.length;i++) {
			if (suggestTeam[i] == correctSolTeam[i]) { // checks how many elements are in the correct indexes
				numberCorrectSpot++;
			}
		}
		return numberCorrectSpot;

	}
	public int getNumWrongSpot() {
		int[] suggestTeam = suggestedTeam.getPlayers(); 
		int[] correctSolTeam = solutionTeam.getPlayers();
		int numberWrongSpot = 0;

		for (int i = 0; i < suggestTeam.length;i++) {
			if (suggestTeam[i] != correctSolTeam[i] && (i - 1 >= 0)) {
				for (int j = 0; j < i; j++) {
					if (suggestTeam[i] == correctSolTeam[j]) { // checks all elements before current element
						numberWrongSpot++;
					}
				}
			}
			if (suggestTeam[i] != correctSolTeam[i] && (i + 1 < suggestTeam.length)) {
				for (int k = i; k < suggestTeam.length; k++) {
					if (suggestTeam[i] == correctSolTeam[k]) { // checks all elements after current element
						numberWrongSpot++;
					}
				}
			}
		}
		return numberWrongSpot;
	}
	public boolean isCorrect() {
		SuggestedTeam team = new SuggestedTeam(suggestedTeam,solutionTeam);
		if (team.getNumGood() != solutionTeam.getPlayers().length) {
			return false;
		}
		return true;
		
	}
	public String toString() {
		int goodCount = getNumGood();
		int badCount = getNumWrongSpot();
		String strGetSpots = suggestedTeam.toString() + " (Good " + goodCount + "," + " Wrong spot " + badCount + ")"; // x x x x x (Good <num>, Wrong spot <num>)
		return strGetSpots;
	}

}
