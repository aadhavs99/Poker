package poker;
public class PokerHandEvaluator {
	
	// method to find if there is one pair in hand:
	public static boolean hasPair(Card[] cards) { 
		for (int i=0; i<cards.length; i++) {
			// first card to compare to:
			Card temp = new Card(cards[i].getValue(), cards[i].getSuit()); 
			// second card to compare to:
			for(int j=0; j<cards.length; j++) {
				// if new card and different card value equal:
				if (temp.getValue() == cards[j].getValue() && !(temp.getSuit()
						== cards[j].getSuit())) { 
					return true; 
				}
			}
		}
		return false; // if no pairs are found
	}
	// method to find if hand has two separate pairs:
	public static boolean hasTwoPair(Card[] cards) {
		int count = 0;
		if (!hasFourOfAKind(cards)) { // making sure two pairs are different
			for (int i=0; i<cards.length; i++) {
				// first card to compare to:
				Card temp = new Card(cards[i].getValue(), cards[i].getSuit());
				// second card to compare to:
				for(int j=0; j<cards.length; j++) {
					// making sure cards are not repeating:
					if (temp.getValue() == cards[j].getValue() 
						&& !(temp.getSuit() 
							== cards[j].getSuit())) {
						// how many cards that are equal to each other are:
						count +=1; 
					}
				}
			}
		}
		if (count >=4) { // if there are two pairs
			return true;
		}
		return false;
	}
	// method to check if there are three cards with the same value:
	public static boolean hasThreeOfAKind(Card[] cards) { 
		if (hasPair(cards)) {
			for (int i=0; i<cards.length; i++) {
				// first card to compare to:
				Card temp = new Card(cards[i].getValue(), cards[i].getSuit());
				// second card to compare to:
				for(int j=0; j<cards.length; j++) {
					// checks for no repeats:
					if (temp.getValue() == cards[j].getValue() 
						&& !(temp.getSuit() == cards[j].getSuit())) {
						// making sure not last card:
						if (j<cards.length-1) {
							// making sure cards do not repeat,
							// third card to compare to:
							for(int k=j+1; k<cards.length; k++) {
								// checks for no repeats:
								if (cards[j].getValue() == cards[k].getValue() 
								&& !(cards[j].getSuit() == 
								cards[k].getSuit())
								&& !(temp.getSuit() 
								== cards[k].getSuit())){
									return true;
								}
							}
						}
					}
				}
			}
		} else {
			return false;
		}
		return false;
	}
	// method to check if hand has straight:
	public static boolean hasStraight(Card [] cards) {
		Card[] temp = new Card[5]; // new temporary hand
		int count = 0;
		// rearranges cards in ascending order:
		for(int l=0; l<temp.length; l++) {
			for (int i=0; i<cards.length; i++) {
				Card temp2 = cards[i]; // card to compare to
				// cards that are being compared:
				for(int j=0; j<cards.length; j++) {
					if (temp2.getValue()<cards[j].getValue()) {
					// counts number of cards that are greater than first card:
						count +=1; 
					}
				}
				// adds cards in ascending order to array
				temp[cards.length-(count+1)] = temp2;
				count = 0; // resets for next comparison
			}
		}
		// if in ascending order:
		if (!(temp[4] == null) && !(temp[3] == null) && !(temp[2] == null)
			&& !(temp[1] == null) && !(temp[0] == null) 
			&& temp[4].getValue()-temp[3].getValue() == 1 
			&& temp[3].getValue()-temp[2].getValue() == 1 && 
			temp[2].getValue()-temp[1].getValue() == 1 
			&& temp[1].getValue()-temp[0].getValue() == 1) {
			return true;
		}
		return false;
	}
	// method to check if hand has flush:
	public static boolean hasFlush(Card[] cards) {
		// checks if all cards' suits are equal
		if (cards[0].getSuit() == cards[1].getSuit() 
			&& cards[1].getSuit() == cards[2].getSuit() &&
			cards[2].getSuit() == cards[3].getSuit() && 
			cards[3].getSuit() == cards[4].getSuit() ) {
			return true;
		}
		return false;
	}
	// method to check if hand has full house
	public static boolean hasFullHouse(Card[] cards) {
		if (hasPair(cards)) { // if there isn't a pair, does not run
			for (int i=0; i<cards.length; i++) {
				// first card to compare to:
				Card temp = new Card(cards[i].getValue(), cards[i].getSuit());
				// second card to compare to:
				for(int j=0; j<cards.length; j++) {
					// check for no repeats:
					if (temp.getValue() == cards[j].getValue() 
						&& !(temp.getSuit() == cards[j].getSuit())) {
						if (j<cards.length-1) {
							// third card to compare to:
							for(int k=j+1; k<cards.length; k++) {
								// check for no repeats:
								if (cards[j].getValue() == cards[k].getValue() 
									&& !(cards[j].getSuit() 
									== cards[k].getSuit()) 
									&& !(temp.getSuit() == cards[k].getSuit())){
									// puts remaining two cards in array:
									Card[] temp2 = new Card[2];
									int count = 0;
									for(int l=0; l<cards.length; l++) {
										// checks for no repeats:
										if (!(cards[l].getValue() 
											== cards[j].getValue())){
											temp2[count] = cards[l];
											count +=1;
										}
									}
									// checks if two cards are a pair:
									if (!(temp2[0] == null) 
										&& !(temp2[1] == null) 
										&& hasPair(temp2)) {
										return true;
									}
									return false; // if not return false
								}
							}
						}
					}
				}
			}
		} else {
			return false;
		}
		return false;
	}
	// method to check if hand has four cards of same value:
	public static boolean hasFourOfAKind(Card[] cards) {
		// if there is four of same value then there has to be three:
		if (hasThreeOfAKind(cards)) {
			for (int i=0; i<cards.length; i++) {
				// first card to compare to:
				Card temp = new Card(cards[i].getValue(), cards[i].getSuit());
				// second card to compare to:
				for(int j=0; j<cards.length; j++) {
					// check for no repeats:
					if (temp.getValue() == cards[j].getValue() 
						&& !(temp.getSuit() == cards[j].getSuit())) {
						if (j<cards.length-1) {
							// third card to compare to:
							for(int k=j+1; k<cards.length; k++) {
								// check for no repeats:
								if (cards[j].getValue() == cards[k].getValue() 
									&& !(cards[j].getSuit() == 
									cards[k].getSuit()) 
									&& !(temp.getSuit() == 
									cards[k].getSuit())){
									// fourth card to compare to:
									for(int l=0; l<cards.length; l++) {
										// check for no repeats:
										if ((cards[l].getValue() 
											== cards[j].getValue()) 
											&& !(cards[j].getSuit() 
											== cards[l].getSuit()) 
											&& !(temp.getSuit() 
											== cards[l].getSuit()) 
											&& !(cards[k].getSuit() 
											== cards[l].getSuit())){
											return true;
										}
									}
								}
							}
						}
					}
				}
			}
		} else {
			return false;
		}
		return false;
	}
	// method to check if hand has straight flush
	public static boolean hasStraightFlush(Card[] cards) {
		// uses methods already written to check:
		return (hasStraight(cards) && hasFlush(cards));
	}
}

