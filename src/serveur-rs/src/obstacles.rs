use crate::abstract_world::WorldGrid;
use dyn_clone::DynClone;
use std::fmt::Debug;
use std::time::Instant;

pub mod pillar;

pub struct ObstacleType;
impl ObstacleType {
    const NOTHING: u8 = 0;
    const PILLAR: u8 = 1;
    const MISSILE: u8 = 5;
}

pub trait Obstacle: Debug {
    fn as_bytes(&self) -> Vec<u8>;
    fn try_spawn(maintenant: Instant, grid: &mut WorldGrid) -> Option<f32>
    where
        Self: Sized;

    fn is_dead(&self, now: Instant) -> bool;
}
