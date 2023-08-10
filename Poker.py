from cmu_112_graphics import *
import random, string, math, time

class Card: # got this idea from a website, did not copy, simply got idea: https://medium.com/@anthonytapias/build-a-deck-of-cards-with-oo-python-c41913a744d3
    def __init__(self, number, suit):
        self.number = number # number of card
        self.suit = suit # suit of card
    def __repr__(self):
        return str(self.number)+str(self.suit) # combines both number and suit, ex: 10h(10 of hearts)

suits = ["d", "h", "s", "c"] # all the different possible suits
deck = [] # empty list for deck of cards
for number in range(1, 14):
    for suit in suits:
        deck.append(Card(number, suit)) # creates full deck of cards(11-14 are royals)
    
def appStarted(app):
    app.paused = False
    app.pot = 0 # total pot
    app.aiturn = False # whether it is ai's turn, used for transitioning and displaying AI's actions
    app.playing = False # used to check whether or not to start the game
    app.betting = False # whether in betting stage or not
    app.validBet = True # check whether bet is valid or not
    app.players = ['AI', 'Player1'] # minimum players in game
    app.money = [500, 500] # everybody starts off with 500 dollars
    app.curplayer = 0 # current player's turn
    app.player1 = [] # cards of player1
    app.ai = [] # cards of ai
    app.player2 = [] # cards of player 2
    app.player3 = [] # cards of player 3
    app.table = [] # cards on table
    app.transition = False # check whether to transition between players
    app.curdeck = deck # current deck in game
    app.betround = 1 # betting round
    app.curbet = 0 # current highest bet per round
    app.aiprob = -1 # prob of ai based on deck
    app.tableprob = -1 # prob of ai based on deck and table
    app.suitcount = 0 # number of same suits in a deck and table
    app.bestplayer = '' # highest valued hand at end of betting rounds
    app.numcount = 0 # number of same pairs in a deck and table
    app.staircount = 0 # number of stairs in a deck and table
    app.difficult = None # difficulty that user selects

def generateDecks(app): # generates deck of cards for all players
    if len(app.players) == 2: # if 2 players
        for index in range(2): # 2 cards per person
            rand = random.choice(app.curdeck)
            app.player1.append(rand)
            app.curdeck.remove(rand) # cards removed from deck
            rand = random.choice(app.curdeck)
            app.ai.append(rand)
            app.curdeck.remove(rand)
    if len(app.players) == 3: # if 3 players
        for index in range(2):
            rand = random.choice(app.curdeck)
            app.player1.append(rand)
            app.curdeck.remove(rand)
            rand = random.choice(app.curdeck)
            app.ai.append(rand)
            app.curdeck.remove(rand)
            rand = random.choice(app.curdeck)
            app.player2.append(rand)
            app.curdeck.remove(rand)
    if len(app.players) == 4: # if 4 players
        for index in range(2):
            rand = random.choice(app.curdeck)
            app.player1.append(rand)
            app.curdeck.remove(rand)
            rand = random.choice(app.curdeck)
            app.ai.append(rand)
            app.curdeck.remove(rand)
            rand = random.choice(app.curdeck)
            app.player2.append(rand)
            app.curdeck.remove(rand)
            rand = random.choice(app.curdeck)
            app.player3.append(rand)
            app.curdeck.remove(rand)


def addCards(app):
    if app.betround == 2: # 2nd round of betting == 3 cards on table
        for index in range(3):
            rand = random.choice(app.curdeck)
            app.table.append(rand)
            app.curdeck.remove(rand) # remove from deck
    else:
        rand = random.choice(app.curdeck)
        app.table.append(rand)
        app.curdeck.remove(rand) # remove from deck
    if len(app.table) == 5: # if last betting round, compare hands
        compareHands(app)

