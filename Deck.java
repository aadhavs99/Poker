package poker;

public class Deck {

	private Card[] cards;
	
	

	public Deck() {
		int count = 0; // index of array of deck of cards
		Card[] cards = new Card[52]; // array of 52 cards
		for (int suit = 0; suit<4; suit++) { // different suits
			for (int val = 1; val<14; val++) {	// different numerical values
				cards[count] = new Card(val, suit);
				count +=1; // move cursor over by 1
			}
		}
		this.cards = cards; 
	}

	public Deck(Deck other) { // copy constructor
		this.cards = other.cards;
	}

	public Card getCardAt(int position) { // returns card at specified position
		return cards[position];
	}

	public int getNumCards() { // returns number of cards in deck
		return cards.length;
	}

	public void shuffle() { // shuffles deck
		int firstLength = 0;
		if (cards.length%2 == 1) { // checks if odd
			firstLength += 1; // makes first deck larger if odd
		}
		// temporary deck representing top half of the deck:
		Card[] temp1 = new Card[cards.length/2+firstLength];
		// temporary deck representing top bottom of the deck:
		Card[] temp2 = new Card[cards.length/2];
		for (int i = 0; i<cards.length/2+firstLength; i++) {
			temp1[i] = cards[i]; // fills array with top half
		}
		int count = 0;
		for (int i = cards.length/2+firstLength; i<cards.length; i++) {
			temp2[count] = cards[i]; // fills array with bottom half
			count += 1;
		}
		int count2 = 0;
		// temporary deck to combine the two halves:
		Card[] temp3 = new Card[cards.length]; 
		for (int i = 0; i<cards.length-1; i+=2) {
			temp3[i] = temp1[count2]; // inserts card from first half
			temp3[i+1] = temp2[count2]; // inserts card from second half
			count2 += 1;
		}
		if (firstLength >0) { // if odd then last card manually inserted
			temp3[cards.length-1] = temp1[count2];
		}
		this.cards = temp3; // sets them equal
		
		
	}
	// method to cut deck with position:
	public void cut(int position) {
		Card[] temp1 = new Card[52]; // creates temporary deck of cards
		int count = 0;
		// puts second half of cards in new temporary deck
		for (int i = position; i<cards.length; i++) {
			temp1[count] = cards[i]; 
			count +=1;
		}
		// puts first half of cards at the end of temporary deck:
		for (int i = 0; i<position; i++) {
			temp1[count] = cards[i];
			count +=1;
		}
		this.cards = temp1; // sets them equal:
	}
	// method to deal the cards:
	public Card[] deal(int numCards) {
		// creates temporary deck representing hand:
		Card[] temp2 = new Card[numCards]; 
		for (int i =0; i<numCards; i++) {
			temp2[i] = cards[i]; // fills temporary deck with hand
		}
		// temporary deck representing new deck:
		Card[] temp1 = new Card[cards.length-numCards]; 
		int count = numCards;
		for (int i = 0; i<temp1.length; i++) {
			temp1[i] = cards[count]; // fills new temporary deck minus hand
			count +=1;
		}
		this.cards = temp1; // sets them equal
		return temp2;
	}
		
}
