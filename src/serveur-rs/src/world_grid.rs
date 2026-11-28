use crate::global_difficulty;
use crate::obstacles::*;
use crate::utils::*;
use std::boxed::Box;
use std::time::Instant;
use bytes::Bytes;
use crate::global_difficulty::*;

pub mod hashed_grid;
pub mod vec_grid;

#[derive(Debug, Copy, Clone, Eq, Hash, PartialEq)]
pub struct TilePosition {
    pub x: u8,
    pub y: u8,
}

impl TilePosition {
    fn from(x: u8, y: u8) -> Self {
        Self { x, y }
    }
}

pub trait WorldGrid {
    const MAX_GEN_ATTEMPTS: u8 = 48;
    const DIFFICULTY_LEVEL: u8 = 2;
    fn new_empty(x: u8, y: u8) -> Self;
    fn is_free(&self, pos: TilePosition) -> bool;
    fn len_x(&self) -> usize;
    fn len_y(&self) -> usize;
    fn set(&mut self, pos: TilePosition, obstacle: Box<dyn Obstacle>);
    fn delete(&mut self, pos: TilePosition);
    fn is_dead_at(&self, pos: TilePosition) -> Option<bool>;

    #[inline]
    fn default() -> Self
    where
        Self: Sized,
    {
        Self::new_empty(8, 8)
    }

    fn random_tile(&self) -> TilePosition {
        let x_max = self.len_x() as u8;
        let y_max = self.len_y() as u8;

        TilePosition::from(select_random(x_max - 1), select_random(y_max - 1))
    }

    fn delete_if_dead(&mut self, pos: TilePosition) {
        if self.is_free(pos) {
            return;
        }
        if let Some(liveness) = self.is_dead_at(pos)
            && liveness
        {
            self.delete(pos);
        }
    }
    
    fn garbage_collect(&mut self);
    
    fn get_now(&self) -> Instant;
    
    fn generate_obstacles(&mut self) -> Vec<Bytes>; /*{
        let mut new_obstacles: Vec<Bytes> =
            Vec::with_capacity(self.len_x() * self.len_y() / 10 + 3); //random approximation
        let now = self.get_now();
        //println!("{:?}", now.elapsed().as_secs());
        let mut target_difficulty = difficulty_fn(Self::DIFFICULTY_LEVEL)(now);
        let global_difficulty = self.global_difficulty();
        println!("{:?}  {:?}", global_difficulty, target_difficulty);

        for _ in 0..Self::MAX_GEN_ATTEMPTS {
            if *global_difficulty >= target_difficulty {
                println!("break");
                break;
            }

            let choice = ObstacleType::random_implemented_type();
            let now = self.get_now();
            let grid = self.grid_ref();

            if let Some((gained_difficulty, mut obstacle)) =
                ObstacleType::construct(choice, now, grid)
            {
                *global_difficulty += gained_difficulty;
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
    */
    
    
}
