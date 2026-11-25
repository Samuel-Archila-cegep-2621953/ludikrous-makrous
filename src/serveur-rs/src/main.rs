use serde::{Deserialize, Serialize};
use serde_json::error::Category::Data;
use std::{
    net::SocketAddr,
    sync::Arc,
    time::{Duration, Instant},
};
use tokio::{
    net::{TcpListener, TcpStream},
    sync::broadcast,
    time::interval
};
mod abstract_player;
use abstract_player::*;

mod obstacles;
use obstacles::*;

mod abstract_world;
use abstract_world::*;

mod utils;
use utils::*;

mod world_grid;

mod database;
mod login;
use database::*;
mod packet_types;
mod args;
mod config;

use sha2::{self, Digest, Sha256};

#[tokio::main]
async fn main() {
    /* */
    let hashed = &*Sha256::digest(b"\0");
    //let a = hex::encode(hashed);
    
    
    let db = Database::open();
    let r = db.user_exists("u2");
    let p = db.password_matches("u2", hashed);
    println!("Hello, world! {r}");
    println!("Hello, world! {p}");
}
