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

        # store generation signatures to check for recurrences
        self.history = {}

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
        period = 0
        terminal = False

        self.generation += 1
        # copy next generation over the current
        # a shallow copy should be sufficient
        self.occupied = self.occupied_next_generation.copy()
        self.neighbours = self.neighbours_next_generation.copy()

        # check if we have found a period yet, or all cells have died
        signature = frozenset(self.occupied)
        if signature in self.history:
            #print(f"Generation {self.generation} is the same as {self.history[signature]}")
            period = self.generation - self.history[signature]
            terminal = True
        else:
            self.history[signature] = self.generation

        if len(self.occupied) == 0:
            terminal = True

        # update next generation, based on current, according to life rules

        # die with 0, 1, 4-8, survive with 2, 3 neighbours
        for cell in self.occupied:
            if cell not in self.neighbours or self.neighbours[cell] not in [2, 3]:
                self.unpopulate_cell(cell)
        # birth if empty cell has 3 neighbours
        for cell, neighbours in self.neighbours.items():
            if neighbours == 3 and cell not in self.occupied:
                self.populate_cell(cell)

        return terminal, period, self.generation



MAX_PERIOD = 10

if __name__ == '__main__':
    g = GameOfLife([(0, 0)])

    #print(g.occupied)

    terminal = False
    period = 0
    generation = 0

    for i in range(MAX_PERIOD):
        terminal, period, generation = g.next_generation()
        if terminal:
            break

    if terminal:
        if period > 0:
            print(f"Period {period} found at generation {generation}")
        else:
            print(f"All cells have died at generation {generation}")
    else:
        print(f"No period found after {generation} generations")
