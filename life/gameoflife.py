class GameOfLife:
    def __init__(self):
        # set to store all populated cells: {(x, y)}
        self.occupied = {}
        # dictionary to store all cells with neighbours: {(x, y): n}
        self.neighbours = {}

if __name__ == '__main__':
    g = GameOfLife()