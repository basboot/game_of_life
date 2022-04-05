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
                self.add_neighbour((x, y))

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
                self.remove_neighbour((x, y))

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


if __name__ == '__main__':
    g = GameOfLife([(1, 1), (2, 1)])

    print(g.neighbours_next_generation)
    g.unpopulate_cell((2, 1))
    print(g.neighbours_next_generation)