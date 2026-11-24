use crate::abstract_player::AbstractPlayer;
use crate::obstacles::Obstacle;
use crate::utils::*;
use std::boxed::Box;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;

#[derive(Debug)]
pub struct WorldGrid(Vec<Vec<Option<Box<dyn Obstacle>>>>);
const MAX_GEN_ATTEMPTS: u8 = 48;

impl WorldGrid {
    fn new_empty(x: u16, y: u16) -> Self {
        Self(
            repeat_with(|| repeat_with(|| None).take(x as usize).collect())
                .take(y as usize)
                .collect(),
        )
    }

    pub fn is_free(&self, x: u8, y: u8) -> bool {
        self.0[x as usize][y as usize].is_none()
    }

    pub fn select_random_grid_position(&self) -> (u8, u8) {
        let x_max = self.len_x() as u8;
        let y_max = self.len_y() as u8;

        (select_random(x_max - 1), select_random(y_max - 1))
    }

    pub fn len_x(&self) -> usize {
        self.0.len()
    }

    pub fn len_y(&self) -> usize {
        self.0[0].len()
    }

    pub fn set(&mut self, pos: (u8, u8), obstacle: Box<dyn Obstacle>) {
        self.0[pos.0 as usize][pos.1 as usize] = Some(obstacle);
    }
}

#[derive(Debug)]
pub struct AbstractWorld {
    world: WorldGrid,
    players: Vec<AbstractPlayer>,
    queue_new_obstacles: Arc<RwLock<Vec<u8>>>, // type provisoire
    pub debut: Instant,
}

impl AbstractWorld {
    fn new(x: u16, y: u16) -> Self {
        Self {
            world: WorldGrid::new_empty(x, y),
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
