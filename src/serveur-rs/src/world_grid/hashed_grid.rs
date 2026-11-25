use crate::obstacles::Obstacle;
use crate::world_grid::{TilePosition, WorldGrid};
use std::boxed::Box;
use std::collections::HashMap;
use std::time::Instant;

pub struct HashedGrid {
    size: (u8, u8),
    grid: HashMap<TilePosition, Box<dyn Obstacle>>,
}

impl WorldGrid for HashedGrid {
    fn new_empty(x: u8, y: u8) -> Self {
        Self {
            size: (x, y),
            grid: HashMap::with_capacity((x * y) as usize),
        }
    }

    #[inline]
    fn is_free(&self, pos: TilePosition) -> bool {
        !self.grid.contains_key(&pos)
    }

    #[inline]
    fn len_x(&self) -> usize {
        self.size.0 as usize
    }

    #[inline]
    fn len_y(&self) -> usize {
        self.size.1 as usize
    }

    #[inline]
    fn set(&mut self, pos: TilePosition, obstacle: Box<dyn Obstacle>) {
        self.grid.insert(pos, obstacle);
    }

    #[inline]
    fn delete(&mut self, pos: TilePosition) {
        _ = self.grid.remove(&pos);
    }
    
    /*
    fn get<'a>(&mut self, pos: &'a TilePosition) -> Option<&'a mut Box<dyn Obstacle>> {
        self.grid.get_mut(pos)
    }
    */
    
    fn is_dead_at(&self, pos: TilePosition, now: Instant) -> Option<bool> {
        if let Some(tile) = self.grid.get(&pos) {
            return Some(tile.is_dead(now))
        }
        None
    }
    
    fn garbage_collect(&mut self, now: Instant) {
        let mut queue: Vec<TilePosition> = Vec::with_capacity(16);
        
        for (pos, obstacle) in &self.grid {
            if obstacle.is_dead(now) { 
                queue.push(*pos); 
            }
        }
        
        for p in queue {
            self.delete(p);
        }
    }
}
