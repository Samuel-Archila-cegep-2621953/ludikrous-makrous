use std::default::Default;

pub struct Config {
    pub ip: String,
    pub port: u16,
    pub max_players: u16,
    pub world_size: (u8, u8)
}

impl Config {
    #[inline]
    pub fn addr(&self) -> String {
        format!("{}:{}", self.ip, self.port)
    }
    
    pub fn ip(&mut self, ip: &str) { self.ip = ip.to_string() }
    pub fn port(&mut self, port: u16) { self.port = port }
    pub fn max_players(&mut self, max_players: u16) { self.max_players = max_players }
    pub fn world_size(&mut self, x: u8, y: u8) { self.world_size = (x, y); }
}

impl Default for Config {
    fn default() -> Self {
        Self {
            ip: String::from("127.0.0.1"),
            port: 9004,
            max_players: 4,
            world_size: (8, 8)
        }
    }
}