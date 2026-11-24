use crate::joueur_abstrait::AbstractPlayer;
use crate::obstacles::Obstacle;
use crate::utils::Vec2;
use std::boxed::Box;
use std::iter::repeat_with;
use std::sync::{Arc, RwLock};
use std::time::Instant;

#[derive(Debug)]
pub struct AbstractWorld {
    world: Vec<Vec<Option<Box<dyn Obstacle>>>>,
    players: Vec<AbstractPlayer>,
    queue_new_obstacles: Arc<RwLock<Vec<u8>>>, // type provisoire
    pub debut: Instant
}

impl AbstractWorld {
    fn new(x: u16, y: u16) -> Self {
        let monde: Vec<Vec<Option<Box<dyn Obstacle>>>> =
            repeat_with(|| repeat_with(|| None).take(x as usize).collect())
                .take(y as usize)
                .collect();

        Self {
            world: monde,
            players: Vec::new(),
            queue_new_obstacles: Arc::new(RwLock::new(Vec::new())),
            debut: Instant::now()
        }
    }
}
