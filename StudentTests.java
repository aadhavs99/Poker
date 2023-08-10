package poker;

import static org.junit.Assert.*;

import java.util.Arrays;

import org.junit.Test;

public class StudentTests {
	
	@Test
	public void testDeck() {
		Deck car = new Deck();
		Card[] temp = new Card[52];
		int count = 0;
		for (int suit = 0; suit<4; suit++) {
			for (int val = 1; val<14; val++) {
				temp[count] = new Card(val, suit);
				assertTrue(temp[count].getSuit() 
						== (car.getCardAt(count).getSuit()));
				assertTrue(temp[count].getValue() 
						== (car.getCardAt(count).getValue()));
				count +=1;
			}
		}
	}
	@Test
	public void testShuffle() {
		Deck car = new Deck();
		car.shuffle();
		assertTrue(car.getCardAt(0).getValue() == 1);
		assertTrue(car.getCardAt(0).getSuit() == 0);
	} 
	@Test
	public void testCut() {
		Deck car = new Deck();
		car.cut(4);
		Deck temp = new Deck();
		int count = 0;
		for (int i = 4; i<52; i++) {
			assertTrue(temp.getCardAt(i).getSuit() 
					== car.getCardAt(count).getSuit());
			assertTrue(temp.getCardAt(i).getValue() 
					== car.getCardAt(count).getValue());
			count +=1;
		}
		count = 0;
		for (int i = 48; i<52; i++) {
			assertTrue(temp.getCardAt(count).getSuit() 
					== car.getCardAt(i).getSuit());
			assertTrue(temp.getCardAt(count).getValue() 
					== car.getCardAt(i).getValue());
			count +=1;
		}
	}
	@Test
	public void testDeal() {
		Deck car = new Deck();
		Deck temp = new Deck();
		Card[] test = car.deal(4);
		for(int i = 0; i<4; i++) {
			assertTrue(test[i].getSuit() == temp.getCardAt(i).getSuit());
			assertTrue(test[i].getValue() == temp.getCardAt(i).getValue());
		}
		int count = 0;
		for(int i = 4; i<car.getNumCards()+4; i++) {
			assertTrue(temp.getCardAt(i).getSuit() 
					== car.getCardAt(count).getSuit());
			count +=1;
		} 
	}  
	@Test
	public void testHandEvaluators() {
		Card[] test = new Card[5];
		test[0] = new Card(5, 1);
		test[1] = new Card(9, 3);
		test[2] = new Card(9, 2);
		test[3] = new Card(4, 1);
		test[4] = new Card(5, 2);
		assertTrue(PokerHandEvaluator.hasPair(test));
		assertTrue(PokerHandEvaluator.hasTwoPair(test));
		assertFalse(PokerHandEvaluator.hasThreeOfAKind(test)); 
		assertFalse(PokerHandEvaluator.hasStraight(test));
		assertFalse(PokerHandEvaluator.hasFlush(test));
		assertFalse(PokerHandEvaluator.hasFullHouse(test));
		assertFalse(PokerHandEvaluator.hasFourOfAKind(test)); 
		assertFalse(PokerHandEvaluator.hasStraightFlush(test));
		Card[] test3 = new Card[5];
		test3[0] = new Card(5, 1);
		test3[1] = new Card(5, 2);
		test3[2] = new Card(9, 2);
		test3[3] = new Card(9, 1);
		test3[4] = new Card(9, 3);
		assertTrue(PokerHandEvaluator.hasPair(test3)); 
		assertTrue(PokerHandEvaluator.hasTwoPair(test3)); 
		assertTrue(PokerHandEvaluator.hasThreeOfAKind(test3)); 
		assertFalse(PokerHandEvaluator.hasStraight(test3));
		assertFalse(PokerHandEvaluator.hasFlush(test3));
		assertTrue(PokerHandEvaluator.hasFullHouse(test3));
		assertFalse(PokerHandEvaluator.hasFourOfAKind(test3)); 
		assertFalse(PokerHandEvaluator.hasStraightFlush(test3));
		Card[] test4 = new Card[5];
		test4[0] = new Card(1, 3);
		test4[1] = new Card(1, 0);
		test4[2] = new Card(1, 1);
		test4[3] = new Card(11, 0);
		test4[4] = new Card(11, 3);
		assertTrue(PokerHandEvaluator.hasPair(test4));
		assertTrue(PokerHandEvaluator.hasTwoPair(test4));
		assertTrue(PokerHandEvaluator.hasThreeOfAKind(test4));	
		assertFalse(PokerHandEvaluator.hasStraight(test4));
		assertFalse(PokerHandEvaluator.hasFlush(test4));
		assertTrue(PokerHandEvaluator.hasFullHouse(test4));
		assertFalse(PokerHandEvaluator.hasFourOfAKind(test4));
		assertFalse(PokerHandEvaluator.hasStraightFlush(test4));
		Card[] test5 = new Card[5];
		test5[0] = new Card(1, 3);
		test5[1] = new Card(1, 2);
		test5[2] = new Card(1, 1);
		test5[3] = new Card(1, 0);
		test5[4] = new Card(11, 3);
		assertTrue(PokerHandEvaluator.hasPair(test5));
		assertFalse(PokerHandEvaluator.hasTwoPair(test5));
		assertTrue(PokerHandEvaluator.hasThreeOfAKind(test5));
		assertFalse(PokerHandEvaluator.hasStraight(test5));
		assertFalse(PokerHandEvaluator.hasFlush(test5));
		assertFalse(PokerHandEvaluator.hasFullHouse(test5));
		assertTrue(PokerHandEvaluator.hasFourOfAKind(test5));
		assertFalse(PokerHandEvaluator.hasStraightFlush(test5));
		Card[] test6 = new Card[5];
		test6[0] = new Card(1, 3);
		test6[1] = new Card(2, 3);
		test6[2] = new Card(5, 3);
		test6[3] = new Card(3, 3);
		test6[4] = new Card(4, 3);
		assertFalse(PokerHandEvaluator.hasPair(test6));
		assertFalse(PokerHandEvaluator.hasTwoPair(test6));
		assertFalse(PokerHandEvaluator.hasThreeOfAKind(test6));
		assertTrue(PokerHandEvaluator.hasStraight(test6));
		assertTrue(PokerHandEvaluator.hasFlush(test6));
		assertFalse(PokerHandEvaluator.hasFullHouse(test6));
		assertFalse(PokerHandEvaluator.hasFourOfAKind(test6));
		assertTrue(PokerHandEvaluator.hasStraightFlush(test6));
		Card[] test7 = new Card[5];
		test7[0] = new Card(2, 3);
		test7[1] = new Card(2, 0);
		test7[2] = new Card(2, 1);
		test7[3] = new Card(2, 2);
		test7[4] = new Card(9, 0);
		assertTrue(PokerHandEvaluator.hasPair(test7));
		assertFalse(PokerHandEvaluator.hasTwoPair(test7));
		assertTrue(PokerHandEvaluator.hasThreeOfAKind(test7));
		assertFalse(PokerHandEvaluator.hasStraight(test7));
		assertFalse(PokerHandEvaluator.hasFlush(test7));
		assertFalse(PokerHandEvaluator.hasFullHouse(test7));
		assertTrue(PokerHandEvaluator.hasFourOfAKind(test7));
		assertFalse(PokerHandEvaluator.hasStraightFlush(test7));
	}

}
