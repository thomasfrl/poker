class Card:
	def __init__(self, s):
		assert len(s) == 2, "argument not valid for this card"
		assert s[0] in ["2","3","4","5","6","7","8","9", "T", "J", "Q", "K","A"] , "card has incorrect value"
		assert s[1] in ["H", "C", "S", "D"], "card has incorrect color"

		if s[0] == "T":
			nb = 10
		elif s[0] == "J":
			nb = 11
		elif s[0] == "Q":
			nb = 12
		elif s[0] == "K":
			nb = 13
		elif s[0] == "A":
			nb = 14
		else:
			nb = int(s[0])
		self.value = nb
		self.color = s[1]

class Hand:

	def __init__(self, cards):
		assert len(cards) == 5, "not enough card in that hand"
		for card in cards:
			assert type(card) == Card, "the argument should be a list of cards"
		self.cards = cards
		self._evaluate()

	def _evaluate(self):
		straight = self._straight() #determine if the hand is a straight, return the highest value if it is the case
		flush = self._flush() #determine if the hand is a flush, return the highest value if it is the case
		if straight:
			if flush:
				if flush == 14 :
					self._rank = 9 # royal flush
				else :					
					rank = 8 # straight flush
					self._values = [straight]
			else:
				self._rank = 4 #straight
				self._values = [straight]
		elif flush:
			self._rank = 5 # flush
			self._values = [flush]
		else :
			same_values = self._same_values() #determine is there is cards in the hand which have the same value, assign rank and values			


	def _flush(self):
		if all(card.color == self.cards[0].color for card in self.cards):
			return max([card.value for card in self.cards])
		else :
			return False

	def _straight(self):
		cards = [card.value for card in self.cards]
		cards.sort()
		for i in range(4) :
			if cards[i] +1 != cards[i+1]  : return False

		return cards[-1]

	def _same_values(self):
		cards = [card.value for card in self.cards]
		same_values = []
		highest_values = []
		rank = 0
		i = 0
		while True:
			try:
				cards[i]
			except :
				break
			else:
				same_value = [card for card in cards if card == cards[i]]
				if len(same_value) > 1 :
					same_values.append({'nb' :len(same_value), "value": cards[i]})
					if len(same_values) == 2:
						if same_values[0]['nb'] > same_values[1]['nb'] :
							highest_values.append(cards[i])
							rank = 6
						elif same_values[0]['nb'] < same_values[1]['nb'] :
							highest_values.insert(0,cards[i])
							rank = 6
						else:
							rank = 2
							if same_values[0]['value'] > same_values[1]['value'] :
								highest_values.append(cards[i])
							elif same_values[0]['value'] <= same_values[1]['value'] :
								highest_values.insert(0,cards[i])
					else:
						highest_values.append(cards[i])
						if len(same_value) == 2:
							rank = 1
						elif len(same_value) == 3:
							rank = 3
						else :
							rank = 7
					for card in same_value:
						cards.remove(card)
				i += 1

		cards.sort(reverse=True)
		highest_values += cards
		self._rank = rank
		self._values = highest_values

		
	@property
	def rank(self):
		return self._rank
	
	@property
	def values(self):
		return self._values
		


class Set:
	def __init__(self, arg):
		assert type(arg) == str
		cards = [Card(s) for s in arg.split()]
		self.hand_1 = Hand(cards[0:5])
		self.hand_2 = Hand(cards[5:10])

	def winner(self):
		if self.hand_1.rank > self.hand_2.rank : 
			return "player 1"
		elif self.hand_2.rank > self.hand_1.rank :
			return "player 2"
		else:
			i = 0
			while self.hand_1.values[i] == self.hand_2.values[i]:
				i += 1
			if self.hand_1.values[i] > self.hand_2.values[i]:
				return "player 1"
			else :
				return "player 2"

def main():
	f = open("poker.txt", "r")
	victory = 0
	for line in f:
		s = Set(line)
		print(line)
		if s.winner() == "player 1" : 
			# print(s.hand_1.values)
			# print(s.hand_1.rank)
			# print(s.hand_2.values)
			# print(s.hand_2.rank)
			victory += 1 
	f.close()
	print("number of victory of player 1 :")
	print(victory)
	

main()