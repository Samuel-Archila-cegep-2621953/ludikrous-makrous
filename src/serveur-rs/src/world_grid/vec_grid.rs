use crate::world_grid::WorldGrid;
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

    fn is_free(&self, x: u8, y: u8) -> bool {
        self.0[x as usize][y as usize].is_none()
    }

    fn len_x(&self) -> usize {
        self.0.len()
    }

    fn len_y(&self) -> usize {
        self.0[0].len()
    }

    fn set(&mut self, pos: (u8, u8), obstacle: Box<dyn Obstacle>) {
        self.0[pos.0 as usize][pos.1 as usize] = Some(obstacle);
    }
    
    fn delete(&mut self, x: u8, y: u8) {
        if self.is_free(x, y) { return }

        self.0[x][y] = None;
    }
}