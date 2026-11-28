use bytes::Bytes;
use crate::world_grid::{TilePosition, WorldGrid};
use std::boxed::Box;
use crate::obstacles::*;
use std::iter::repeat_with;
use crate::utils::select_random;
use std::default::Default;
use crate::global_difficulty::*;

#[derive(Debug)]
pub struct VecGrid {
    world: Vec<Vec<Option<Box<dyn Obstacle>>>>,
    clock: std::time::Instant,
    global_difficulty: f32
}

impl WorldGrid for VecGrid {
    fn new_empty(x: u8, y: u8) -> Self {
        Self {
            world: repeat_with(|| repeat_with(|| None).take(x as usize).collect())
                .take(y as usize)
                .collect(),
            clock: std::time::Instant::now(),
            global_difficulty: 0.0
        }
    }

    #[inline]
    fn is_free(&self, pos: TilePosition) -> bool {
        self.world[pos.x as usize][pos.y as usize].is_none()
    }

    #[inline]
    fn len_x(&self) -> usize {
        self.world.len()
    }

    #[inline]
    fn len_y(&self) -> usize {
        self.world[0].len()
    }

    #[inline]
    fn set(&mut self, pos: TilePosition, obstacle: Box<dyn Obstacle>) {
        self.world[pos.x as usize][pos.y as usize] = Some(obstacle);
    }
    
    fn delete(&mut self, pos: TilePosition) {
        if self.is_free(pos) { return }
        self.world[pos.x as usize][pos.y as usize] = None;
    }
    
    fn is_dead_at(&self, pos: TilePosition) -> Option<bool> {
        if let Some(tile) = &self.world[pos.x as usize][pos.y as usize] {
            return Some(tile.is_dead(self.clock))
        }
        None
    }
    
    fn garbage_collect(&mut self) {
        let mut queue: Vec<TilePosition> = Vec::with_capacity(16);
        
        for x in 0..self.len_x() {
            for y in 0..self.len_y() {
                if let Some(obstacle) = self.is_dead_at(TilePosition::from(x as u8, y as u8)) && obstacle {
                    queue.push(TilePosition::from(x as u8,y as u8));
                }
            }
        }
        
        for p in queue {
            self.delete(p);
        }
    }
    
    fn get_now(&self) -> std::time::Instant {
        self.clock
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