//mod utils;
use crate::utils::*;
use serde::Serialize;

#[derive(Copy, Clone, Debug, Serialize, PartialEq, Eq, Hash)]
pub struct Id(u8);

#[derive(Debug, Serialize)]
pub struct AbstractPlayer {
    life: u8,
    id: Id,
    position: Vec3,
    recv_update_obstacles: bool,
}

impl AbstractPlayer {
    pub fn new(id: u8) -> Self {
        Self {
            life: 255,
            id: Id(id),
            position: Vec3(0f32,0f32,0f32),
        recv_update_obstacles: false
        }   
    }
}
