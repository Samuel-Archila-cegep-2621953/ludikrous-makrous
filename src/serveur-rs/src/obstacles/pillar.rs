use crate::obstacles::*;
use crate::utils::*;
use bincode_next::encode_to_vec;
use rand::{random, rng};
use serde::Serialize;
use std::boxed::Box;
use std::convert::From;
use std::time::{Duration, Instant};
use bincode_next::{Encode, encode_into_slice};

const PILLAR_DURATION: Duration = Duration::from_secs(7);
const MAX_ATTEMPTS: u8 = 8;

#[derive(Debug, Serialize, Encode)]
struct SerializedPillar {
    ty: u8,
    x: u8,
    y: u8,
    h_mode: u8,
}

impl SerializedPillar {
    fn encode_to_vec(self) -> Vec<u8> {
        encode_to_vec(self, DEFAULT_BINCODE_CFG).expect("Bincode failed to encode Pillar")
    }
    
    fn from(x: u8, y: u8, h_mode: u8) -> Self {
        Self {
            ty: ObstacleType::Pillar as u8,
            x,
            y,
            h_mode
        }
    }
}


#[derive(Debug, Clone)]
struct Pillar {
    death: Instant,
    h_mode: u8,
    difficulty: f32,
}

impl Pillar {
    fn new(instant: Instant) -> Self {
        let h_mode = select_random(5);
        let difficulty = 0.1 * h_mode as f32;
        let death = instant + PILLAR_DURATION;

        Self {
            death,
            h_mode,
            difficulty
        }
    }

    fn into_box(self) -> Box<Self> {
        Box::new(self)
    }
    
    fn as_serialized(&self, x: u8, y: u8) -> SerializedPillar {
        SerializedPillar::from(self.h_mode, x, y)
    }
}

impl Obstacle for Pillar {
    fn try_spawn(maintenant: Instant, grid: &mut WorldGrid) -> Option<f32> {
        for _ in 0..MAX_ATTEMPTS {
            let random_position = grid.select_random_grid_position();

            if !grid.is_free(random_position.0, random_position.1) {
                continue;
            }
            let pillar = Pillar::new(maintenant);
            let difficulty = pillar.difficulty;
            
            grid.set(random_position, pillar.into_box());
            
            return Some(difficulty);
        }
        None
    }

    fn as_bytes(&self, aoe: ObstacleAoe) -> Vec<u8> {
        self.as_serialized(x, y)
    }

    fn is_dead(&self, now: Instant) -> bool {
        self.mort >= now
    }
}
