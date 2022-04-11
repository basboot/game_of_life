from persistent_data import *

# Global for easy implementation TODO: cleanup
# keep track of x,y max and min to determine size of the universe
min_x = 0
min_y = 0
max_x = 0
max_y = 0

class GameOfLife:
    def __init__(self, population):
        # set to store all populated cells: {(x, y)}
        self.occupied = set()
        self.occupied_next_generation = set()

        # dictionary to store all cells with neighbours: {(x, y): n}
        self.neighbours = {}
        self.neighbours_next_generation = {}

        # the initial population will be put in the next gen, so we need to init
        # the current generation at -1
        self.generation = -1
        for cell in population:
            self.populate_cell(cell)

        # store generation signatures to check for recurrences
        self.history = {}

    def populate_cell(self, cell):
        global min_x, min_y, max_x, max_y

        assert cell not in self.occupied_next_generation, f"Cell {cell} is already populated."
        # add cell to the next generation
        self.occupied_next_generation.add(cell)

        # keep track of x,y max and min to determine size of the universe
        min_x = min(min_x, cell[0])
        min_y = min(min_y, cell[1])
        max_x = max(max_x, cell[0])
        max_y = max(max_y, cell[1])

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



MAX_PERIOD = 10000

INITIAL_POPULATION = 1
FINAL_POPULATION = 101

# TODO: Save results, and use cached results, but bypass cache when settings have been changed

if __name__ == '__main__':
    # Load data to (re)start
    results, max_n = load_data()

    initial_population = []

    # skip until initial population has been reached
    for n in range(INITIAL_POPULATION - 1):
        initial_population.append((0, n))

    for n in range(INITIAL_POPULATION, FINAL_POPULATION):
        initial_population.append((0, n))

        g = GameOfLife(initial_population)

        # we only need to repeat the experiment if we have not run it yet (terminal == True)
        # or if it was not finished, and we might improve (terminal == False, generation < MAX_PERIOD - 1)

        if (n not in results) or (not results[n]["terminal"] and results[n]["generation"] < MAX_PERIOD - 1):
            terminal = False
            period = 0
            generation = 0

            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0

            for i in range(MAX_PERIOD):
                terminal, period, generation = g.next_generation()
                if terminal:
                    break

            if n in results:
                print(f"Updated result for f({n})")

            universe = (min_x, max_x, min_y, max_y)
            results[n] = {"terminal": terminal, "period": period, "generation": generation, "universe": universe}
            max_n = max(n, max_n)
            save_data(results, max_n)
        else:
            terminal = results[n]["terminal"]
            period = results[n]["period"]
            generation = results[n]["generation"]
            universe = results[n]["universe"]

        if terminal:
            if period > 0:
                print(f"f({n}) = {period}. Period {period} found at generation {generation}. Universe: {universe[0]}..{universe[1]}, {universe[2]}..{universe[3]}")
                #print(f"{n}, {period}, {generation}")
            else:
                print(f"f({n}) = 0. All cells have died at generation {generation}. Universe: {universe[0]}..{universe[1]}, {universe[2]}..{universe[3]}")
                #print(f"{n}, {period}, {generation}")
        else:
            print(f"f({n}) = INF. No period found after {generation} generations. Universe: {universe[0]}..{universe[1]}, {universe[2]}..{universe[3]}")
            #print(f"{n}, {MAX_PERIOD}, {generation}")
