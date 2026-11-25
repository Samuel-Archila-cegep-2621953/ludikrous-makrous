use crate::obstacles::*;
use crate::utils::*;
use bincode_next::encode_to_vec;
use serde::Serialize;
use std::boxed::Box;
use std::time::{Duration, Instant};
use bincode_next::{Encode, encode_into_slice};

const PILLAR_DURATION: Duration = Duration::from_secs(7);
const MAX_ATTEMPTS: u8 = 8;

#[derive(Debug, Serialize, Encode)]
struct SerializedPillar {
    pkt_ty: u8,
    ty: u8,
    x: u8,
    y: u8,
    h_mode: u8,
}

impl SerializedPillar {
    #[inline]
    fn encode_to_vec(self) -> Vec<u8> {
        encode_to_vec(self, DEFAULT_BINCODE_CFG).expect("Bincode failed to encode Pillar")
    }
    
    #[inline]
    fn from(x: u8, y: u8, h_mode: u8) -> Self {
        Self {
            pkt_ty: FromServerPacketTypes::ObstacleUpdate as u8, 
            ty: ObstacleType::Pillar as u8,
            x,
            y,
            h_mode
        }
    }
}


#[derive(Debug, Clone)]
pub struct Pillar {
    death_foretold: Instant,
    h_mode: u8,
    difficulty: f32,
}

impl Pillar {
    fn new(instant: Instant) -> Self {
        let h_mode = select_random(5);
        let difficulty = 0.1 * h_mode as f32;
        let death_foretold = instant + PILLAR_DURATION;

        Self {
            death_foretold,
            h_mode,
            difficulty
        }
    }

    /*
    #[inline]
    fn into_box(self) -> Box<Self> {
        Box::new(self)
    } */
    
    
    #[inline]
    fn as_serialized(&self, x: u8, y: u8) -> SerializedPillar {
        SerializedPillar::from(x, y, self.h_mode)
    }
}

impl Obstacle for Pillar {
    fn try_spawn(server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)> {
        for _ in 0..MAX_ATTEMPTS {
            let tile = grid.random_tile();

            if !grid.is_free(tile) {
                continue;
            }
            let pillar = Pillar::new(server_time);
            let difficulty = pillar.difficulty;
            let bytes = pillar.as_serialized(tile.x, tile.y).encode_to_vec();
            
            grid.set(tile, pillar.into_box());
            
            return Some((difficulty, ObstacleBytes::WillBeSent(bytes)));
        }
        None
    }

    #[inline]
    fn is_dead(&self, now: Instant) -> bool {
        self.death_foretold >= now
    }
}