def tableProb(app): # calculates prob based on table alone
    prob = 0
    if app.tableprob == -1:
        app.tableprob = 0
    for index in range(len(app.ai)): # for every card in deck
        numstreak = 0
        suitstreak = 0
        stairstreak = 0
        for tablecard in range(len(app.table)):
            if app.ai[index].number == app.table[tablecard].number: # check if number equal
                if numstreak >= 10:
                    numstreak += 20
                else:
                    numstreak += 10
            if app.ai[index].number == ((app.table[tablecard].number)-1 or (app.table[tablecard].number)+1): # checks for staircase
                stairstreak += 10
            if app.ai[index].suit == app.table[tablecard].suit: # checks for same suit
                if suitstreak >= 10:
                    suitstreak += 20
                else:
                    suitstreak += 10
            if app.ai[index].number == ((app.table[tablecard].number)-1 or (app.table[tablecard].number)+1) and (app.ai[index].suit == app.table[tablecard].suit): # check for same suit and number(straight flush)
                prob += 50
    for index in range(len(app.table)-1): # check for every card in table 
        if app.table[index].number == app.table[index+1].number: # check for same number
            if numstreak >= 10:
                numstreak += 20
            else:
                numstreak += 10
        if app.table[index].number == ((app.table[index+1].number)-1 or (app.table[index+1].number)+1): # check for staircase
            stairstreak += 10
        if app.table[index].suit == app.table[index+1].suit: # check for same suit
            if suitstreak >= 10:
                suitstreak += 20
            else:
                suitstreak += 10
        if app.table[index].number == ((app.table[index+1].number)-1 or (app.table[index+1].number)+1) and (app.table[index].suit == app.table[index+1].suit): # check for same suit and number(straight flush)
            prob += 50
    prob += suitstreak + numstreak + stairstreak # adds probability
    app.tableprob = prob

def aiProb(app): # calculates prob based on curdeck alone
    stairstreak = 0
    numstreak = 0
    suitstreak = 0
    for index in range(len(app.ai)-1): # for every card in curdeck
        if app.ai[index].number == app.ai[index+1].number: # checks for same number
            if numstreak > 10:
                numstreak += 20
            else:
                numstreak += 10
        if app.ai[index].number == ((app.ai[index+1].number)-1 or (app.ai[index+1].number)+1): # checks for staircase
            stairstreak += 10
        if app.ai[index].suit == app.ai[index+1].suit: # checks for same suit
            if suitstreak > 10:
                suitstreak += 20
            else:
                suitstreak = 10 
        if app.ai[index].number ==((app.ai[index+1].number)-1 or (app.ai[index+1].number)+1) and app.ai[index].suit == app.ai[index+1].suit: # checks for staircase and same suit(straight flush)
            app.aiprob = 0
            app.aiprob += 50
    app.aiprob = 0
    app.aiprob += numstreak + suitstreak + stairstreak
    

def hardAI(app):
    prob = 0
    testCards = [] # test cards to append back later in deck
    numstreak = 0
    suitstreak = 0
    stairstreak = 0
    success = 0 # successful trials
    fail = 0 # failed trials
    if app.aiprob == -1:
        aiProb(app)
    if app.betround > 1: # makes sure not first round
        tableProb(app)
        for tablecard in range(5-len(app.table)): # for every possible future table card
            for cards in range(len(app.players)-2): # removes 2 random cards per opponent
                randcard1 = random.choice(app.curdeck)
                randcard2 = random.choice(app.curdeck)
                testCards.append(randcard1)
                testCards.append(randcard2)
                app.curdeck.remove(randcard1)
                app.curdeck.remove(randcard2)
            for card in app.curdeck: # for every card in the deck after test cards removed
                # prob values based on value of each hand:
                for index in range(len(app.ai)-1):
                    if app.ai[index].number == card.number:
                        if numstreak == 10:
                            numstreak += 20
                        if numstreak == 30:
                            numstreak += 30
                        if numstreak == 60:
                            numstreak += 100
                        else:
                            numstreak += 10
                    if app.ai[index].suit == card.suit and app.ai[index].number == (card.number-1 or card.number+1):
                        prob += 50
                    elif app.ai[index].suit == card.suit:
                        if suitstreak == 30:
                            suitstreak += 70
                        elif suitstreak == 100:
                            suitstreak += 90
                        else:
                            suitstreak += 10
                    elif app.ai[index].number == ((card.number)-1 or card.number+1):
                        if stairstreak == 30:
                            stairstreak += 50
                        else:
                            stairstreak += 10
                prob += suitstreak + numstreak + stairstreak
                if (app.aiprob + prob + app.tableprob) >= 30:
                    success += 1
                    suitstreak = 0
                    numstreak = 0
                    stairstreak = 0
                else:
                    fail += 1
                    suitstreak = 0
                    numstreak = 0
                    stairstreak = 0
                prob = 0
        for test in testCards:
            app.curdeck.append(test)
        if success >= fail//2:
            bet(app, 25)
        elif success >= fail//3:
            bet(app, 10)
        elif success > fail:
            allin(app)
        else:
            rand = random.choice(range(5))
            if rand == 1:
                bet(app, 25)
            else:
                fold(app)
        success = 0
        fail = 0
    else:
        if app.curbet == 0: # bets 5 automatically if first round
            bet(app, 5)
        else:
            stand(app)

