mod game_of_life;

use std::collections::BTreeSet;
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use crate::game_of_life::{Cell, next_generation, populate_cell, show_neighbours, show_population, unpopulate_cell};

const MAX_PERIOD:i32 = 1000;

fn main() {

    let mut population= Vec::new();

    for n in 1..70 {
        population.push(Cell{x:0, y:n});
        // set to store all populated cells: {(x, y)}
        let mut occupied: BTreeSet<Cell>= BTreeSet::new();
        let mut occupied_next_generation: BTreeSet<Cell>= BTreeSet::new();

        // dictionary to store all cells with neighbours: {(x, y): n}
        let mut neighbours: HashMap<Cell, i32> = HashMap::new();
        let mut neighbours_next_generation: HashMap<Cell, i32> = HashMap::new();

        // keep a history of all populations to detect repetition
        let mut history = HashMap::new();

        // the initial population will be put in the next gen, so we need to init
        // the current generation at -1
        let mut generation = -1;
        for cell in &population {
            populate_cell(*cell, &mut occupied_next_generation, &mut neighbours_next_generation);
            //println!("{}", cell);
        }

        let mut terminal = false;
        let mut period = 0;

        for i in 0..MAX_PERIOD {
            //println!("---------------------- {} ---------------------", i);
            next_generation(&mut generation, &mut occupied, &mut occupied_next_generation, &mut neighbours, &mut neighbours_next_generation);
            //show_population(generation, &occupied);

            // create hash for this population
            let mut hasher = DefaultHasher::new();
            occupied.hash(&mut hasher);
            let hash = hasher.finish();

            if history.contains_key(&hash) {
                // repetition found
                let same_generation = history.get(&hash);
                period = generation - same_generation.unwrap();
                terminal = true;
            } else {
                history.insert(hash, generation);
            }

            if occupied.len() == 0 {
                // all died
                terminal = true;
            }

            //show_neighbours(generation, &neighbours);

            if terminal {
                break;
            }
        }

        if terminal {
            if period == 0 {
                println!("f({}) = 0. All cells have died at generation {}", n, generation)
            } else {
                println!("f({}) = {}. Period {} found at generation {}", n, period, period, generation);
            }
        } else {
            println!("f({}) = INF. No period found after {} generations", n, generation);
        }
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
