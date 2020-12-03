use std_semaphore::Semaphore;
use std::sync::{Arc};
use std::thread;


pub fn rendezvous() {

    let a_arrived = Arc::new(Semaphore::new(0));
    let b_arrived = Arc::new(Semaphore::new(0));

    thread::spawn(move || {
        println!("statement b1");
        b_arrived.release();
        let _g = a_arrived.access();
        println!("statement b2");
    });

}

