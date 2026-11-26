use bincode_next::config::{self, Configuration};
use rand::{random, random_range, rng};
use serde::Serialize;
use std::range::Range;
use bytes::*;

pub const DEFAULT_BINCODE_CFG: bincode_next::config::Configuration<
    bincode_next::config::BigEndian,
    bincode_next::config::Fixint,
    bincode_next::config::NoLimit,
    bincode_next::config::AllowBitPacking,
    bincode_next::config::MsbFirst,
> = config::standard() // Son what is this type 😭
    .with_big_endian()
    .with_fixed_int_encoding()
    .with_bit_packing();


#[derive(Debug, Serialize, PartialEq, PartialOrd, Clone, Copy)]
pub struct Vec2(pub f32, pub f32);

#[derive(Debug, Serialize, PartialEq, PartialOrd, Clone, Copy)]
pub struct Vec3(pub f32, pub f32, pub f32);

#[derive(Debug, Serialize, PartialEq, PartialOrd, Clone, Copy)]
pub struct FalseVec3(pub i32, pub i32, pub i32);

#[inline]
pub fn select_random(max: u8) -> u8 {
    random_range(0..=max)
}

pub fn is_ip_valid(candidate: &str) -> bool {
    const ALLOWED_CHARS: [char; 11] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']; 
    if !candidate.chars().all(|c| ALLOWED_CHARS.contains(&c)) { return false }
    
    let sp: Vec<&str> = candidate.split('.').collect();
    if sp.len() != 4 { return false }
    
    for seg in sp {
        if seg.chars().count() > 3 { return false }
        
        let res = seg.parse::<u8>();
        if res.is_err() { return false }
    }
    
    true
}

pub fn build_grand_packet(b: Vec<Bytes>) -> Bytes {
    let mut buf = BytesMut::with_capacity(64);
    buf.put_u16(b.len() as u16); // header for number of packets
    
    for packet in b {
        buf.extend_from_slice(&packet);
    }
    
    Bytes::from(buf)
}

pub fn bytes_from_vecu8(v: Vec<u8>) -> Bytes {
    Bytes::from(v)
}