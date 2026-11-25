use crate::world_grid::{TilePosition, WorldGrid};
use std::boxed::Box;
use crate::obstacles::Obstacle;
use std::iter::repeat_with;
use crate::utils::select_random;
use std::default::Default;

#[derive(Debug)]
pub struct VecGrid(Vec<Vec<Option<Box<dyn Obstacle>>>>);

impl WorldGrid for VecGrid {
    fn new_empty(x: u8, y: u8) -> Self {
        Self(
            repeat_with(|| repeat_with(|| None).take(x as usize).collect())
                .take(y as usize)
                .collect(),
        )
    }

    #[inline]
    fn is_free(&self, pos: TilePosition) -> bool {
        self.0[pos.x as usize][pos.y as usize].is_none()
    }

    #[inline]
    fn len_x(&self) -> usize {
        self.0.len()
    }

    #[inline]
    fn len_y(&self) -> usize {
        self.0[0].len()
    }

    #[inline]
    fn set(&mut self, pos: TilePosition, obstacle: Box<dyn Obstacle>) {
        self.0[pos.x as usize][pos.y as usize] = Some(obstacle);
    }
    
    fn delete(&mut self, pos: TilePosition) {
        if self.is_free(pos) { return }
        self.0[pos.x as usize][pos.y as usize] = None;
    }
}