use crate::utils::*;
use std::boxed::Box;
use crate::obstacles::*;
use std::time::Instant;

pub mod vec_grid;
pub mod hashed_grid;

#[derive(Debug, Copy, Clone, Eq, Hash, PartialEq)]
pub struct TilePosition {
    pub x: u8, 
    pub y: u8
}

impl TilePosition {
    fn from(x: u8, y: u8) -> Self {
        Self { x, y }
    }
}

pub trait WorldGrid {
    fn new_empty(x: u8, y: u8) -> Self;
    fn is_free(&self, pos: TilePosition) -> bool;
    
    fn random_tile(&self) -> TilePosition {
        let x_max = self.len_x() as u8;
        let y_max = self.len_y() as u8;

        TilePosition::from(select_random(x_max - 1), select_random(y_max - 1))
    }
    
    #[inline]
    fn default() -> Self 
    where Self: Sized {
        Self::new_empty(8, 8)
    }
    
    fn len_x(&self) -> usize;
    fn len_y(&self) -> usize;
    fn set(&mut self, pos: TilePosition, obstacle: Box<dyn Obstacle>);
    fn delete(&mut self, pos: TilePosition);
    fn delete_if_dead(&mut self, pos: TilePosition, now: Instant) {
        if !self.is_free(pos) {}
    }
}