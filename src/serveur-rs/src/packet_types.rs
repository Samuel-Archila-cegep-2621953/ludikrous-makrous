use serde::{Serialize, Deserialize};

pub mod from_client;
pub mod from_server;

#[derive(Debug, Clone, Copy)]
#[repr(u8)]
pub enum FromServerPacketTypes {
    PlayerUpdate = 0,
    LoginSuccess = 1,
    LoginFailure = 2,
    ObstacleUpdate = 3,
    Disconnect = 4
}

impl FromServerPacketTypes {
    pub fn max() -> u8 { 4 }
}

#[derive(Debug, Clone, Copy)]
#[repr(u8)]
pub enum FromClientPacketTypes {
    PlayerUpdate = 0,
    Login = 1,
    AccountCreation = 2,
    Logout = 3
}

impl FromClientPacketTypes {
    pub fn max() -> u8 { 3 }
}