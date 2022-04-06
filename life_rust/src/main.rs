mod game_of_life;

use std::collections::HashSet;
use std::collections::HashMap;
use crate::game_of_life::{Cell, populate_cell, unpopulate_cell};


fn main() {
    let population = [Cell{ x: 0, y: 1 }, Cell{ x: 0, y: 2 }];
    // set to store all populated cells: {(x, y)}
    let mut occupied: HashSet<Cell>= HashSet::new();
    let mut occupied_next_generation: HashSet<Cell>= HashSet::new();

    // dictionary to store all cells with neighbours: {(x, y): n}
    let mut neighbours: HashMap<Cell, i32> = HashMap::new();
    let mut neighbours_next_generation: HashMap<Cell, i32> = HashMap::new();

    // the initial population will be put in the next gen, so we need to init
    // the current generation at -1
    let generation = -1;
    for cell in population {
        populate_cell(cell, &mut occupied_next_generation, &mut neighbours_next_generation);
        println!("{}", cell);
    }

    unpopulate_cell(Cell{x: 0, y: 2}, &mut occupied_next_generation, &mut neighbours_next_generation);
    unpopulate_cell(Cell{x: 0, y: 1}, &mut occupied_next_generation, &mut neighbours_next_generation);

    println!("Neighbours");
    for (cell, neighbours) in &neighbours_next_generation {
        println!("{} has {} neighbours", cell, neighbours);
    }

// self.populate_cell(cell)
//
// # store generation signatures to check for recurrences
// self.history = {}

}
