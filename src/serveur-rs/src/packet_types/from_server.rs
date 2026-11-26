use serde::Serialize;
use std::convert::From;
use bincode_next::{Encode, encode_into_slice, encode_to_vec};
use bytes::*;
use crate::{abstract_player::*, packet_types::FromServerPacketTypes};
use crate::utils::DEFAULT_BINCODE_CFG;

#[derive(Debug, Serialize, Encode)]
pub struct PlayerUpdate {
    ty: u8,
    id: u32,
    display_name: [u8; 16],
    x: i32,
    y: i32,
    z: i32,
    health: u8,
    animation: u8,
    rotation: f32
}

#[derive(Debug, Serialize, Encode)]
pub struct LoginSuccess {
    ty: u8,
    no_idea: i32,
    message: [u8; 32]
}

#[derive(Debug, Serialize, Encode)]
pub struct LoginFailure {
    ty: u8,
}

#[derive(Debug, Serialize, Encode)]
pub struct ObstacleUpdate {
    ty: u8,
}

#[derive(Debug, Serialize, Encode)]
pub struct Logout {
    ty: u8,
}


impl From<AbstractPlayer> for PlayerUpdate {
    fn from(item: AbstractPlayer) -> Self {
        Self {
            ty: FromServerPacketTypes::PlayerUpdate as u8,
            id: item.id.0,
            display_name: item.display_name,
            x: item.position.0,
            y: item.position.1,
            z: item.position.2,
            health: item.health,
            animation: item.animation,
            rotation: item.rotation
        }
    }
}

impl PlayerUpdate {
    pub fn encode(self) -> Bytes {
        let vec = encode_to_vec(self,  DEFAULT_BINCODE_CFG).expect("Failed encoding from_server::PlayerUpdate");
        Bytes::from(vec)
    }
}