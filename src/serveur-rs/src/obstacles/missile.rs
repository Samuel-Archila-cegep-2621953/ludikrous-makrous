use crate::obstacles::*;
use crate::utils::*;
use bincode_next::encode_to_vec;
use serde::Serialize;
use std::boxed::Box;
use std::time::{Duration, Instant};
use bincode_next::{Encode, encode_into_slice};

const MAX_ATTEMPS: u8 = 8;
const DIFFICULTY: f32 = 3.0;
const DURATION: Duration = Duration::from_secs(5);

#[derive(Debug)]
pub struct Missile {
    death_foretold: Instant,
    difficulty: f32
}

impl Missile {
    fn new(instant: Instant) -> Self {
        let death_foretold = instant + DURATION;
        let difficulty = DIFFICULTY;
        
        Self {
            death_foretold,
            difficulty
        }
    }
    
    fn into_box(self) -> Box<Self> {
        Box::new(self)
    }
    
    fn as_serialized(&self, x: u8, y: u8) -> SerializedMissile {
        SerializedMissile::from(x, y)
    }
}

#[derive(Encode, Debug)]
struct SerializedMissile {
    ty: u8,
    x: u8,
    y: u8
}

impl SerializedMissile {
    fn encode_to_vec(self) -> Vec<u8> {
        encode_to_vec(self, DEFAULT_BINCODE_CFG).expect("Bincode failed to encode Missile")
    }
    
    fn from(x: u8, y: u8) -> Self {
        Self {
            ty: ObstacleType::Missile as u8,
            x,
            y
        }
    }
}


impl Obstacle for Missile {
    fn try_spawn(server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)>
    where
        Self: Sized
    {
        if select_random(1) == 0 { return None } // 50% Chance of generation failure
        
        for _ in 0..MAX_ATTEMPS {
            let (x, y) = grid.select_random_grid_position();
            
            if !grid.is_free(x, y) { continue }
            
            let missile = Missile::new(server_time);
            let bytes = missile.as_serialized(x, y).encode_to_vec();
            
            grid.set((x, y), missile.into_box());
            
            return Some((
                DIFFICULTY,
                ObstacleBytes::WillBeSent(bytes)
            ))
        }
        None
    }
    
    fn is_dead(&self, now: Instant) -> bool {
        self.death_foretold >= now
    }
}