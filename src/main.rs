mod rendezvous;
mod multiplex;
mod barrier;
mod reusable_barrier;
mod mutex;

fn main() {
    rendezvous::rendezvous();
    multiplex::multiplex();
    barrier::barrier();
    reusable_barrier::reusable_barrier();
    mutex::mutex();
    println!("Hello, world!");
}
