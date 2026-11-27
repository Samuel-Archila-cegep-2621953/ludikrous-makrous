use crate::abstract_player::AbstractPlayer;
use crate::abstract_player::*;
use crate::global_difficulty::difficulty_fn;
use crate::obstacles::*;
use crate::packet_types;
use crate::packet_types::from_server;
use crate::utils::*;
use crate::world_grid::{WorldGrid, vec_grid::*};
use bincode_next::encode_into_slice;
use bytes::*;
use dashmap::DashMap;
use std::boxed::Box;
use std::collections::HashMap;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;
use tokio::sync::broadcast;

const MAX_GEN_ATTEMPTS: u8 = 48;
const DIFFICULTY_LEVEL: u8 = 4;

#[derive(Debug)]
pub struct AbstractWorld<W: WorldGrid> {
    pub world: W,
    pub players: AbstractPlayerStates,
    global_difficulty: f32,
    pub new_obstacles_queue: NewObstaclesQueue, // type provisoire
    pub clock: Instant,
    pub tx: broadcast::Sender<bytes::Bytes>,
}

impl AbstractWorld<VecGrid> {
    pub fn new(x: u8, y: u8, max_players: u16, tx: broadcast::Sender<bytes::Bytes>) -> Self {
        Self {
            world: VecGrid::new_empty(x, y),
            players: AbstractPlayerStates::init(max_players),
            global_difficulty: 0.0,
            //queue_new_obstacles: RwLock::new(Vec::new()),
            new_obstacles_queue: NewObstaclesQueue::new(),
            clock: Instant::now(),
            tx,
        }
    }

    pub fn generate_obstacles(&mut self) -> Vec<Bytes> {
        println!("Generatoion +++++++++++++++++");
        let mut new_obstacles: Vec<Bytes> =
            Vec::with_capacity(self.world.len_x() * self.world.len_y() / 10 + 3); //random approximation
        let now = self.get_now();
        //println!("{:?}", now.elapsed().as_secs());
        let mut target_difficulty = difficulty_fn(DIFFICULTY_LEVEL)(now);
        println!("{:?}  {:?}", self.global_difficulty, target_difficulty);

        for _ in 0..MAX_GEN_ATTEMPTS {
            if self.global_difficulty >= target_difficulty {
                println!("break");
                break;
            }

            let choice = ObstacleType::random_implemented_type();
            let now = self.clock;
            let grid = &mut self.world;

            if let Some((gained_difficulty, mut obstacle)) =
                ObstacleType::construct(choice, now, grid)
            {
                self.global_difficulty += gained_difficulty;
                //target_difficulty += gained_difficulty;

                if let ObstacleBytes::WillBeSent(bytes) = &mut obstacle {
                    new_obstacles.push(bytes.clone());
                }
            } else {
                continue;
            }
        }

        new_obstacles
    }

    #[inline]
    pub fn add_new_obstacles_to_queue(&mut self, mut obstacles_bytes: Vec<Bytes>) {
        //for RwLock *self.queue_new_obstacles.write().expect("Error on writing to new obstacles queue").append(bytes);
        self.queue_new_obstacles.append(&mut obstacles_bytes);
    }

    pub fn get_player_states(&self) -> Vec<bytes::Bytes> {
        /*
        let mut buf_vec: Vec<Bytes> = Vec::with_capacity(self.players.len());

        for entry in &self.players {
            buf_vec.push(from_server::PlayerUpdate::from(*entry.value()).encode());
        }

        buf_vec
         */
        self.players.get_player_states()
    }

    pub fn get_now(&self) -> Instant {
        self.clock
    }

    pub fn flush_new_obstacles_queue(&mut self) -> Vec<Bytes> {
        let mut out: Vec<Bytes> = Vec::with_capacity(self.queue_new_obstacles.len());
        out.append(&mut self.queue_new_obstacles);
        println!("Flush");
        out
    }
}

#[derive(Debug)]
struct NewObstaclesQueue(Vec<Bytes>);

impl NewObstaclesQueue {
    pub fn flush_new_obstacles_queue(&mut self) -> Vec<Bytes> {
        let mut out: Vec<Bytes> = Vec::with_capacity(self.len());
        out.append(&mut self.0);
        println!("Flush");
        out
    }
    
    pub fn len(&self) -> usize {
        self.0.len()
    }
    
    pub fn new() -> Self { Self(Vec::new())}
}
