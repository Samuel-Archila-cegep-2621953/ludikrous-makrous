use dyn_clone::DynClone;
use std::fmt::Debug;

pub mod pilier;

pub trait Obstacle: Debug {
    fn as_bytes(&self) -> Vec<u8>;
    fn try_spawn(temps_maintenant: f32) -> Option<f32>
        where Self: Sized
    ;
}
