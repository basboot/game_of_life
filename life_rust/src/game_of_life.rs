use std::collections::{HashMap, HashSet};
use std::fmt;

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
                     occupied_next_generation: &mut HashSet<Cell>,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    assert!(!occupied_next_generation.contains(&cell), "Cell {} is already populated.", cell);
    // add cell to the next generation
    occupied_next_generation.insert(cell);
    println!("{}", cell);

    // update the cells neighbours for the next generation
    for x in -1..2 {
        for y in -1..2 {
            if x == 0 && y == 0 {
                continue
            }
            println!("{}, {}", x, y);
            add_neighbour(Cell{x: cell.x + x, y: cell.y + y}, neighbours_next_generation);
        }
    }
}

pub fn unpopulate_cell(cell: Cell,
                     occupied_next_generation: &mut HashSet<Cell>,
                     neighbours_next_generation: &mut HashMap<Cell, i32>) {
    assert!(occupied_next_generation.contains(&cell), "Cell {} is not populated.", cell);
    // remove cell from the next generation
    occupied_next_generation.remove(&cell);
    println!("{}", cell);

    // update the cells neighbours for the next generation
    for x in -1..2 {
        for y in -1..2 {
            if x == 0 && y == 0 {
                continue
            }
            println!("{}, {}", x, y);
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
