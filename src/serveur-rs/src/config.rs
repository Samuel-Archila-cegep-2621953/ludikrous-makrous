use std::default::Default;

#[derive(Debug)]
pub struct Config {
    pub ip: String,
    pub port: u16,
    pub max_players: u16,
    pub size_x: u8,
    pub size_y: u8,
}

impl Config {
    #[inline]
    pub fn addr(&self) -> String {
        format!("{}:{}", self.ip, self.port)
    }
    
    pub fn set_ip(&mut self, ip: &str) { self.ip = ip.to_string() }
    pub fn set_port(&mut self, port: u16) { self.port = port }
    pub fn set_max_players(&mut self, max_players: u16) { self.max_players = max_players }
    pub fn set_size_x(&mut self, size_x: u8) { self.size_x = size_x }
    pub fn set_size_y(&mut self, size_y: u8) { self.size_x = size_y }
}

impl Default for Config {
    fn default() -> Self {
        Self {
            ip: String::from("127.0.0.1"),
            port: 9004,
            max_players: 4,
            size_x: 8,
            size_y: 8
        }
    }
}