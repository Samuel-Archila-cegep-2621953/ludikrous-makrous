use crate::obstacles::*;
use crate::utils::*;
use bincode_next::encode_to_vec;
use serde::Serialize;
use std::boxed::Box;
use std::time::{Duration, Instant};
use bincode_next::{Encode, encode_into_slice};

const DURATION: Duration = Duration::from_secs(12);
const MAX_ATTEMPTS: u8 = 8;

#[derive(Debug)]
pub struct TilePlaceHolder {
    death_foretold: Instant
}

impl TilePlaceHolder {
    fn new(born: Instant) -> Self {
        Self { death_foretold: born + DURATION }
    }
}

impl Obstacle for TilePlaceHolder {
    fn is_dead(&self, now: Instant) -> bool {
        self.death_foretold >= now
    }
    
    fn try_spawn(server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)>
        where Self: Sized
    {
        if select_random(2) != 0 { return None } // 1/3 chance of success
        
        for _ in 0..MAX_ATTEMPTS {
            let tile = grid.random_tile();
            if !grid.is_free(tile) { continue }
            
            let placeholder = TilePlaceHolder::new(server_time);
            
            grid.set(tile, placeholder.into_box());
            
            println!("Gen placeholder");
            return Some((0.0, ObstacleBytes::PurelyAbstract));
        }
        None
    }
    
}