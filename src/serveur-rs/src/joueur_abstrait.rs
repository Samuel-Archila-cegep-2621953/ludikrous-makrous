//mod utils;
use crate::utils::*;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct AbstractPlayer {
    life: u8,
    id: u8,
    position: Vec3,
    recv_update_obstacles: bool,
}

impl AbstractPlayer {
    pub fn new(id: u8) -> Self {
        Self {
            life: 255,
            id: id,
            position: Vec3(0f32,0f32,0f32),
        recv_update_obstacles: false
        }   
    }
}
