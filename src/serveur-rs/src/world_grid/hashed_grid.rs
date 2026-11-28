use crate::obstacles::Obstacle;
use crate::world_grid::{TilePosition, WorldGrid};
use crate::global_difficulty::*;
use crate::obstacles::*;
use std::boxed::Box;
use std::collections::HashMap;
use std::time::Instant;
use bytes::Bytes;

pub struct HashedGrid {
    size: (u8, u8),
    grid: HashMap<TilePosition, Box<dyn Obstacle>>,
    clock: Instant,
    global_difficulty: f32
}

impl WorldGrid for HashedGrid {
    fn new_empty(x: u8, y: u8) -> Self {
        Self {
            size: (x, y),
            grid: HashMap::with_capacity((x * y) as usize),
            clock: Instant::now(),
            global_difficulty: 0.0
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
    
    fn get_now(&self) -> Instant {
        self.clock
    }
    
    /*
    fn get<'a>(&mut self, pos: &'a TilePosition) -> Option<&'a mut Box<dyn Obstacle>> {
        self.grid.get_mut(pos)
    }
    */
    
    fn is_dead_at(&self, pos: TilePosition) -> Option<bool> {
        if let Some(tile) = self.grid.get(&pos) {
            return Some(tile.is_dead(self.clock))
        }
        None
    }
    
    fn garbage_collect(&mut self) {
        let mut queue: Vec<TilePosition> = Vec::with_capacity(16);
        
        for (pos, obstacle) in &self.grid {
            if obstacle.is_dead(self.clock) { 
                queue.push(*pos); 
            }
        }
        
        for p in queue {
            self.delete(p);
        }
    }
    
    fn generate_obstacles(&mut self) -> Vec<Bytes> {
        let mut new_obstacles: Vec<Bytes> =
            Vec::with_capacity(self.len_x() * self.len_y() / 10 + 3); //random approximation
        let now = self.get_now();
        //println!("{:?}", now.elapsed().as_secs());
        let target_difficulty = difficulty_fn(Self::DIFFICULTY_LEVEL)(now);
        println!("{:?}  {:?}", self.global_difficulty, target_difficulty);

        for _ in 0..Self::MAX_GEN_ATTEMPTS {
            if self.global_difficulty >= target_difficulty {
                println!("break");
                break;
            }

            let choice = ObstacleType::random_implemented_type();
            let now = self.clock;
            //let grid = &mut self.world;

            if let Some((gained_difficulty, mut obstacle)) =
                ObstacleType::construct(choice, now, self)
            {
                self.global_difficulty += gained_difficulty;
                //target_difficulty += gained_difficulty;

                if let ObstacleBytes::WillBeSent(bytes) = &mut obstacle {
                    new_obstacles.push(bytes.clone());
                }
            } else {
                continue;
            }
        }
        new_obstacles
    }
}
