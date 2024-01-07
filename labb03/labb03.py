import random

class Card:
    def __init__(self, suit, value):
        assert 1 <= suit <= 4 and 1 <= value <= 13
        self.suit = suit
        self.value = value

    def getValue(self):
        return self.value 

    def getSuit(self):
        return self.suit

    def __str__(self):
        suits= {1:"Hearts", 2:"Diamonds", 3:"Clubs", 4:"Spades"}
        values= {1:"Ace",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10",11:"Jack",12:"Queen",13:"King"}
        if self.suit in suits and self.value in values:#finns dem i arrayen
            return f"{values[self.value]} of {suits[self.suit]}"


class CardDeck:
    def __init__(self):
        self.reset()

    def shuffle(self):
        random.shuffle(self.myCards)


    def getCard(self):
        if self.size()>0:
            card=self.myCards[-1]
            self.myCards.pop()
            return card
        else:
            return None

    def size(self):
        return len(self.myCards)

    def reset(self):
        self.myCards=[]
        for i in range(1,5):
            for j in range(1,14):
                card=Card(i,j)
                self.myCards.append(card)

deck = CardDeck()
deck.shuffle()
while deck.size()>0:
    card = deck.getCard()
    print(f"Card {card} has value {card.getValue()}")