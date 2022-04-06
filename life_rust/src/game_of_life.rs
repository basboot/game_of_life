use std::collections::{HashMap, BTreeSet};
use std::fmt;
use std::hash::Hash;


// A cell needs to be hashable and comparable to use it as key for sets and maps
// Copy and Clone are needed to use the value multiple times
#[derive(PartialEq, Eq, PartialOrd, Ord, Hash, Copy, Clone)]
pub struct Cell {
    pub x: i32,
    pub y: i32,
}

// Implement `Display` for `Cell`.
impl fmt::Display for Cell {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

pub fn populate_cell(cell: Cell,
                     occupied_next_generation: &mut BTreeSet<Cell>,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    assert!(!occupied_next_generation.contains(&cell), "Cell {} is already populated.", cell);
    // add cell to the next generation
    occupied_next_generation.insert(cell);
    //println!("{}", cell);

    // update the cells neighbours for the next generation
    for x in -1..2 {
        for y in -1..2 {
            if x == 0 && y == 0 {
                continue
            }
            //println!("{}, {}", x, y);
            add_neighbour(Cell{x: cell.x + x, y: cell.y + y}, neighbours_next_generation);
        }
    }
}

pub fn unpopulate_cell(cell: Cell,
                     occupied_next_generation: &mut BTreeSet<Cell>,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    assert!(occupied_next_generation.contains(&cell), "Cell {} is not populated.", cell);
    // remove cell from the next generation
    occupied_next_generation.remove(&cell);
    //println!("{}", cell);

    // update the cells neighbours for the next generation
    for x in -1..2 {
        for y in -1..2 {
            if x == 0 && y == 0 {
                continue
            }
            //println!("{}, {}", x, y);
            remove_neighbour(Cell{x: cell.x + x, y: cell.y + y}, neighbours_next_generation);
        }
    }
}

pub fn add_neighbour(cell: Cell,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    // update a key, guarding against the key possibly not being set
    let neighbours = neighbours_next_generation.entry(cell).or_insert(0);
    *neighbours += 1;
}

pub fn remove_neighbour(cell: Cell,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    assert!(neighbours_next_generation.contains_key(&cell), "Cell {} has no neighbours", cell);

    let neighbours = neighbours_next_generation.entry(cell).or_insert(1);
    *neighbours -= 1;

    if *neighbours == 0 {
        neighbours_next_generation.remove_entry(&cell);
    }
}

pub fn next_generation(generation: &mut i32,
                       occupied: &mut BTreeSet<Cell>,
                       occupied_next_generation: &mut BTreeSet<Cell>,
                       neighbours: &mut HashMap<Cell, i32>,
                       neighbours_next_generation: &mut HashMap<Cell, i32>,
                       ) {

    // period = 0
    // terminal = False
    //
    *generation += 1;
    // # copy next generation over the current
    // # a shallow copy should be sufficient
    // self.occupied = self.occupied_next_generation.copy()
    // self.neighbours = self.neighbours_next_generation.copy()

    // TODO: implement extend trait
    occupied.clear();
    for cell in occupied_next_generation.iter() {
        occupied.insert(*cell);
    }

    neighbours.clear();
    for (cell, n) in &*neighbours_next_generation {
        // all entries are new
        let neighbours = neighbours.entry(*cell).or_insert(*n);
    }

    //
    // # check if we have found a period yet, or all cells have died
    // signature = frozenset(self.occupied)
    // if signature in self.history:
    // #print(f"Generation {self.generation} is the same as {self.history[signature]}")
    // period = self.generation - self.history[signature]
    // terminal = True
    // else:
    // self.history[signature] = self.generation
    //
    // if len(self.occupied) == 0:
    //     terminal = True
    //
    // # update next generation, based on current, according to life rules
    //
    // # die with 0, 1, 4-8, survive with 2, 3 neighbours
    for cell in occupied.iter() {
        println!("Check {}", cell);
        if !neighbours.contains_key(cell) || (neighbours.get(&cell) != Some(&2) && neighbours.get(&cell) != Some(&3)) {
            unpopulate_cell(*cell, occupied_next_generation, neighbours_next_generation);
        }
    }

    // # birth if empty cell has 3 neighbours
    for (cell, n) in neighbours {
        if *n == 3 && !occupied.contains(cell) {
            populate_cell(*cell, occupied_next_generation, neighbours_next_generation);
        }
    }
    // if neighbours == 3 and cell not in self.occupied:
    //     self.populate_cell(cell)
    //
    // return terminal, period, self.generation
}

pub fn show_population(generation: i32, occupied: &BTreeSet<Cell>) {
    print!("Generation {}: ", generation);
    for cell in occupied.iter() {
        print!("{}, ", cell);
    }
}

pub fn show_neighbours(generation: i32, neighbours: &HashMap<Cell, i32>) {
    print!("Generation {}: ", generation);
    for (cell, n) in neighbours {
        print!("{}: {}, ", cell, n);
    }
    println!();
}