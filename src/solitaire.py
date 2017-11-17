#!/usr/bin/env python
from obj import Card, Deck

RULES = "The initial array may be changed by \"building\" - transferring cards "+\
       "among the face-up cards in the tableau. Certain cards of the tableau can be played at once, "+\
       "while others may not be played until certain blocking cards are removed. For example, of the"+\
       " seven cards facing up in the tableau, if one is a red nine and another is a black ten, you may transf"+\
       "er the nine to on top of the ten to begin building that pile in sequence. Since you have mov"+\
       "ed the nine from one of the seven piles, you have now unblocked a face down card; this card "+\
       "can be turned over and now is in play.\nAs you transfer cards in the tableau and begin build"+\
       "ing sequences, if you uncover an ace, the ace should be placed in one of the foundation pile"+\
       "s. The foundations get built by suit and in sequence from ace to king.\nContinue to transfer"+\
       " cards on top of each other in the tableau in sequence. If you can't move any more face up c"+\
       "ards, you can utilize the stock pile by flipping over the first card. This card can be playe"+\
       "d in the foundations or tableau. If you cannot play the card in the tableau or the foundatio"+\
       "ns piles, move the card to the waste pile and turn over another card in the stock pile.\nIf "+\
       "a vacancy in the tableau is created by the removal of cards elsewhere it is called a \"space"+\
       "\", and it is of major importance in manipulating the tableau. If a space is created, it can"+\
       " only be filled in with a king. Filling a space with a king could potentially unblock one of"+\
       " the face down cards in another pile in the tableau.\nContinue to transfer cards in the tabl"+\
       "eau and bring cards into play from the stock pile until all the cards are built in suit sequ"+\
       "ences in the foundation piles to win! In this version, you automatically win if you reveal all cards in the tableau.\n"
MOVES = "These are the legal commands you can use.\n"+ \
"\'help\': Displays rules and moves\n"+\
"\'rules\': Displays the rules\n"+\
"\'moves\': Displays the list of commands\n"+\
"\'build <card> <pile1> <pile2>\': Moves the chosen card from pile1 to the top of pile2 [UNIMPLEMENTED]\n"+\
"\'add <pile>\': Moves the top card of the waste to the top of the chosen pile [UNIMPLEMENTED]\n"+\
"\'score <pile>\': Moves the top card of the chosen pile to its appropriate foundation. Use 'score waste' to score directly from the waste pile\n"+\
"\'draw\': Flips the next three cards of the deck onto the waste\n"+\
"\'draw1\': Flips the next card of the deck onto the waste\n"+\
"\'undo\': Undoes the last move\n"+\
"\'redeal\': Starts the game over with the same configuration\n"+\
"\'restart\': Restarts the game with a fresh shuffle\n"

class Board:
   def __init__(self, board=None):
      #set up the board
      if board is None:
         self.deck = Deck()
         self.deck.shuffle()
         self.foundations = [Deck([],[]),Deck([],[]),Deck([],[]),Deck([],[])]
         self.waste = Deck([],[])
         self.tableau = [Deck(cards=self.deck.deal(n)) for n in range(1,8)]
         for column in self.tableau:
            column[-1].flip()
      else:
         #copy constructor
         import copy
         #NOT COMPLETE: THIS WILL NOT CREATE A NEW INSTANCE OF THESE OBJECTS
         self.deck = copy.deepcopy(board.deck)
         self.foundations = copy.deepcopy(board.foundations)
         self.waste = copy.deepcopy(board.waste)
         self.tableau = copy.deepcopy(board.tableau)

   def display_board(self):
      
      #display the foundations
      line = "\033[1;30;47m"
      for pile in self.foundations:
         line += str(pile[-1])+"\033[1;30;47m " if len(pile)>0 else "\033[1;30;47m-- "
      
      #separator
      line += "|  "

      #print the waste
      line += "-- " if len(self.waste) == 0 else str(self.waste[-1])+"\033[1;30;47m "


      #display the deck
      line += "\033[1;30;47m--\033[0m(0)" if len(self.deck) == 0 else ("\033[1;30;47mXX \033[0m("+str(len(self.deck))+")")
 
      print line
      #print "~"*20
      print "\033[1;30;47m 1  2  3  4  5  6  7 \033[0m"

      #display the tableau
      level = 0
      maxlevel = False
      while (not maxlevel):
         line = "\033[22;35;42m"
         maxlevel = True
         for pile in self.tableau:
            if level >= len(pile):
               line += "   "
            else:
               maxlevel = False
               #color = color_code[pile[level].suit] if pile[level].faceup else "\033[22;35;42m"
               line += str(pile[level]) + "\033[22;35;42m "
         print line + "\033[0m"
         level += 1

      #done!

   def victory_state(self):
    # if all the foundations are full, you win!
    try:
      if (self.foundations[0][-1].rank == 13 and self.foundations[0][-1].rank == 13 and self.foundations[0][-1].rank == 13 and
          self.foundations[0][-1].rank == 13):
        return True
      else:
        return False
    except:
      return False

   def auto_win(self):
    #loop through the tableau
    #if every card is faceup, the game is trivially winnable
    for pile in self.tableau:
      if len(pile) > 0:
        for card in pile:
          if not card.faceup:
            return False

    return True


