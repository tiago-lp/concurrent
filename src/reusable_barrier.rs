use std_semaphore::Semaphore;
use std::sync::{Arc, RwLock};
use std::thread;

pub fn reusable_barrier() {
    const NUM_THREADS_ALLOWED: isize = 2;
    let barrier = Arc::new(Semaphore::new(0));
    let turnstile = Arc::new(Semaphore::new(1));
    let mutex = Arc::new(Semaphore::new(1));
    let counter = Arc::new(RwLock::new(0));
    let mut handles = vec![];
    
    for _i in 0..NUM_THREADS_ALLOWED {
        let t_barrier = barrier.clone();
        let _t_mutex = mutex.clone();
        let t_counter = counter.clone();
        let t_turnstile = turnstile.clone();
        let handle = thread::spawn(move || {
            for _j in 0..2 {
                let mut num = t_counter.write().unwrap();
                *num += 1;
                if *num == NUM_THREADS_ALLOWED {
                    t_turnstile.acquire();
                    t_barrier.release();
                }
                drop(num);
                t_barrier.acquire();
                t_barrier.release();
                    
                // critical section
    
                let mut num = t_counter.write().unwrap();
                *num -= 1;
                if *num == 0 {
                    t_barrier.acquire();
                    t_turnstile.release();
                }
                drop(num);
                t_turnstile.acquire();
                t_turnstile.release()
            }
    
    
        });
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
    }
}