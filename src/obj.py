class Card:
   def __init__(self, rank, suit):
      #rank must be an integer. suit must be representable as a one-character string.
      self.rank = rank
      self.suit = suit
      self.faceup = False

   def __str__(self, prefs = None, color_code = None):
      """Two-letter string representation of the card. prefs is a list of one-character strings, one per rank."""
      if not self.faceup:
         return "XX"
      if prefs is None:
         prefs = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
      if color_code is None:
         color_code = {
         "D": "\033[1;31m",
         "C": "\033[1;30m",
         "H": "\033[22;31m",
         "S": "\033[2;30m"
         }
      return color_code[str(self.suit)]+prefs[self.rank-1]+str(self.suit)+"\033[0m"

   def __eq__(self, other):
      return self.rank == other.rank and self.suit == other.suit


   def flip(self):
      self.faceup = not self.faceup


class Deck:
   

   def __init__(self, ranks=range(1,14), suits=["H", "C", "D", "S"], cards=None):
      #the deck is represented by a stack (last element is the top)
      if cards is None:
         self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
      else:
         self.cards = cards

      self.size = len(self.cards)

   def __len__(self):
      return self.size

   def __getitem__(self, n):
      return self.cards[n]

   def index(self, card):
      return self.cards.index(card)

   def splice_from(self, card):
      idx = self.cards.index(card) #will return a ValueError if card is not in the list!!!
      result = self.cards[idx:]
      self.cards = self.cards[:idx]
      self.size = idx
      return result

   def splice_from_position(self, idx):
      result = self.cards[idx:]
      self.cards = self.cards[:idx]
      self.size = idx
      return result


   def shuffle(self):
      import random
      random.shuffle(self.cards)

   def deal(self, n=1, flip=False):
      self.size -= n
      if not flip: 
         return [self.cards.pop() for i in range(n)]
      else:
         tmp = [self.cards.pop() for i in range(n)]
         for card in tmp: card.flip()
         return tmp

   def add(self, card):
      #add a Card or list of Cards
      try:
         self.cards.extend(card)
         self.size += len(card)
      except:
         self.cards.append(card)
         self.size += 1

   def flip(self):
      self.cards = self.deal(self.size, flip=True)
