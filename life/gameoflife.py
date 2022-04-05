class GameOfLife:
    def __init__(self, population):
        # set to store all populated cells: {(x, y)}
        self.occupied = set()
        self.occupied_next_generation = set()

        # dictionary to store all cells with neighbours: {(x, y): n}
        self.neighbours = {}
        self.neighbours_next_generation = {}

        # the initial population will be put in the next gen, so we need to init
        # the current generation at 0
        self.generation = 0
        for cell in population:
            self.populate_cell(cell)

    def populate_cell(self, cell):
        assert cell not in self.occupied_next_generation, f"Cell {cell} is already populated."
        # add cell to the next generation
        self.occupied_next_generation.add(cell)

        # update the cells neighbours for the next generation
        for x in range(-1, 2):
            for y in range(-1, 2):
                # skip the cell itself
                if x == 0 and y == 0:
                    continue
                self.add_neighbour((cell[0] + x, cell[1] + y))

    def unpopulate_cell(self, cell):
        assert cell in self.occupied_next_generation, f"Cell {cell} is not populated."
        # add cell to the next generation
        self.occupied_next_generation.remove(cell)

        # update the cells neighbours for the next generation
        for x in range(-1, 2):
            for y in range(-1, 2):
                # skip the cell itself
                if x == 0 and y == 0:
                    continue
                self.remove_neighbour((cell[0] + x, cell[1] + y))

    def add_neighbour(self, cell):
        if cell not in self.neighbours_next_generation:
            self.neighbours_next_generation[cell] = 1
        else:
            self.neighbours_next_generation[cell] += 1

    def remove_neighbour(self, cell):
        assert cell in self.neighbours_next_generation, f"Cell {cell} has no neighbours"

        self.neighbours_next_generation[cell] -= 1

        # remove cell from dictionary if there are no neighbours left
        if self.neighbours_next_generation[cell] == 0:
            del self.neighbours_next_generation[cell]

    def next_generation(self):
        # copy next generation over the current
        # a shallow copy should be sufficient
        self.occupied = self.occupied_next_generation.copy()
        self.neighbours = self.neighbours_next_generation.copy()

        # update next generation, based on current, according to life rules

        # die with 0, 1, 4-8, survive with 2, 3 neighbours
        for cell in self.occupied:
            if cell not in self.neighbours or self.neighbours[cell] not in [2, 3]:
                self.unpopulate_cell(cell)
        # birth if empty cell has 3 neighbours
        for cell, neighbours in self.neighbours.items():
            if neighbours == 3 and cell not in self.occupied:
                self.populate_cell(cell)




if __name__ == '__main__':
    g = GameOfLife([(0, 0), (0, 1), (0, 2)])

    #print(g.occupied)

    for i in range(10):
        g.next_generation()
        print(g.occupied)
        #print(g.neighbours)
