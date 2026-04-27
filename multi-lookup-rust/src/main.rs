/*
 * Name: multi-lookup
 * Author: Josiah Lawrence
 * Project: CSCI 3753 DNS Resolver in Rust Threaded
 * Create Date: 2026/04/15
 * Description:
 * 	This is a threaded implementation of a
 *  bulk DNS lookup program.
 *
 */

use crossbeam_channel::bounded;
use dns_lookup::lookup_host;
use std::env;
use std::fs::File;
use std::io::{prelude::*, BufReader, BufWriter, Write};
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

const MINARGS: usize = 3;
const USAGE: &str = "<inputFilePath> <outputFilePath>";
const QUEUE_SIZE: usize = 10;
const NUM_RESOLVER_THREADS: usize = 10;
const DEBUG: bool = false;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < MINARGS {
        panic!(
            "Not enough arguments: {}\n
            Usage:\n
            {} {}",
            args.len(),
            "cargo run ",
            USAGE
        )
    }

    let outfile_str = args[args.len() - 1].clone();
    let outfile_path = Path::new(&outfile_str);
    let display = outfile_path.display();

    // Open output file
    let ofile = match File::create(outfile_path) {
        Err(why) => panic!("couldn't create {}: {}", display, why),
        Ok(file) => {
            if DEBUG {
                println!("Outfile created: {}", outfile_str);
            }
            file
        }
    };

    let output: Arc<Mutex<BufWriter<File>>> = Arc::new(Mutex::new(BufWriter::new(ofile)));

    let (sender, receiver) = bounded::<String>(QUEUE_SIZE);

    // Spawn resolver threads
    let mut resolver_handles: Vec<JoinHandle<()>> = Vec::new();

    for i in 0..NUM_RESOLVER_THREADS {
        let receiver = receiver.clone();
        let output = Arc::clone(&output);
        let handle = thread::spawn(move || {
            if DEBUG {
                println!("Hello from resolver thread #{}!", i);
            }
            while let Ok(hostname) = receiver.recv() {
                let version = lookup_host(&hostname);
                let ip_str = match version {
                    Err(why) => {
                        eprintln!("dnslookup error for {}: {}", hostname, why);
                        format!("{},", hostname)
                    }
                    Ok(mut v) => match v.next() {
                        Some(addr) => format!("{},{}", hostname, addr),
                        None => {
                            eprintln!("dnslookup error: no results for {}", hostname);
                            continue;
                        }
                    },
                };
                let mut out = output.lock().unwrap();
                writeln!(out, "{}", ip_str).unwrap();
            }
        });
        resolver_handles.push(handle);
    }

    // Spawn requester threads
    let mut requester_handles: Vec<JoinHandle<()>> = Vec::new();
    for i in 1..(args.len() - 1) {
        let sender = sender.clone();
        let infile_str = args[i].clone();
        let handle = thread::spawn(move || {
            if DEBUG {
                println!("Hello from requester thread #{}!", i);
            }
            // Open input file
            let infile_path = Path::new(&infile_str);
            let display = infile_path.display();
            let ifile = match File::open(infile_path) {
                Err(why) => {
                    eprintln!("Couldn't open {}: {}", display, why);
                    return;
                }
                Ok(file) => {
                    if DEBUG {
                        println!("Infile opened: {}", infile_str);
                    };
                    file
                }
            };
            let reader = BufReader::new(ifile);

            for line in reader.lines() {
                let mut hostname = match line {
                    Err(why) => panic!("Error reading line: {}", why),
                    Ok(l) => l,
                };
                hostname = hostname.trim().to_string();
                if !hostname.is_empty() {
                    sender.send(hostname).unwrap();
                };
            }
        });
        requester_handles.push(handle);
    }

    // Join all requester threads
    for handle in requester_handles {
        handle.join().unwrap();
    }

    // Close the original channel
    drop(sender);

    // Join all resolver threads
    for handle in resolver_handles {
        handle.join().unwrap();
    }

    output.lock().unwrap().flush().unwrap();
}
