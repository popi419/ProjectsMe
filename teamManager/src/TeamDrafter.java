
public class TeamDrafter {
	private Team solutionTeam;
	private ListNode head;
	
	class ListNode {

		private ListNode next;
		private SuggestedTeam value;
		
		public ListNode(SuggestedTeam value,ListNode next) {
			this.value = value;
			this.next = next;
		}
		public ListNode(SuggestedTeam value) {
			this.value = value;
			this.next = null;
		}
		public SuggestedTeam getValue() {
			return value;
		}	
		public ListNode getNext() {
			return next;
		}
		public void setValue(SuggestedTeam value) {
			this.value = value;
		}
		public void setNext(ListNode next) {
			this.next = next;
		}
		public String toString() {
			String stringList = "";
			if (head == null) {
				return null;
			}
			else {
				ListNode current = head; // cursor
				while (current != null) {
					stringList += current.getValue().toString();
					stringList += "\n"; // move to new line after every string

					current = current.getNext();
				}
			}
			return stringList;
		}
		
	}
	
	public void insertAtHead(SuggestedTeam suggestedTeam) {
		ListNode newHead = new ListNode(suggestedTeam,null); // newHead -> null
		newHead.setNext(head); // newHead -> (head)Team -> ...
		head = newHead; // (head)newHead -> Team -> ...
	}
	
	public TeamDrafter(Team solutionTeam) {
		this.solutionTeam = solutionTeam; 
	}
	
	public TeamDrafter() {
		int[] randomSolution = new int[5];
		
		boolean isRandom = false;
		
		while (isRandom == false) {
        	for (int i = 0; i < randomSolution.length;i++) {
    			randomSolution[i] = (int) Math.floor(Math.random() * 9)+1; // generate from 1-9
    		}
        	
        	isRandom = true; 
        	for (int j = 0; j < randomSolution.length; j++) {
        		for (int k = j+1; k < randomSolution.length; k++) {
        			if (randomSolution[j] == randomSolution[k]) {  // if duplicate element is found
        				isRandom = false;
        				break; // breaks out of inner 
        			}
        		}
        		if (isRandom == false) {
        			break; // breaks out of outer
        		}
        	}
        }
		if (isRandom == true) {
			Team newSolution = new Team(randomSolution);
			this.solutionTeam = newSolution; // makes randomized solution the new solution
		}
		
	}
	public boolean checkSuggestedTeam(Team teamSuggested) { // checks if suggestedTeam == solutionTeam
		SuggestedTeam suggestedTeam = new SuggestedTeam(teamSuggested, solutionTeam);
		insertAtHead(suggestedTeam); 
		if (suggestedTeam.isCorrect()) {
			return true;
		}
		return false;
	}
		
	public ListNode getPreviousSuggestions() {
		return head; // running toString on this node gives list of all previous attempts

	}
	public Team getSolution() {
		return solutionTeam;
	}
	
	
	
}
