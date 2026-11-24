use rand::{random, rng};

use crate::obstacles::Obstacle;

const DUREE_PILIER: f32 = 7.0;

#[derive(Debug)]
struct Pilier {
    mort: f32,
    mode_hauteur: u8,
}

impl Obstacle for Pilier {
    fn try_spawn(temps_maintenant: f32) -> Option<f32> {
        let temp = [6u8; 8];

        None
    }

    fn as_bytes(&self) -> Vec<u8> {
        Vec::new()
    }
}
