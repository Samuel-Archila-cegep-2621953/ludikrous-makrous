use crate::obstacles::*;
use crate::utils::*;
use crate::packet_types::FromServerPacketTypes;
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
    
    /*
    #[inline]
    fn into_box(self) -> Box<Self> {
        Box::new(self)
    } */
    
    #[inline]
    fn as_serialized(&self, x: u8, y: u8) -> SerializedMissile {
        SerializedMissile::from(x, y)
    }
}

#[derive(Encode, Debug)]
struct SerializedMissile {
    pkt_ty: u8,
    ty: u8,
    x: u8,
    y: u8
}

impl SerializedMissile {
    #[inline]
    fn encode_to_bytes(self) -> bytes::Bytes {
        bytes::Bytes::from(encode_to_vec(self, DEFAULT_BINCODE_CFG).expect("Bincode failed to encode Missile"))
    }
    
    #[inline]
    fn from(x: u8, y: u8) -> Self {
        Self {
            pkt_ty: FromServerPacketTypes::ObstacleUpdate as u8,
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
            let tile = grid.random_tile();
            
            if !grid.is_free(tile) { continue }
            
            let missile = Missile::new(server_time);
            let bytes = missile.as_serialized(tile.x, tile.y).encode_to_bytes();
            
            grid.set(tile, missile.into_box());
            
            println!("Gen missile");
            return Some((
                DIFFICULTY,
                ObstacleBytes::WillBeSent(bytes)
            ))
        }
        None
    }
    
    #[inline]
    fn is_dead(&self, now: Instant) -> bool {
        self.death_foretold >= now
    }
}