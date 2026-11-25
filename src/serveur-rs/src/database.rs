use rusqlite::{Connection, Result as DbResult, params};
use sha2::Digest;

const DB_PATH: &str = "assets/server.db";

pub struct Database {
    connection: rusqlite::Connection
}

#[derive(Debug, PartialEq, Eq)]
pub struct UserData {
    username: String,
    passwd: String,
    id: u32
}

impl Database {
    pub fn open() -> Self {
        let connection = Connection::open(DB_PATH).expect("Failed to open db connection");
        {
            let mut create = connection.prepare("
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    passwd TEXT NOT NULL,
                    creation_date TEXT DEFAULT (datetime('now', 'localtime'))
                )
            ").expect("Table creation statement error");
            _ = create.execute([]);
        }
        
        Self { connection }
    }
    
    pub fn user_exists(&self, username: &str) -> bool {
        let mut statement = self.connection.prepare("SELECT id FROM users WHERE username = ?1").expect("Db stmt err");
        
        statement.exists(params![username]).expect("Error verifying if user exists")
    }
    
    ///Hashes once
    pub fn password_matches(&self, username: &str, passwd: &[u8]) -> bool {
        let mut statement = self.connection.prepare("SELECT passwd FROM users WHERE username = ?1").expect("Db stmt err");
        let double_hashed_passwd = hex::encode(sha2::Sha256::digest(passwd));
        
        let real_passwd: String = statement.query_one([username], |row| row.get(0)).expect("Error getting passwd from db");
        
        double_hashed_passwd == real_passwd.as_str()
    }
}
