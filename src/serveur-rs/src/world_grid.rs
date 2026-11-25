use crate::utils::*;
use std::boxed::Box;
use crate::obstacles::*;

pub mod vec_grid;
pub mod hashed_grid;

pub trait WorldGrid {
    fn new_empty(x: u8, y: u8) -> Self;
    fn is_free(&self, x: u8, y: u8) -> bool;
    
    fn select_random_grid_position(&self) -> (u8, u8) {
        let x_max = self.len_x() as u8;
        let y_max = self.len_y() as u8;

        (select_random(x_max - 1), select_random(y_max - 1))
    }
    
    #[inline]
    fn default() -> Self 
    where Self: Sized {
        Self::new_empty(8, 8)
    }
    
    fn len_x(&self) -> usize;
    fn len_y(&self) -> usize;
    fn set(&mut self, pos: (u8, u8), obstacle: Box<dyn Obstacle>);
    fn delete(&mut self, x: u8, y: u8);
}