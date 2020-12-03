use std_semaphore::Semaphore;
use std::sync::{Arc, Mutex};
use std::thread;

pub fn mutex() {

    // By default rust implements Mutex in std lib
    let _mutex = Mutex::new(0);

    // Add semaphores to the following example to enforce mutual exclusion to the shared variable count.
    // Thread A
    // count = count + 1
    // Thread B
    // count = count + 1

    let mut count = 0;
    let a = Arc::new(Semaphore::new(0));
    let b = Arc::new(Semaphore::new(0));
    let a_clone = a.clone();
    let b_clone = b.clone();


    thread::spawn(move || {
        count += 1;
        b_clone.release();
        let _g = a_clone.access();
    });

    {
        count += 1;
        a.release();
        let _g = b.access();
    }

    println!("{}", count);
}