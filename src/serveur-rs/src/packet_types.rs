#[derive(Debug, Clone, Copy)]
#[repr(u8)]
pub enum FromServerPacketTypes {
    PlayerUpdate = 0,
    LoginSuccess = 1,
    LoginFailure = 2,
    ObstacleUpdate = 3,
    Disconnect = 4
}