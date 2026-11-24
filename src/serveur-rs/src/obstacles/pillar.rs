use crate::obstacles::*;
use crate::utils::*;
use rand::{random, rng};
use serde::Serialize;
use std::boxed::Box;
use std::convert::From;
use std::time::{Duration, Instant};

const PILLAR_DURATION: Duration = Duration::from_secs(7);
const MAX_ATTEMPTS: u8 = 8;

#[derive(Debug, Serialize)]
struct PillarSerialized {
    ty: u8,
    mode_hauteur: u8,
}

impl From<Pillar> for PillarSerialized {
    fn from(item: Pillar) -> Self {
        Self {
            ty: ObstacleType::PILLAR,
            mode_hauteur: item.mode_hauteur,
        }
    }
}

#[derive(Debug)]
struct Pillar {
    mort: Instant,
    mode_hauteur: u8,
    difficulty: f32,
}

impl Pillar {
    fn new(instant: Instant) -> Self {
        let mode_hauteur = select_random(5);
        let diff = 0.1 * mode_hauteur as f32;
        let mort = instant + PILLAR_DURATION;

        Self {
            mort,
            mode_hauteur,
            difficulty: diff,
        }
    }

    fn into_box(self) -> Box<Self> {
        Box::new(self)
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

    fn as_bytes(&self) -> Vec<u8> {
        Vec::new()
    }

    fn is_dead(&self, now: Instant) -> bool {
        self.mort >= now
    }
}
