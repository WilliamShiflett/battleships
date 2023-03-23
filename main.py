import copy
import random

class GameBoard(object):

    def __init__(self, battleships, width, height):
        self.battleships = battleships
        self.shots = []
        self.width = width
        self.height = height

    def take_shot(self, shot_location):
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                break

        self.shots.append(Shot(shot_location, is_hit))

    def is_game_over(self):
        return all([b.is_destroyed() for b in self.battleships])
            
        #for each battleship, is it destroyed?

class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit

class Battleship(object):
    '''
    @staticmethod refers to a method called on the class itself, i.e.:
    
    b = Battleship.build((1,2), 5, "S")
    
    a "non-static method" refers to a method called on an instance of a class, i.e.:

    b.build, 
    
    which doesn't make sense, because b is an instance of the class "Battleship"
    '''
    @staticmethod
    def build(head, length, direction):

        body = []

        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "E":
                el = (head[0] + i, head[1])
            elif direction == "W":
                el = (head[0] - i, head[1])
            body.append(el)

        return Battleship(body, direction)

    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None
        
    def is_destroyed(self):
        return all(self.hits)

class Player(object):
    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f

def render(game_board, show_battleships=False):
    header = "+" + "-" * game_board.width + "+"
    
    print(header)
    

    #create a grid of height by width with the value "None" for each
    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])

    #replace the value "None" with "O" wherever there are battleships
    if show_battleships:
        for b in game_board.battleships:
            for i, (x,y) in enumerate(b.body):
                if b.direction == 'N':
                    chs = ('v','|','^')
                elif b.direction == 'S':
                    chs = ('^','|','v')
                elif b.direction == 'W':
                    chs = ('>','=','<')
                elif b.direction == 'E':
                    chs = ('<','=','>')
                else:
                    raise 'Unknown direction'

                if i == 0:
                    ch = chs[0]
                elif i == len(b.body) - 1:
                    ch = chs[2]
                else:
                    ch = chs[1]
                board[x][y] = ch
    
    #rplace the value "None" or "O" with "X" whenever there is a shot
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "."
        board[x][y] = ch

    #replace the "None" values with " ", join all of the elements in each row of the board and print the rows

    for y in range(game_board.height):
        row =[]
        for x in range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)

def get_random_ai_shot(game_board):
    # random.randint(a, b)
    x = random.randint(0, game_board.width - 1)
    y = random.randint(0, game_board.height - 1)
    return (x, y)

#Todo, make actual clever AI
def get_clever_ai(game_board):
    return(0,0)

def get_human_shot(game_board):
    inp = input("Where do you want to shoot?\n")
    xstr, ystr = inp.split(",")
    x = int(xstr)
    y = int(ystr)

    return(x, y)

if __name__ == "__main__":

    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]

    game_boards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    # Pass in the name of the player and the shot getting function itself
    players = [
        Player("Rob", get_human_shot),
        Player("Alice", get_random_ai_shot)
    ]

    offensive_idx = 0
    while True: 
        # make defensive_idx the opposite of offensive_idx
        defensive_idx = (offensive_idx + 1) % 2

        defensive_board = game_boards[defensive_idx] 

        offensive_player = players[offensive_idx]

        print('%s YOUR TURN!' % offensive_player.name)

        shot_location = offensive_player.shot_f(defensive_board)

        defensive_board.take_shot(shot_location)

        render(defensive_board, True)

        if defensive_board.is_game_over():
            print('%s WINS!' % offensive_player.name)
            break

        offensive_idx = defensive_idx

        # if game_has_ended:
        #   print('You win')
        #   break
