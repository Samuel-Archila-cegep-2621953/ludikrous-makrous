use serde::{Serialize, Deserialize};
use std::{net::SocketAddr, sync::Arc, time::{Duration, Instant}};

mod abstract_player;
use abstract_player::*;

mod obstacles;
use obstacles::*;

mod abstract_world;
use abstract_world::*;

mod utils;
use utils::*;

mod world_grid;

fn main() {
    println!("Hello, world!");
}
