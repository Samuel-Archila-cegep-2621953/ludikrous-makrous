use crate::abstract_player::AbstractPlayer;
use crate::obstacles::Obstacle;
use crate::utils::*;
use crate::world_grid::{vec_grid::*, WorldGrid};
use std::boxed::Box;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;

const MAX_GEN_ATTEMPTS: u8 = 48;


#[derive(Debug)]
pub struct AbstractWorld<W: WorldGrid> {
    world: W,
    players: Vec<AbstractPlayer>,
    queue_new_obstacles: Arc<RwLock<Vec<u8>>>, // type provisoire
    pub debut: Instant,
}

impl AbstractWorld<VecGrid> {
    fn new(x: u8, y: u8) -> Self {
        Self {
            world: VecGrid::new_empty(x, y),
            players: Vec::new(),
            queue_new_obstacles: Arc::new(RwLock::new(Vec::new())),
            debut: Instant::now(),
        }
    }

    pub fn generate_obstacles(&mut self) {
        for _ in 0..MAX_GEN_ATTEMPTS {
            todo!();
        }
    }
}
