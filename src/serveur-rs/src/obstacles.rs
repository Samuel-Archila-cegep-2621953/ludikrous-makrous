use crate::utils::select_random;
use crate::world_grid::WorldGrid;
use dyn_clone::DynClone;
use std::fmt::Debug;
use std::time::Instant;

pub mod pillar;
pub mod missile;
pub mod placeholder;
use pillar::Pillar;
use missile::Missile;
use placeholder::TilePlaceHolder;
use crate::world_grid::hashed_grid::HashedGrid;

pub const IMPLEMENTED_OBSTACLES: [ObstacleType; 3] = [
    ObstacleType::Nothing,
    ObstacleType::Pillar,
    ObstacleType::Missile,
];

//type ObstacleConstructor<T: WorldGrid> = fn(Instant, &mut T) -> Option<(f32, ObstacleBytes)>;//(fn(Instant, &mut _) -> Option<_> {<_ as Obstacle>::try_spawn::<_>});

#[repr(u8)]
#[derive(Debug, Clone, Copy)]
pub enum ObstacleType {
    Nothing = 0,
    Pillar = 2,
    Missile = 5
}

impl ObstacleType {
    pub fn random_implemented_type() -> ObstacleType {
        let len = IMPLEMENTED_OBSTACLES.len();
        let choice = select_random(len as u8) as usize - 1;
        
        IMPLEMENTED_OBSTACLES[choice]
    }
    
    /*
    fn get_constructor(ty: Self) -> ObstacleConstructor<HashedGrid> {
        match ty {
            Self::Nothing => TilePlaceHolder::try_spawn,
            Self::Pillar => Pillar::try_spawn,
            Self::Missile => Missile::try_spawn
        }
    } */
    
    pub fn construct(ty: Self, server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)> {
        match ty {
            Self::Nothing => TilePlaceHolder::try_spawn(server_time, grid),
            Self::Pillar => Pillar::try_spawn(server_time, grid),
            Self::Missile => Missile::try_spawn(server_time, grid),
        }
    }
}


#[derive(Debug, Clone)]
pub enum ObstacleBytes {
    WillBeSent(Vec<u8>),
    PurelyAbstract,
}

pub trait Obstacle: Debug {

    fn is_dead(&self, now: Instant) -> bool;
    
    fn try_spawn(server_time: Instant, grid: &mut impl WorldGrid) -> Option<(f32, ObstacleBytes)>
        where Self: Sized;
        
    fn into_box(self) -> Box<Self> 
        where Self: Sized
    {
        Box::new(self)
    }
}