def easyAI(app): # simple takes basic prob calculators and uses it to make move
    if app.betround == 1:
        bet(app, 5)
        aiProb(app)
    else:
        tableProb(app)
        if app.tableprob > 10:
            bet(app, 5)
        elif app.tableprob > 20:
            bet(app, 10)
        elif app.tableprob > 30:
            bet(app, 10)
        elif app.tableprob > 40:
            bet(app, 25)
        elif app.tableprob > 50:
            bet(app, 100)

def bet(app, amount):
    if app.curplayer == 0 and app.betround != 5: 
        app.aiturn = True # displays what ai's bet is
    if app.money[app.curplayer] - amount >= 0: # makes sure player has enough money
        if amount >= app.curbet: # updates current highest bet
            app.validBet = True
            app.pot += amount # adds to pot
            app.money[app.curplayer] -= amount # subtracts from player's account
            app.curbet = amount
        else:
            app.validBet = False
    else:
        app.validBet = False
    if app.curplayer == 0 and app.validBet == True and app.betround != 5: # checks if curplayer is AI
        app.aiturn = True # shows AI's actions
        app.curplayer += 1
    elif app.curplayer < len(app.players)-1 and app.validBet == True: # checks if player that is not AI and not last player
        app.curplayer += 1
        app.transition = True # transition between players
    elif app.curplayer == len(app.players)-1 and app.validBet == True: # checks if last player
        app.betround += 1
        app.curbet = 0
        addCards(app) # adds cards to table
        app.curplayer = 0
        if app.difficult == True and app.betround != 5:
            hardAI(app) # AI's turn because AI automatically first
            app.aiturn = True
        elif app.difficult == False and app.betround != 5:
            easyAI(app)
            app.aiturn = True


def stand(app): # matches current highest bet
    if app.curbet != 0:
        bet(app, app.curbet)
    else:
        app.validbet = False

def allin(app): # bets amount of money left in player's bank
    bet(app, app.money[app.curplayer])

