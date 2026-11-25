use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct PlayerUpdate {
    ty: u8,
    no_idea: u32,
    display_name: [u8; 16],
    x: i32,
    y: i32,
    z: i32,
    health: u8,
    animation: u8,
    rotation: f32
}

#[derive(Debug, Serialize)]
pub struct LoginSuccess {
    ty: u8,
    no_idea: i32,
    message: [u8; 32]
}

#[derive(Debug, Serialize)]
pub struct LoginFailure {
    ty: u8,
}

#[derive(Debug, Serialize)]
pub struct ObstacleUpdate {
    ty: u8,
}

#[derive(Debug, Serialize)]
pub struct Logout {
    ty: u8,
}