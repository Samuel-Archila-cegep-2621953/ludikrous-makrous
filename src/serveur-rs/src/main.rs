use serde::{Serialize, Deserialize};
use std::{net::SocketAddr, sync::Arc, time::{Duration, Instant}};

mod joueur_abstrait;
use joueur_abstrait::*;

mod obstacles;
use obstacles::*;

mod monde_abstrait;
use monde_abstrait::*;

mod utils;
use utils::*;

fn main() {
    println!("Hello, world!");
}
