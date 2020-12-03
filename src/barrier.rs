use std_semaphore::Semaphore;
use std::sync::{Arc, RwLock};
use std::thread;

pub fn barrier() {
    const THREADS_ALLOWED: isize = 5;

    let barrier = Arc::new(Semaphore::new(0));
    let mutex = Arc::new(Semaphore::new(1));
    let counter = Arc::new(RwLock::new(0));
    let mut handles = vec![];

    (0..THREADS_ALLOWED).for_each(|_| {
        let t_barrier = barrier.clone();
        let _t_mutex = mutex.clone();
        let t_counter = counter.clone();
        let handle = thread::spawn(move || {
            let mut num = t_counter.write().unwrap();
            *num += 1;
            if *num == THREADS_ALLOWED {
                t_barrier.release();
            }
            drop(num);
            let _g = t_barrier.access();
            // critical section
        });
        handles.push(handle);
    });

    for handle in handles {
        handle.join().unwrap();
    }
}