def invalidBet(app, canvas): # draws invalid bet message
    if app.validBet == False:
        canvas.create_text(app.width//2, app.height*(4.5/10), font= ("slab serif", 20), text="Invalid Bet")

def fold(app): # folds current player's deck(removed from game)
    app.money.pop(app.curplayer)
    app.players.pop(app.curplayer)

def checkFlush(app, player):
    curPlayer = app.ai
    if player == 0:
        curPlayer = app.ai
    else:
        curPlayer = app.player1
    suits = []
    for card in curPlayer:
        suits.append(card.suit)
    for cards in app.table:
        suits.append(cards.suit)
    for index in range(len(suits)-1):
        if suits.count(suits[index]) > app.suitcount:
            app.suitcount = suits.count(suits[index])
        else:
            pass

def checkPairs(app, player): # counts number of pairs indeck
    curPlayer = app.ai # just assignment of variable
    if player == 0:
        curPlayer = app.ai
    elif player == 1:
        curPlayer = app.player1
    elif player == 2:
        curPlayer = app.player2
    elif player == 3:
        curPlayer = app.player3
    pairs = []
    for card in curPlayer:
        pairs.append(card.number)
    for cards in app.table:
        pairs.append(cards.number)
    for index in range(len(suits)-1):
        if pairs.count(pairs[index]) > app.numcount:
            app.numcount = pairs.count(pairs[index]) # counts number of times a number occurs
        else:
            pass

def checkStairs(app, player):
    curPlayer = app.ai
    if player == 0:
        curPlayer = app.ai
    elif player == 1:
        curPlayer = app.player1
    elif player == 2:
        curPlayer = app.player2
    elif player == 3:
        curPlayer = app.player3
    stairs = []
    for card in curPlayer:
        stairs.append(card.number) # appends numbers in deck
    for cards in app.table:
        stairs.append(cards.number) # appends numbers in table
    stairs.sort() # puts it in order
    for index in range(len(suits)-1):
        if stairs.count(stairs[index]) == (stairs.count(stairs[index+1])-1 or stairs.count(stairs[index+1])+1):
            app.staircount += 1 # counts number of times stairs occur
        else:
            pass

def bestHand(app, player): # checks all hands
    checkFlush(app, player)
    checkPairs(app, player)
    checkStairs(app, player)

def compareHands(app):
    if len(app.players) == 1: # if everybody folds, then one automatic winner
        app.bestplayer = app.players[0]
    else:
        best = 0 # best hand value
        for player in range(len(app.players)): # for every player
            bestHand(app, player) # calculate values for each hand
            current = app.numcount # automatic, just assignment
            if app.staircount == 5 and app.suitcount == 5: # makes sure staircount is 5 and suitcount is 5 because that is the only time the hands are of value
                current = max(app.staircount, app.numcount, app.suitcount)
            elif app.staircount == 5 and app.suitcount != 5:
                current = max(app.staircount, app.numcount)
            elif app.staircount != 5 and app.suitcount == 5:
                current = max(app.suitcount, app.numcount)
            if current == app.staircount and app.numcount >= 4: # 4 pairs > 5 stairs
                current = app.numcount
            elif current == app.suitcount and app.numcount >= 4: # 4 pairs > 5 suits
                current = app.numcount
            elif current == app.suitcount and current == app.staircount and current >= 5: # tiebreaker between 5 suits and 5 stairs
                current = app.suitcount
            elif app.staircount == app.suitcount and app.suitcount == 5: # straight flush
                current = 8
            if current == app.staircount: # 5 stairs
                current = 4
            elif current == app.numcount: # values based on pairs
                if app.numcount <= 3:
                    current = app.numcount
                if app.numcount >= 4:
                    current = 7
            elif current == app.suitcount:
                current = 5
            if current > best: # replaces best with hand
                best = current
                app.bestplayer = app.players[player]
        app.paused = True # pauses game


#DRAWING:

def drawWinner(app, canvas): # draws winner of game, goes to new screen
    if app.bestplayer != '':
        canvas.create_rectangle(0, 0, app.width, app.height, fill="dark green")
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 30), text=f'Winner: {app.bestplayer}')

