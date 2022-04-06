mod game_of_life;

use std::collections::BTreeSet;
use std::collections::HashMap;
use crate::game_of_life::{Cell, next_generation, populate_cell, show_neighbours, show_population, unpopulate_cell};


fn main() {
    let population = [Cell{ x: 0, y: 0 }, Cell{ x: 0, y: 1 }, Cell{ x: 0, y: 2 }];
    // set to store all populated cells: {(x, y)}
    let mut occupied: BTreeSet<Cell>= BTreeSet::new();
    let mut occupied_next_generation: BTreeSet<Cell>= BTreeSet::new();

    // dictionary to store all cells with neighbours: {(x, y): n}
    let mut neighbours: HashMap<Cell, i32> = HashMap::new();
    let mut neighbours_next_generation: HashMap<Cell, i32> = HashMap::new();

    // the initial population will be put in the next gen, so we need to init
    // the current generation at -1
    let mut generation = -1;
    for cell in population {
        populate_cell(cell, &mut occupied_next_generation, &mut neighbours_next_generation);
        //println!("{}", cell);
    }

    for i in 0..5 {
        println!("---------------------- {} ---------------------", i);
        next_generation(&mut generation, &mut occupied, &mut occupied_next_generation, &mut neighbours, &mut neighbours_next_generation);
        show_population(generation, &occupied);
        //show_neighbours(generation, &neighbours);
    }

    // println!("Neighbours");
    // for (cell, neighbours) in &neighbours_next_generation {
    //     println!("{} has {} neighbours", cell, neighbours);
    // }

// self.populate_cell(cell)
//
// # store generation signatures to check for recurrences
// self.history = {}

}
