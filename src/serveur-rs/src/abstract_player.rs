use crate::utils::*;
use dashmap::DashMap;
use serde::Serialize;
use bytes::Bytes;
use crate::packet_types::from_server;

#[derive(Copy, Clone, Debug, Serialize, PartialEq, Eq, Hash)]
pub struct Id(pub u32);

#[derive(Debug)]
pub struct AbstractPlayerStates {
    players: DashMap<Id, AbstractPlayer>,
}

impl AbstractPlayerStates {
    pub fn init(max_players: u16) -> Self {
        Self {
            players: DashMap::with_capacity(max_players as usize),
        }
    }
    
    pub fn len(&self) -> usize {
        self.players.len()
    }
    
    pub fn get_player_states(&self) -> Vec<bytes::Bytes> {
        let mut buf_vec: Vec<Bytes> = Vec::with_capacity(self.players.len());

        for entry in &self.players {
            buf_vec.push(from_server::PlayerUpdate::from(*entry.value()).encode());
        }

        buf_vec
    }
}

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
            position: FalseVec3(0, 0, 0),
            health: 255,
            animation: 0,
            rotation: 0.0,
            display_name,
            recv_update_obstacles: false,
        }
    }
}
