use futures_util::{SinkExt, StreamExt};
use serde::{Serialize, Deserialize};
use std::{
    net::SocketAddr,
    sync::Arc,
    time::Duration
};
use tokio::{
    net::{TcpListener, TcpStream},
    sync::broadcast,
    time::interval
};

pub struct LoginAttempt {

}

fn connection() {
    
}
