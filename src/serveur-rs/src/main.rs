use serde::{Deserialize, Serialize};
use serde_json::error::Category::Data;
use tokio_tungstenite::accept_async;
use std::{
    fs::read, net::SocketAddr, sync::{Arc, RwLock}, time::{Duration, Instant},
    
};
use tokio::{
    io::AsyncReadExt, net::{TcpListener, TcpStream}, sync::{RwLock as tokio_RwLock, broadcast}, time::{interval, sleep},
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
mod global_difficulty;

use sha2::{self, Digest, Sha256};

use crate::{args::process_args, world_grid::{WorldGrid, vec_grid::VecGrid}};

const TIME_BEFORE_START_OBSTACLE_GEN: Duration = Duration::from_secs(3);

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
    
    let cfg = process_args();
    println!("{}", cfg.addr());
    
    let addr = cfg.addr();
    
    let listener = TcpListener::bind(&addr).await.expect("Failed to bind TcpListener");
    println!("Listening on {addr}");
    
    let (tx, _rx) = tokio::sync::broadcast::channel::<bytes::Bytes>(128);
    
    let abstract_world = AbstractWorld::new(cfg.size_x, cfg.size_y, cfg.max_players, tx);
    //let world_grid = Arc::new(abstract_world.world);
    
    let world = Arc::new(RwLock::new(abstract_world));
    
    let loop_state_world = world.clone();
    let obstacles_world = world.clone();
    
    tokio::spawn(async move {
        let mut ticker = interval(Duration::from_millis(50));
        
        loop {
            ticker.tick().await;
            
            let mut collected_player_states = { //for dropping lock
                loop_state_world.read().expect("POISOM!").get_player_states()
            };
            
            let should_flush = {
                loop_state_world.read().expect("Tried getting obstacle queue len").queue_new_obstacles.len() > 0
            };
            //let new_obstacles = loop_state_world.flush_new_obstacles_queue();
            //let mut new_obstacles = loop_state_world.write().await.queue_new_obstacles.clone();
            let mut new_obstacles: Vec<bytes::Bytes> = {
                if should_flush { 
                    loop_state_world.write().expect("POISON!!").flush_new_obstacles_queue()
                } else { Vec::new() }
            };
            
            collected_player_states.append(&mut new_obstacles);
            
            let collected_states_as_bytes = build_grand_packet(collected_player_states);
            
            
            if !collected_states_as_bytes.is_empty() {
                _ = loop_state_world.read().expect("POISON!!!!").tx.send(collected_states_as_bytes)
            }
        }
    });
    
    // Obstacles
    tokio::spawn(async move {
        _ = sleep(TIME_BEFORE_START_OBSTACLE_GEN).await;
        let mut ticker = interval(Duration::from_secs(1));
        
        
        loop {
            ticker.tick().await;
            let now = { 
                obstacles_world.read().expect("Slow cycle POISON! trying to get the time 🕛").get_now()
            };
            
            {
                obstacles_world.write().expect("Poison trying to garbage collect").world.garbage_collect(now);
            }
            let new_obstacles = {
                obstacles_world.write().expect("Poison trying to generate obstacles").generate_obstacles() 
            };

            obstacles_world
                .write()
                .expect("Poison trying to add obstacles to queue")
                .add_new_obstacles_to_queue(new_obstacles);

            println!("============================================");
        }
    });
    
    while let Ok((stream, peer_addr)) = listener.accept().await {
        let connection_state = world.clone();
        tokio::spawn(handle_connections(stream, peer_addr, connection_state));
    }
    
    
    
}

async fn handle_connections(stream: TcpStream, addr: SocketAddr, state: Arc<RwLock<AbstractWorld<VecGrid>>>) {
    let websock_stream = match accept_async(stream).await {
        Ok(sock) => sock,
        Err(e) => {
            eprintln!("WebSocket nono for {}: {}", addr, e);
            return;
        }
    };
    let mut initial_buf: [u8; 1024] = [0; 1024];
    
    println!("ADDD {}", addr.to_string());
    
    let player_id = 9u32;
}

pub fn handle_connections2(stream: TcpStream, addr: SocketAddr, state: Arc<RwLock<AbstractWorld<VecGrid>>>) {
    let sender = {
        if let Ok(s) = state.read() {
            s.tx.clone()
        } else {
            println!("Some connection failed to get a lock to the World");
            return;
        }
    };
    
    let receiver = sender.subscribe();
    
    
}
