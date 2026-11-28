use serde::{Deserialize, Serialize};
use serde_json::error::Category::Data;
use std::{
    fs::read,
    net::SocketAddr,
    sync::{Arc, RwLock},
    time::{Duration, Instant},
};
use tokio::{
    io::AsyncReadExt,
    net::{TcpListener, TcpStream},
    sync::{RwLock as tokio_RwLock, broadcast},
    time::{interval, sleep},
};
use tokio_tungstenite::accept_async;
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
mod args;
mod config;
mod packet_types;
use config::Config;
mod global_difficulty;

use sha2::{self, Digest, Sha256};

use crate::{
    args::process_args,
    world_grid::{WorldGrid, vec_grid::VecGrid},
};

const TIME_BEFORE_START_OBSTACLE_GEN: Duration = Duration::from_secs(3);

//static mut CONFIG: Config = process_args();

#[tokio::main]
async fn main() {
    /* */
    let hashed = &*Sha256::digest(b"\0");
    //let a = hex::encode(hashed);

    let CONFIG: Config = process_args();
    let db = Database::open();
    let r = db.user_exists("u2");
    let p = db.password_matches("u2", hashed);
    println!("Hello, world! {r}");
    println!("Hello, world! {p}");

    println!("{}", CONFIG.addr());

    let addr = CONFIG.addr();

    let listener = TcpListener::bind(&addr)
        .await
        .expect("Failed to bind TcpListener");
    println!("Listening on {addr}");

    let (tx, _rx) = tokio::sync::broadcast::channel::<bytes::Bytes>(128);

    let abstract_world = AbstractWorld::new(CONFIG.size_x, CONFIG.size_y, CONFIG.max_players, tx);
    let players = Arc::new(abstract_world.players);
    let world_grid = Arc::new(RwLock::new(abstract_world.world));
    //let server_time = Arc::new(abstract_world.clock);
    let obstacles_queue = Arc::new(RwLock::new(abstract_world.new_obstacles_queue));

    //let world = Arc::new(RwLock::new(abstract_world));
    let tx = abstract_world.tx.clone();

    let fast_loop_players_handle = Arc::clone(&players);
    let fast_loop_obstacles_handle = Arc::clone(&world_grid);
    let fast_loop_obstacles_queue_handle = Arc::clone(&obstacles_queue);
    let fast_loop_tx_handle = tx.clone();

    let obstacles_loop_world = Arc::clone(&world_grid);
    //let obstacles_loop_clock = Arc::clone(&server_time);
    let obstacles_loop_new_queue = Arc::clone(&obstacles_queue);

    tokio::spawn(async move {
        let mut ticker = interval(Duration::from_millis(50));

        loop {
            ticker.tick().await;

            let mut collected_player_states = {
                //for dropping lock
                /*
                loop_state_world
                    .read()
                    .expect("POISOM!")
                    .get_player_states()
                */
                fast_loop_players_handle.get_player_states()
            };

            let should_flush = {
                fast_loop_obstacles_queue_handle
                    .read()
                    .expect("Tried getting obstacle queue len")
                    .len() > 0
                //*/
                //fast_loop_obstacles_queue_handle.len() > 0
            };
            //let new_obstacles = loop_state_world.flush_new_obstacles_queue();
            //let mut new_obstacles = loop_state_world.write().await.queue_new_obstacles.clone();
            let mut new_obstacles: Vec<bytes::Bytes> = {
                if should_flush {
                    fast_loop_obstacles_queue_handle
                        .write()
                        .expect("Tried flushing queue")
                        .flush_new_obstacles_queue()
                } else {
                    Vec::new()
                }
            };

            collected_player_states.append(&mut new_obstacles);

            let collected_states_as_bytes = build_grand_packet(collected_player_states);

            if !collected_states_as_bytes.is_empty() {
                _ = fast_loop_tx_handle.send(collected_states_as_bytes);
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
                obstacles_loop_world
                    .write()
                    .expect("Failed getting time in obstacles")
                    .get_now() 
            };

            {
                obstacles_loop_world
                    .write()
                    .expect("Tried garbage collecting")
                    .garbage_collect();
            }
            let new_obstacles = {
                obstacles_loop_world
                    .write()
                    .expect("Poison trying to generate obstacles")
                    .generate_obstacles()
            };

            /*
            obstacles_world
                .write()
                .expect("Poison trying to add obstacles to queue")
            */
            obstacles_loop_new_queue
                .write()
                .expect("Poison trying to add obstacles to queue")
                .append(new_obstacles);

            println!("============================================");
        }
    });

    while let Ok((stream, peer_addr)) = listener.accept().await {
        let connection_state = Arc::clone(&players);
        tokio::spawn(handle_connections2(stream, peer_addr, connection_state, tx.clone()));
    }
}

async fn handle_connections(
    stream: TcpStream,
    addr: SocketAddr,
    state: Arc<RwLock<AbstractWorld<VecGrid>>>,
) {
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

pub async fn handle_connections2(
    stream: TcpStream,
    addr: SocketAddr,
    state: Arc<AbstractPlayerStates>,
    tx: tokio::sync::broadcast::Sender<bytes::Bytes>
) {
    /*
    let sender = {
        if let Ok(s) = *state {
            s.tx.clone()
        } else {
            println!("Some connection failed to get a lock to the World");
            return;
        }
    };
     */
    let sender = tx;

    let receiver = sender.subscribe();
}