def backgroundTitle(app, canvas): # draws title and current player
    canvas.create_rectangle(0, 0, app.width, app.height, fill="dark green")
    canvas.create_text(app.width/2, app.height//20, font=("slab serif", 45), text="Poker")
    canvas.create_text(app.width//2, app.height//6, font=("slab serif", 30), text=f'Current Player: {app.players[app.curplayer]}')

def displayCards(app, canvas): # draws cards, table cards, pot, current player's total money, and betting denominations
    if app.difficult != None:
        canvas.create_rectangle(app.width*1/5, app.height*2/3, app.width*1/5+70, app.height*2/3+90 )
        if app.curplayer == 0:
            canvas.create_text((app.width*1/5+(app.width*1/5+70))//2,(app.height*2/3+app.height*2/3+90)//2, text=app.ai[0])
            canvas.create_text((app.width*2/3+70+app.width*2/3)//2,(app.height*2/3+ app.height*2/3+90)//2, text=app.ai[1])
        elif app.curplayer == 1:
            canvas.create_text((app.width*1/5+(app.width*1/5+70))//2,(app.height*2/3+app.height*2/3+90)//2, text=app.player1[0])
            canvas.create_text((app.width*2/3+70+app.width*2/3)//2,(app.height*2/3+ app.height*2/3+90)//2, text=app.player1[1])
        elif app.curplayer == 2:
            canvas.create_text((app.width*1/5+(app.width*1/5+70))//2,(app.height*2/3+app.height*2/3+90)//2, text=app.player2[0])
            canvas.create_text((app.width*2/3+70+app.width*2/3)//2,(app.height*2/3+ app.height*2/3+90)//2, text=app.player2[1])
        elif app.curplayer == 3:
            canvas.create_text((app.width*1/5+(app.width*1/5+70))//2,(app.height*2/3+app.height*2/3+90)//2, text=app.player3[0])
            canvas.create_text((app.width*2/3+70+app.width*2/3)//2,(app.height*2/3+ app.height*2/3+90)//2, text=app.player3[1])
        if app.betround > 1:
            for index in range(len(app.table)):
                canvas.create_rectangle(app.width*(index+1)/7, app.height//4, app.width*(index+1)/7+70, app.height//4+90)
                canvas.create_text((app.width*(index+1)/7+app.width*(index+1)/7+70)//2, (app.height//4+app.height//4+90)//2, text = app.table[index])
        canvas.create_rectangle(app.width*2/3, app.height*2/3, app.width*2/3+70, app.height*2/3+90)
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 25), text=f'Pot: ${app.pot}')
        canvas.create_text(app.width//2, app.height*(6/10), font=("slab serif", 25), text=f'Current Bet: ${app.curbet}')
        canvas.create_text(app.width//2, app.height*(9/10), font=("slab serif", 25), text=f'Total Money: ${app.money[app.curplayer]}')
        canvas.create_text(app.width//2, app.height*(6.5/10), font=("slab serif", 10), text=f'Betting Denominations: 1 = $1, 2 = $5, 3 = $10, 4 = $25, 5 = $50, 6 = $100')

def displayAI(app, canvas): # draws AI's actions to inform other players what AI did
    if app.aiturn == True and app.betround != 4:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="dark green")
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 45), text="AI's Turn")
        canvas.create_text(app.width//2, app.height*(2/3), font=("slab serif", 30), text=f'The AI bet ${app.curbet}')
        canvas.create_text(app.width//2, app.height*(3/4), font=("slab serif", 20), text=f'Press c to continue')

def transition(app, canvas): # transition between players
    if app.transition == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="dark green")
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 45), text=f'Next Player: {app.players[app.curplayer]}')
        canvas.create_text(app.width//2, app.height*(2/3), font=("slab serif", 30), text=f'Press c to continue')
    
def drawDifficulty(app, canvas): # prompts for difficulty from player(s)
    if app.difficult == None and app.playing == True:
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 20), text="Press h for hard difficulty and e for easy difficulty")

def drawPlayers(app, canvas): # asks for number of players
    if app.playing == False:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="dark green")
        canvas.create_text(app.width//2, app.height//2, font=("slab serif", 20), text="Press a to add a player, press d when you are done")
        canvas.create_text(app.width//2, app.height//2+20, font=("slab serif", 20), text="Only 3 players are allowed")



def keyPressed(app, event):
    if event.key == 'r': # reset
        appStarted(app)
    if event.key == 'c' and app.aiturn == True: # continue from AI turn
        app.aiturn = False
    if event.key == 'c' and app.transition == True: # continue from transition
        app.transition = False  
    if app.difficult == None:
        if event.key == 'h': # hard difficulty
            app.difficult = True
            hardAI(app)
            app.aiturn = True 
        if event.key == 'e': # easy difficulty
            app.difficult = False
            easyAI(app)
            app.aiturn = True
    if app.playing == False and len(app.players)<4:
        if event.key == 'a': # add player
            app.players.append(f'Player{len(app.players)}')
            app.money.append(500)
        if event.key == 'd': # done/continue/start game
            generateDecks(app)
            app.playing = True
    if app.playing == False and len(app.players) == 4: # if max number of players, start game
        generateDecks(app)
        app.playing = True
    if app.paused == False and app.difficult != None and app.playing == True and app.transition == False and app.aiturn == False: # checks if difficulty and number of players have been chosen
        if event.key == 'b': # start betting 
            app.betting = True
        if event.key == 's': # match previous bet
            stand(app)
        if event.key == 'a': # go "all-in"(bet all money in account)
            allin(app)
        if app.betting == True:
            if event.key == '1': # bet $1
                bet(app, 1)
            if event.key == '2': # bet $5
                bet(app, 5)
            if event.key == '3': # bet $10
                bet(app, 10)
            if event.key == '4': # bet $25 
                bet(app, 25)
            if event.key == '5': # bet $50
                bet(app, 50)
            if event.key == '6': # bet $100
                bet(app, 100)
        if event.key == 'f' and app.players[app.curplayer] != 'AI': # makes sure not AI's turn when folding
            fold(app)
            compareHands(app)

def redrawAll(app, canvas): # makes sure everything is being drawn
    backgroundTitle(app, canvas)
    displayCards(app, canvas)
    drawDifficulty(app, canvas)
    drawWinner(app, canvas)
    drawPlayers(app, canvas)
    displayAI(app, canvas)
    transition(app, canvas)
    invalidBet(app, canvas)

def main():
    runApp(width=500, height=500)

if __name__ == '__main__':
    main()