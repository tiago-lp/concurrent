use std_semaphore::Semaphore;
use std::sync::{Arc};
use std::thread;

pub fn multiplex() {
    const NUM_THREADS_ALLOWED: isize = 5;
    let multiplex = Arc::new(Semaphore::new(NUM_THREADS_ALLOWED));
    let mut handles = vec![];
    
    for i in 0..10 {
        let t_multiplex = multiplex.clone();
        let handle = thread::spawn(move || {
            let _g = t_multiplex.access();
            // critical section
        });
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
    }
}