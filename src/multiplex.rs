use std_semaphore::Semaphore;
use std::sync::{Arc};
use std::thread;

pub fn multiplex() {
    const THREADS_ALLOWED: isize = 5;

    let multiplex = Arc::new(Semaphore::new(THREADS_ALLOWED));
    let mut handles = vec![];
    
    (0..10).for_each(|_| {
        let t_multiplex = multiplex.clone();
        let handle = thread::spawn(move || {
            let _g = t_multiplex.access();
            // critical section
        });
        handles.push(handle);
    });

    for handle in handles {
        handle.join().unwrap();
    }
}