if __name__ == "__main__":

   #construct board
   b = Board()
   history = []
   victory = False

   while(1):

      b.display_board()
      move = raw_input("Make a move ('moves' for options): ").split()

      if len(move) == 0: continue

      if (move[0].lower() == "quit" or move[0].lower() == "q"): 
         break

      if (move[0].lower() == "help" or move[0].lower() == "h"):
         print RULES
         print MOVES

      if (move[0].lower() == "rules" or move[0].lower() == "rl"):
         print RULES

      if (move[0].lower() == "moves" or move[0].lower() == "m"):
         print MOVES

      if (move[0].lower() == "redeal" or move[0].lower() == "rd"):
         if len(history) > 0:
            b = history[0]
            history = []

      if (move[0].lower() == "restart" or move[0].lower() == "r"):
         b = Board()
         history = []

      if (move[0].lower() == "undo" or move[0].lower() == "shit" or move[0].lower() == "fuck" or 
          move[0].lower() == "oops" or move[0].lower() == "u"):
         if len(history) > 0: #there needs to be something to undo
            b = history.pop()

      if (move[0].lower() == "draw" or move[0].lower() == "draw3" or move[0].lower() == "d" or move[0].lower() == "d3"):
         if len(b.deck) >= 3:
            history.append(Board(b))
            b.waste.add(b.deck.deal(min(3,len(b.deck)),flip=True))
         else:
            if len(b.waste) == 0: #out of cards in both deck and waste
               continue
            else:
               history.append(Board(b))
               b.deck.add(b.waste.deal(len(b.waste),flip=True)) #flip the waste back onto the deck
               b.waste.add(b.deck.deal(min(3,len(b.deck)),flip=True))

      if (move[0].lower() == "draw1" or move[0].lower() == "d1"):
         if len(b.deck) >= 1: #if there are any cards in the deck, flip one
            history.append(Board(b))
            b.waste.add(b.deck.deal(flip=True))
         else:
            if len(b.waste) > 0: #if there are no cards left in the deck, flip the waste back
               history.append(Board(b))
               b.deck.add(b.waste.deal(len(b.waste),flip=True))
               b.waste.add(b.deck.deal(flip=True))
            else:
               continue


      if (move[0].lower() == "score" or move[0].lower() == "s"):
       try:
        pile = b.tableau[int(move[1])-1] if (move[1].lower() != "waste" and move[1].lower() != "w") else b.waste
        card = pile[-1]
        #FOUNDATION ORDER: D C H S
        if card.suit == "D":
         if card.rank == 1 or card.rank - b.foundations[0][-1].rank == 1:
            history.append(Board(b))
            b.foundations[0].add(pile.deal()) #add the card to the foundation
        if card.suit == "C":
         if card.rank == 1 or card.rank - b.foundations[1][-1].rank == 1:
            history.append(Board(b))
            b.foundations[1].add(pile.deal()) #add the card to the foundation
        if card.suit == "H":
         if card.rank == 1 or card.rank - b.foundations[2][-1].rank == 1:
            history.append(Board(b))
            b.foundations[2].add(pile.deal()) #add the card to the foundation
        if card.suit == "S":
         if card.rank == 1 or card.rank - b.foundations[3][-1].rank == 1:
            history.append(Board(b))
            b.foundations[3].add(pile.deal()) #add the card to the foundation

        if len(pile) > 0:
         pile[-1].faceup = True

       except:
        continue

      if (move[0].lower() == "add" or move[0].lower() == "a"):
         try:
            pile = b.tableau[int(move[1])-1]
            #add a king to a space
            if b.waste[-1].rank == 13 and len(pile) == 0:
               history.append(Board(b))
               pile.add(b.waste.deal())
               continue
            #add any other card to a pile if legal
            if (
               ((b.waste[-1].suit == "S" or b.waste[-1].suit == "C") and 
                 (pile[-1].suit == "H" or pile[-1].suit == "D")
                ) or (
                (b.waste[-1].suit == "H" or b.waste[-1].suit == "D") and 
                 (pile[-1].suit == "S" or pile[-1].suit == "C"))
               ) and pile[-1].rank - b.waste[-1].rank == 1:
               history.append(Board(b))
               pile.add(b.waste.deal())
         
         except:
            continue

      if (move[0].lower() == "build" or move[0].lower() == "b"):
        try:
          rank_conv = {
          "A":1,"a":1,
          "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
          "T":10,
          "J":11,
          "Q":12,
          "K":13
          }
          #card = Card(rank_conv[move[1][0].upper()],move[1][1].upper())
          pile1 = b.tableau[int(move[1])-1]
          pile2 = b.tableau[int(move[2])-1]
          

          #card needs to be faceup in pile1
          
          for idx,card in enumerate(pile1):
            if card.faceup:
              #put a king onto a blank
              if card.rank == 13 and len(pile2) == 0:
                history.append(b)
                pile2.add(pile1.splice_from_position(idx))
              #check for valid move
              if (
                 ((card.suit == "S" or card.suit == "C") and 
                   (pile2[-1].suit == "H" or pile2[-1].suit == "D")
                  ) or (
                  (card.suit == "H" or card.suit == "D") and 
                   (pile2[-1].suit == "S" or pile2[-1].suit == "C"))
                 ) and pile2[-1].rank - card.rank == 1:
                history.append(b)
                pile2.add(pile1.splice_from_position(idx))
              if len(pile1) > 0:
                pile1[-1].faceup = True
        except:
          continue

      if move[0].lower() == "auto" or move[0].lower() == "autowin":
        try:
          victory = b.auto_win();
        except:
          continue

      #check victory
      victory = victory or b.victory_state()
      if victory:
        print "CONGRATULATIONS!!! YOU WON!!!"
        replay = raw_input("Would you like to play again? [y/n/same deck (sd)] ")
        if replay.lower() == "y" or replay.lower() == "yes":
          b = Board()
          history = []
          continue
        elif replay.lower() == "same deck" or replay.lower() == "samedeck" or replay.lower() == "same_deck" or replay.lower() == "sd":
          b = history[0]
          history = []
          continue
        else:
          break;
