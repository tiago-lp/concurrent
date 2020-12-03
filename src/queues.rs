use std_semaphore::Semaphore;
use std::sync::{Arc};
use std::thread;

pub fn queue() {

    let leader_queue = Arc::new(Semaphore::new(0));
    let follower_queue = Arc::new(Semaphore::new(0));
    let l_clone = leader_queue.clone();
    let f_clone = follower_queue.clone();

    thread::spawn(move || {
        follower_queue.release();
        let _l = leader_queue.access();
        println!("dance");
    });

    {        
        l_clone.release();
        let _f = f_clone.access();
        println!("dance");
    }
}