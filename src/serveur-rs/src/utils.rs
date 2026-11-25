use bincode_next::config::{self, Configuration};
use rand::{random, random_range, rng};
use serde::Serialize;
use std::range::Range;

pub const DEFAULT_BINCODE_CFG: bincode_next::config::Configuration<
    bincode_next::config::BigEndian,
    bincode_next::config::Fixint,
    bincode_next::config::NoLimit,
    bincode_next::config::AllowBitPacking,
    bincode_next::config::MsbFirst,
> = config::standard()
    .with_big_endian()
    .with_fixed_int_encoding()
    .with_bit_packing();

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec2(pub f32, pub f32);

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec3(pub f32, pub f32, pub f32);

pub fn select_random(max: u8) -> u8 {
    random_range(0..=max)
}
