use crate::abstract_player::AbstractPlayer;
use crate::obstacles::*;
use crate::packet_types::from_server;
use crate::utils::*;
use crate::world_grid::{vec_grid::*, WorldGrid};
use crate::abstract_player::*;
use crate::packet_types;
use crate::global_difficulty::difficulty_fn;
use std::boxed::Box;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;
use std::collections::HashMap;
use dashmap::DashMap;
use tokio::sync::broadcast;
use bytes::*;
use bincode_next::encode_into_slice;

const MAX_GEN_ATTEMPTS: u8 = 48;
const DIFFICULTY_LEVEL: u8 = 2;


#[derive(Debug)]
pub struct AbstractWorld<W: WorldGrid> {
    pub world: W,
    players: DashMap<Id, AbstractPlayer>,
    global_difficulty: f32,
    pub queue_new_obstacles: Vec<Bytes>, // type provisoire
    pub clock: Instant,
    pub tx: broadcast::Sender<bytes::Bytes>
}

impl AbstractWorld<VecGrid> {
    pub fn new(x: u8, y: u8, max_players: u16, tx: broadcast::Sender<bytes::Bytes>) -> Self {
        Self {
            world: VecGrid::new_empty(x, y),
            players: DashMap::with_capacity(max_players as usize),
            global_difficulty: 0.0,
            //queue_new_obstacles: RwLock::new(Vec::new()),
            queue_new_obstacles: Vec::new(),
            clock: Instant::now(),
            tx
        }
    }

    pub fn generate_obstacles(&mut self) -> Vec<Bytes> {
        let mut new_obstacles: Vec<Bytes> = Vec::with_capacity(self.world.len_x() * self.world.len_y() / 10 + 3); //random approximation
        let mut target_difficulty = difficulty_fn(DIFFICULTY_LEVEL)(self.get_now());
        
        for _ in 0..MAX_GEN_ATTEMPTS {
            if self.global_difficulty >= target_difficulty { break }
            
            let choice = ObstacleType::random_implemented_type();
            let now = self.clock;
            let grid = &mut self.world;
            
            
            if let Some((gained_difficulty, mut obstacle)) = ObstacleType::construct(choice, now, grid) {
                self.global_difficulty += gained_difficulty;
                target_difficulty += gained_difficulty;

                if let ObstacleBytes::WillBeSent(bytes) = &mut obstacle {
                    new_obstacles.push(bytes.clone());
                }
            } else { continue }
        }
        
        new_obstacles
    }
    
    #[inline]
    pub fn add_new_obstacles_to_queue(&mut self, mut obstacles_bytes: Vec<Bytes>) {
        //for RwLock *self.queue_new_obstacles.write().expect("Error on writing to new obstacles queue").append(bytes);
        self.queue_new_obstacles.append(&mut obstacles_bytes);
    }
    
    pub fn get_player_states(&self) -> Vec<bytes::Bytes> {
        let mut buf_vec: Vec<Bytes> = Vec::with_capacity(self.players.len());
        
        for entry in &self.players {
            buf_vec.push(from_server::PlayerUpdate::from(*entry.value()).encode());
        }
        
        buf_vec
    }
    
    pub fn get_now(&self) -> Instant {
        self.clock
    }
    
    pub fn flush_new_obstacles_queue(&mut self) -> Vec<Bytes> {
        let mut out: Vec<Bytes> = Vec::with_capacity(self.queue_new_obstacles.len());
        out.append(&mut self.queue_new_obstacles);
        out
    }
}
