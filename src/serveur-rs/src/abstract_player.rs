use crate::utils::*;
use serde::Serialize;

#[derive(Copy, Clone, Debug, Serialize, PartialEq, Eq, Hash)]
pub struct Id(pub u32);

#[derive(Debug, Serialize, Clone, Copy)]
pub struct AbstractPlayer {
    pub life: u8,
    pub id: Id,
    pub position: FalseVec3,
    pub health: u8,
    pub animation: u8,
    pub rotation: f32,
    pub display_name: [u8; 16],
    recv_update_obstacles: bool,
}

impl AbstractPlayer {
    pub fn new(id: u32, display_name: [u8; 16]) -> Self {
        Self {
            life: 255,
            id: Id(id),
            position: FalseVec3(0,0,0),
            health: 255,
            animation: 0,
            rotation: 0.0,
            display_name,
            recv_update_obstacles: false
        }   
    }
}
