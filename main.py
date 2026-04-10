class BaseSymbol():
    def __init__(self):
        self.name = ''
    def __repr__(self):
        return f'sym is {self.name}'
    def fight(self):
        return
class Rock(BaseSymbol):
    def __init__(self):
        super().__init__()
        self.name = "rock"
    def fight(self,symbol):
        if symbol == "scissors":
            return 1
        else:
            return 0
class Paper(BaseSymbol):
    def __init__(self):
        super().__init__()
        self.name = "paper"
    def fight(self,symbol):
        print(symbol)
        if symbol == "rock":
            return 1
        else:
            return 0
class Scissors(BaseSymbol):
    def __init__(self):
        super().__init__()
        self.name = "scissors"
    def fight(self,symbol):
        if symbol == "paper":
            return 1
        else:
            return 0
class Player():
    def __init__(self,name):
        self.name = name
        self.symbol = Scissors()
    def __repr__(self):
        return f'Player {self.name},{self.symbol}'
    def set_symbol(self,symbol):
        self.symbol = symbol
class Game():
    def __init__(self,pl1,pl2):
        self.player1 =pl1
        self.player2 =pl2
        self.counter = [0,0]
    def __repr__(self):
        return f'{self.player1}-{self.counter[0]},{self.player2}-{self.counter[1]}'
    def sym_compare(self,pl1:Player,pl2:Player):
        if((pl1.symbol.fight(pl2.symbol))==1):
            print(f"{pl1.name} wins!")
            self.counter[0] += 1
        elif((pl2.symbol.fight(pl1.symbol.name))==1):
            print(f"{pl2.name} wins!")
            self.counter[1] += 1
        else:
              print("drow")


pl1=Player("Vic")
pl2=Player("Jim")
pl1.set_symbol(Rock())
pl2.set_symbol(Paper())
print(pl1)
print(pl2)
g=Game(pl1.name,pl2.name)
g.sym_compare(pl1,pl2)
print(g)
breakpoint()