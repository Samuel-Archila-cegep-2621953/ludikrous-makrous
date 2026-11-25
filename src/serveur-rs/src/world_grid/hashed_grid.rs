use crate::obstacles::Obstacle;
use crate::world_grid::WorldGrid;
use std::boxed::Box;
use std::collections::HashMap;

pub struct HashedGrid {
    size: (u8, u8),
    grid: HashMap<(u8, u8), Box<dyn Obstacle>>,
}

impl WorldGrid for HashedGrid {
    fn new_empty(x: u8, y: u8) -> Self {
        Self {
            size: (x, y),
            grid: HashMap::with_capacity((x * y) as usize),
        }
    }

    fn is_free(&self, x: u8, y: u8) -> bool {
        !self.grid.contains_key(&(x, y))
    }

    fn len_x(&self) -> usize {
        self.size.0 as usize
    }

    fn len_y(&self) -> usize {
        self.size.1 as usize
    }

    fn set(&mut self, pos: (u8, u8), obstacle: Box<dyn Obstacle>) {
        self.grid.insert(pos, obstacle);
    }

    fn delete(&mut self, x: u8, y: u8) {
        _ = self.grid.remove(&(x, y));
    }
}
