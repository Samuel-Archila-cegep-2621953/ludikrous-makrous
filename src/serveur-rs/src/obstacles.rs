use crate::world_grid::WorldGrid;
use dyn_clone::DynClone;
use std::fmt::Debug;
use std::time::Instant;

pub mod pillar;
pub mod missile;

#[repr(u8)]
#[derive(Debug)]
pub enum ObstacleType {
    Nothing = 0,
    Pillar = 2,
    Missile = 5
}

#[derive(Debug, Clone)]
pub enum ObstacleBytes {
    WillBeSent(Vec<u8>),
    PurelyAbstract,
}

pub trait Obstacle: Debug {
    //fn as_bytes(&self) -> Vec<u8>;
    fn try_spawn(server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)>
    where
        Self: Sized;

    fn is_dead(&self, now: Instant) -> bool;
}
