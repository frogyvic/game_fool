from enum import Enum
import random
from typing import List


class Suit(Enum):
    HEARTS="H"
    DIAMONDS="D"
    SPADES="S"
    CLUBS="C"

class Card:
    def __init__(self,name:str,value:int,suit:Suit()):
        self.name =name
        self.value=value
        self.suit=suit
    def __repr__(self):
        return f"[{self.name} of {self.suit.value}]"
    def __eq__(self, other):
        return self.value==other.value if isinstance(other,Card) else False

class Deck:
    @staticmethod
    def shuffle_deck(deck:List[Card]):
        shuffled_deck=deck.copy()
        random.shuffle(shuffled_deck)
        return shuffled_deck

class Player:
    def __init__(self, name: str, hand: List[Card] = None):
        self.name = name
        self.hand = hand if hand is not None else []
    def __repr__(self):
        return f"Player {self.name}, {self.hand}"

class Game:
    def __init__(self,cards_in_hand,trump:Suit()):
        self.name="Fool"
        self.cards_in_deck=36
        self.cards_in_hand=cards_in_hand
        self.deck=[]
        self.trump=trump
        self.create_deck()
    def __repr__(self):
        return (f"\033[35mкозырь-{self.trump.name}\033[0m")
    def create_deck(self):
        card_values = [("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("Jack", 11), ("Queen", 12),
                   ("King", 13), ("Ace", 14)]
        suits=[]
        for suit in Suit:
            for name, value in card_values:
                self.deck.append(Card(name, value, suit))
        for suit in Suit:
            suits.append(suit)
        self.trump=random.choice(suits)
    def replenish_hand(self,pl1:Player,pl2:Player):
        """Пополняет руки игроков из колоды до cards_in_hand"""
        if (pl1.hand==pl2.hand):
            pl1.hand=self.deck[:self.cards_in_hand]
            self.deck=self.deck[self.cards_in_hand:]
            pl2.hand=self.deck[:self.cards_in_hand]
            self.deck=self.deck[self.cards_in_hand:]
        for player in [pl1, pl2]:
            if len(player.hand) < self.cards_in_hand and self.deck:
                missing = self.cards_in_hand - len(player.hand)
                take = min(missing, len(self.deck))

                player.hand.extend(self.deck[:take])
                self.deck = self.deck[take:]
                self.cards_in_deck = len(self.deck)

                print(f"{player.name} взял {take} карт из колоды")
    def card_beat(self,atack:Card,defend:Card):
        if (atack.suit != defend.suit and defend.suit != self.trump):
            return 0
        elif (atack.suit == defend.suit and defend.value > atack.value) or (defend.suit == self.trump and atack.suit != self.trump):
            return 1
        else:
            return 0
    def fight(self,atacker:Player,defender:Player):
        print("\033[33mАтакующий",atacker.name,"защищающийся",defender.name,"\033[0m")
        end=False
        cards_on_desk=[]
        while (end!=True):
            print(f"\033[33m{atacker.name},выберите карту(1-{len(atacker.hand)}/0 чтобы закончить ход)\033[0m")
            for i in atacker.hand:
                print(i)
            index_atack=None
            while (index_atack not in range(-1,len(atacker.hand)+1)):
                index_atack=input()
                try:
                    index_atack=int(index_atack)
                    index_atack -= 1
                except ValueError:
                    print(f"некорректный ввод, введите(1-{len(atacker.hand)}/0 чтобы закончить ход)")
            if index_atack==(-1):
                print("ход завершен")
                self.replenish_hand(atacker,defender)
                return 1
            cards_on_desk.append(atacker.hand[index_atack])
            print("=" * 20)
            print(f"\033[31m{atacker.hand[index_atack]}\033[38m")

            print(f"{defender.name},выберите карту, чтобы отбиться(1-{len(defender.hand)}/0 чтобы взять карту)")
            for i in defender.hand:
                print(i)
            index_defend = None
            while True:
                try:
                    index_defend = int(input())
                    if index_defend == 0:
                        print("Вы решили забрать карту")
                        for i in cards_on_desk:
                            defender.hand.append(i)
                        atacker.hand.pop(index_atack)
                        self.replenish_hand(atacker,defender)
                        print("="*20)
                        return 0
                    elif 1 <= index_defend <= len(defender.hand):
                        index_defend -= 1
                        result = self.card_beat(atacker.hand[index_atack], defender.hand[index_defend])

                        if result == 0:
                            print("Эта карта не может отбить атакующую! Попробуйте другую.")
                            continue
                        elif result == 1:
                            print("Вы успешно отбились!")
                            cards_on_desk.append(defender.hand[index_defend])
                            atacker.hand.pop(index_atack)
                            defender.hand.pop(index_defend)
                            break
                    else:
                        print(f"Некорректный ввод. Введите число от 1 до {len(defender.hand)} или 0")
                except ValueError:
                    print(f"Некорректный ввод. Введите число от 1 до {len(defender.hand)} или 0")



g=Game(4,"HEARTS")
pl1=Player("Vic")
pl2=Player("Jack")
g.deck=Deck.shuffle_deck(g.deck)
g.replenish_hand(pl1,pl2)
print(g,end=" ")
move=0
while(len(pl1.hand)>0 or len(pl2.hand)>0):
    match(move):
        case 0:
            move=g.fight(pl1,pl2)

        case 1:
            move=g.fight(pl2,pl1)
if len(pl1.hand)==0:
    print(f"{pl1.name} победил!")
else:
    print(f"{pl2.name} победил!")

    

    
    



