mod rendezvous;
mod multiplex;
mod barrier;
mod reusable_barrier;

fn main() {
    rendezvous::rendezvous();
    multiplex::multiplex();
    barrier::barrier();
    reusable_barrier::reusable_barrier();
    println!("Hello, world!");
}
