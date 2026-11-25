use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct PlayerUpdate {
    //ty: u8,
    name: [u8; 32],
    x: f32,
    y: f32,
    z: f32,
    health: u8,
    animation: u8,
    rotation: f32
}

#[derive(Debug, Deserialize)]
pub struct LoginSuccess {
    //ty: u8,
    name: [u8; 16],
    passwd: [u8; 32],
}


#[derive(Debug, Deserialize)]
pub struct AccountCreation {
    //ty: u8,
    name: [u8; 16],
    passwd: [u8; 32],
}

#[derive(Debug, Deserialize)]
pub struct Logout {
    //ty: u8,
    session: [u8; 32]
}