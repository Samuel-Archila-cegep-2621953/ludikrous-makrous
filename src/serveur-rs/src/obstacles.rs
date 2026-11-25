use crate::abstract_world::WorldGrid;
use dyn_clone::DynClone;
use std::fmt::Debug;
use std::time::Instant;

pub mod pillar;

#[repr(u8)]
#[derive(Debug)]
pub enum ObstacleType {
    Nothing = 0,
    Pillar = 2,
    Missile = 5
}

#[derive(Debug, Clone, Copy)]
pub enum ObstacleAoe {
    Localized(u8, u8),
    Global(u8),
}

pub trait Obstacle: Debug {
    fn as_bytes(&self, aoe: ObstacleAoe) -> Vec<u8>;
    fn try_spawn(maintenant: Instant, grid: &mut WorldGrid) -> Option<f32>
    where
        Self: Sized;

    fn is_dead(&self, now: Instant) -> bool;
    
    fn aoe(&self) -> ObstacleAoe;
}
