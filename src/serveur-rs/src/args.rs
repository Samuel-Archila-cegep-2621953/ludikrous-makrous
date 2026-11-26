use std::env::args;
use crate::config::*;
use crate::utils::is_ip_valid;

const LONE_PARAMS: [&str; 0] = [];
const SINGLE_ARG_PARAMS: [&str; 6] = ["--ip", "-i", "--port", "-p", "--max-players", "-m"];
const DOUBLE_ARG_PARAMS: [&str; 2] = ["--world-size", "-w"];

pub fn process_args() -> Config {
    //let argv = args().map(|s| s.as_str()).collect::<Vec<&str>>();
    let argv = args().collect::<Vec<String>>();
    let mut cfg = Config::default();
    let argv: Vec<&str> = argv.iter().map(|s| s.as_str()).collect();
    
    if argv.len() <= 1 { return cfg }
    
    let args = group_args(argv);
    
    for p in  args {
        match p {
            ParamType::Alone(_) => {},
            ParamType::SingleArg(p, arg) => match p {
                "--ip" | "-i" => if is_ip_valid(arg) {
                    cfg.set_ip(arg) 
                }
                "--port" | "-p" => {
                    let parsed = arg.parse::<u16>();
                    match parsed {
                        Ok(port) => cfg.set_port(port),
                        Err(_) => {}
                    }
                }
                "--max-players" | "-m" => {
                    let parsed = arg.parse::<u16>();
                    match parsed {
                        Ok(m) => cfg.set_max_players(m),
                        Err(_) => {}
                    }
                }
                _ => {}
            }
            ParamType::DoubleArg(p, arg1, arg2) => match p {
                "--world-size" | "-w" => {
                    let parsed1 = arg1.parse::<u8>();
                    let parsed2 = arg2.parse::<u8>();

                    if parsed1.is_ok() && parsed2.is_ok() {
                        cfg.set_size_x(parsed1.unwrap());
                        cfg.set_size_y(parsed2.unwrap());
                    }
                }
                _ => {}
            }
        }
    }
    cfg
}

fn group_args(argv: Vec<&str>) -> Vec<ParamType<'_>> {
    let mut final_vec: Vec<Vec<&str>> = Vec::with_capacity(2);
    let mut tmp_vec: Vec<&str> = Vec::with_capacity(2);
    let mut next_flag: u8 = 0;
    
    for i in 1..argv.len() {
        if next_flag == 0 {
            match argv[i] {
                p if LONE_PARAMS.contains(&p) => final_vec.push(vec![p]),
                p if SINGLE_ARG_PARAMS.contains(&p) => {
                    next_flag = 1;
                    tmp_vec.push(p); // Pushing 🅿️
                }
                p if DOUBLE_ARG_PARAMS.contains(&p) => {
                    next_flag = 2;
                    tmp_vec.push(p);
                }
                _ => {}
            }
        } else {
            tmp_vec.push(argv[i]);
            next_flag -= 1;
        }
        
        if tmp_vec.len() > 0 && next_flag == 0 {
            final_vec.push(tmp_vec.clone());
            tmp_vec = Vec::with_capacity(2);
        }
    }
    
    grouped_args_clean(final_vec)
}

fn grouped_args_clean(args: Vec<Vec<&str>>) -> Vec<ParamType<'_>> {
    let mut out = Vec::with_capacity(2);
    for v in args {
        match v.len() {
            1 => out.push(ParamType::Alone(v[0])),
            2 => out.push(ParamType::SingleArg(v[0], v[1])),
            3 => out.push(ParamType::DoubleArg(v[0], v[1], v[2])),
            _ => {}
        }
    }
    out
}

#[derive(Debug)]
enum ParamType<'a> {
    Alone(&'a str),
    SingleArg(&'a str, &'a str),
    DoubleArg(&'a str, &'a str, &'a str),
}