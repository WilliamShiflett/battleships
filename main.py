class GameBoard(object):

    def __init__(self, battleships, board_width, board_height):
        self.battleships = battleships
        self.shots = []
        self.board_width = board_width
        self.board_height = board_height

    def take_shot(self, shot_location):
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                break

        self.shots.append(Shot(shot_location, is_hit))





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
    
    hich doesn't make sense, because b is an instance of the class "Battleship"
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


def render(board_width: int, board_height: int, shots: list):
    header = "+" + "-" * board_width + "+"
    print(header)

    shots_set = set(shots)

    for y in range(board_height):
        row = []
        for x in range(board_width):
            if (x,y) in shots_set:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|")

    print(header)

def render_battleships(board_width, board_height, battleships):
    header = "+" + "-" * board_width + "+"
    
    print(header)
    
    board = []

    #create a grid of board_height by board_width with the value "None" for each

    for _ in range(board_width):
        board.append([None for _ in range(board_height)])

    #replace the value "None" with "O" wherever there are battleships

    for b in battleships:
        for x,y in b.body:
            board[x][y] = "O"

    #replace the "None" values with " ", join all of the elements in each row of the board and print the rows

    for y in range(board_height):
        row =[]
        for x in range(board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")
    
    print(header)

if __name__ == "__main__":
    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]

    for i in battleships:
        print(i.body)

    game_board = GameBoard(battleships, 10, 10)
    shots = [(1,1),(0,0),(5,7)]
    for sh in shots:
        game_board.take_shot(sh)

    for sh in game_board.shots:
        print(sh.location)
        print(sh.is_hit)
        print("==========")
    for b in game_board.battleships:
        print(b.body)
        print(b.hits)
        print("==========")

    exit(0)

    shots = []   

    while True: 
        inp = input("Where do you want to shoot?\n")
        xstr, ystr = inp.split(",")
        x = int(xstr)
        y = int(ystr)
        shots.append((x,y))
        render(10, 10, shots)
