/*
 * Name: monte-carlo-rust
 * Author: Josiah Lawrence
 * Project: CSCI 440 Final
 * Create Date: 2026/04/15
 * Modify Date: 2026/04/26
 * Description:
 * 	This is a threaded implementation of a
 *  matrix multiplication program.
 *
 */

use rand::Rng;
use std::env;
use std::thread::{self, JoinHandle};

const NUM_THREADS: usize = 10;
const MINARGS: usize = 2;
const USAGE: &str = "<number of samples>";

fn main() {
    /* Collect args */
    let args: Vec<String> = env::args().collect();
    if args.len() < MINARGS {
        panic!(
            "Not enough arguments: {}\nUsage: {} {}",
            args.len(),
            args[0],
            USAGE
        );
    }
    let total_samples: usize = args[1]
        .parse()
        .expect("Number of samples must be a positive integer");

    /* Spawn Threads */
    let mut handles: Vec<JoinHandle<u64>> = Vec::new();
    let start = std::time::Instant::now(); // Start timer

    for t in 0..NUM_THREADS {
        let chunk = total_samples / NUM_THREADS;
        let n_samples = {
            if t == NUM_THREADS - 1 {
                total_samples - t * chunk
            } else {
                chunk
            }
        };

        let handle = thread::spawn(move || {
            let mut hits: u64 = 0;
            let mut rng = rand::thread_rng();

            for _ in 0..n_samples {
                let x: f64 = rng.r#gen::<f64>(); 
                let y: f64 = rng.r#gen::<f64>(); 
                if x * x + y * y <= 1.0 {
                    hits += 1;
                }
            }
            hits
        });
        handles.push(handle);
    }
    
    /* Collect results */
    let total_hits: u64 = handles.into_iter().map(|h| h.join().unwrap()).sum();

    /* Measure elapsed time and print */
    let elapsed = start.elapsed();
    println!("{}", elapsed.as_micros());

    /* Calculate and print estimation of pi */
    let pi = 4.0 * total_hits as f64 / total_samples as f64;
    eprintln!("pi = {}", pi);
}
