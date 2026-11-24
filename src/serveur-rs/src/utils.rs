use std::range::Range;

use serde::Serialize;
use rand::{rng, random, random_range};

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec2(pub f32, pub f32);

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec3(pub f32, pub f32, pub f32);

pub fn select_random(max: u8) -> u8 {
    random_range(0..=max)
}