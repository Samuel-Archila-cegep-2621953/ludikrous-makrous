use serde::Serialize;

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec2(pub f32, pub f32);

#[derive(Debug, Serialize, PartialEq, PartialOrd)]
pub struct Vec3(pub f32, pub f32, pub f32);
