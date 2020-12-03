use std_semaphore::Semaphore;
use std::sync::{Arc};
use std::thread;


pub fn rendezvous() {

    let a_arrived = Arc::new(Semaphore::new(0));
    let b_arrived = Arc::new(Semaphore::new(0));
    let a_clone = a_arrived.clone();
    let b_clone = b_arrived.clone();

    thread::spawn(move || {
        println!("statement b1");
        b_clone.release();
        let _g = a_clone.access();
        println!("statement b2");
    });

    {
        println!("statement a1");
        a_arrived.release();
        let _g = b_arrived.access();
        println!("statement a2");
    }
}

