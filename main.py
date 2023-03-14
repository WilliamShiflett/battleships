import copy

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

        return Battleship(body)

    def __init__(self, body):
        self.body = body
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None
        
    def is_destroyed(self):
        return all(self.hits)

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
            for x,y in b.body:
                board[x][y] = "O"
    
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

if __name__ == "__main__":

    battleships = [
        Battleship.build((1,1), 2, "N"),
        # Battleship.build((5,8), 5, "N"),
        # Battleship.build((2,3), 4, "E")
    ]

    game_boards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    player_names = [
        "Frank",
        "Alice"
    ]

    offensive_idx = 0
    while True: 
        # make defensive_idx the opposite of offensive_idx
        defensive_idx = (offensive_idx + 1) % 2

        defensive_board = game_boards[defensive_idx] 

        print('%s YOUR TURN!' % player_names[offensive_idx])
        inp = input("Where do you want to shoot?\n")
        xstr, ystr = inp.split(",")
        x = int(xstr)
        y = int(ystr)

        defensive_board.take_shot((x,y))
        render(defensive_board)

        if defensive_board.is_game_over():
            print('%s WINS!' % player_names[offensive_idx])
            break

        offensive_idx = defensive_idx

        # if game_has_ended:
        #   print('You win')
        #   break
