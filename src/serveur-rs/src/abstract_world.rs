use crate::abstract_player::AbstractPlayer;
use crate::obstacles::*;
use crate::utils::*;
use crate::world_grid::{vec_grid::*, WorldGrid};
use crate::abstract_player::*;
use std::boxed::Box;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;
use std::collections::HashMap;

const MAX_GEN_ATTEMPTS: u8 = 48;


#[derive(Debug)]
pub struct AbstractWorld<W: WorldGrid> {
    world: W,
    players: HashMap<Id, AbstractPlayer>,
    global_difficulty: f32,
    queue_new_obstacles: RwLock<Vec<u8>>, // type provisoire
    pub clock: Instant,
}

impl AbstractWorld<VecGrid> {
    pub fn new(x: u8, y: u8) -> Self {
        Self {
            world: VecGrid::new_empty(x, y),
            players: HashMap::new(),
            global_difficulty: 0.0,
            queue_new_obstacles: RwLock::new(Vec::new()),
            clock: Instant::now(),
        }
    }

    pub fn generate_obstacles(&mut self) -> Vec<u8> {
        let mut new_obstacles: Vec<u8> = Vec::with_capacity(self.world.len_x() * self.world.len_y() / 10 + 3); //random approximation
        
        for _ in 0..MAX_GEN_ATTEMPTS {
            let choice = ObstacleType::random_implemented_type();
            let now = self.clock;
            let grid = &mut self.world;
            
            
            if let Some((gained_difficulty, mut obstacle)) = ObstacleType::construct(choice, now, grid) {
                self.global_difficulty += gained_difficulty;

                if let ObstacleBytes::WillBeSent(bytes) = &mut obstacle {
                    new_obstacles.append(bytes);
                }
            } else { continue }
        }
        
        new_obstacles
    }
    
    pub fn add_to_new_obstacles_queue(&mut self, bytes: Vec<u8>) {
        *self.queue_new_obstacles.write().expect("Error on writing to new obstacles queue") = bytes;
    }
}
