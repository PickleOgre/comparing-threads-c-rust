/*
 * Name: matrix-mult-rust
 * Author: Josiah Lawrence
 * Project: CSCI 440 Final
 * Create Date: 2026/04/15
 * Modify Date: 2026/04/26
 * Description:
 * 	This is a threaded implementation of a
 *  matrix multiplication program.
 *
 */

use std::env;
use std::sync::Arc;
use std::thread::{self, JoinHandle};

const NUM_THREADS: usize = 10;
const MINARGS: usize = 2;
const USAGE: &str = "<matrixSize>";

fn main() {
    /* Collect args */
    let args: Vec<String> = env::args().collect();
    if args.len() < MINARGS {
        panic!("Not enough arguments: {}\nUsage: {} {}", args.len(), args[0], USAGE);
    }
    let n: usize = args[1].parse().expect("Matrix size must be a positive integer");

    /* Create matrices */
    let mut a = vec![0.0f64; n * n];
    let mut b = vec![0.0f64; n * n];

    for i in 0..n {
        for j in 0..n {
            a[i * n + j] = (i + j) as f64;
            b[i * n + j] = (i * j) as f64;
        }
    }

    let a = Arc::new(a);
    let b = Arc::new(b);

    /* Spawn Threads */
    let mut handles: Vec<JoinHandle<Vec<f64>>> = Vec::new();

    let start = std::time::Instant::now(); // Start timer

    for t in 0..NUM_THREADS {
        let a = Arc::clone(&a);
        let b = Arc::clone(&b);
        let chunk = n / NUM_THREADS;
        let start_row: usize = t * chunk;
        let end_row: usize = {
            if t == NUM_THREADS - 1 { n }
            else { (t + 1) * chunk }
        };

        let handle = thread::spawn(move || {
            let mut rows = vec![0.0f64; (end_row - start_row) * n];
            for row in start_row..end_row {
                for j in 0..n {
                    let mut sum: f64 = 0.0;
                    for k in 0..n {
                        sum += a[row * n + k] * b[k * n + j];
                    }
                    rows[(row - start_row) * n + j] = sum;
                }
            }
            rows
        });
        handles.push(handle);
    }

    /* Collect results */
    let mut c = vec![0.0f64; n * n];
    for (t, handle) in handles.into_iter().enumerate() {
        let chunk = n / NUM_THREADS;
        let start_idx = t * chunk * n;
        let rows = handle.join().unwrap();
        c[start_idx..(start_idx + rows.len())].copy_from_slice(&rows);
    }

    /* Measure elapsed time and print */
    let elapsed = start.elapsed();
    println!("{}", elapsed.as_micros());

}
