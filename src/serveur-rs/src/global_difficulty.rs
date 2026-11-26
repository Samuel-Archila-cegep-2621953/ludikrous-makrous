use std::time::Instant;

pub fn difficulty_fn(level: u8) -> fn(Instant) -> f32 {
    match level {
        0 => |_| 10.0,
        1 => |t| t.elapsed().as_secs() as f32 * 0.19,
        2 => |t| t.elapsed().as_secs() as f32 * 1.0,
        3 => |t| (t.elapsed().as_secs() as f32).exp2() * 0.002,
        4 => |t| 1.0022_f32.powf(t.elapsed().as_secs() as f32) * 1.25,
        _ => |t| t.elapsed().as_secs() as f32 * 1.55,
    }
}
