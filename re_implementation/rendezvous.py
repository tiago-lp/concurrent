from threading import Semaphore, Thread
import logger


log = logger.get_logger("Rendezvous")


def _print(statement):
    log.info(f"Execução arbitrária {statement}")


class Counter():
    """
    Classe que representa os semaforos
    do problema Rendezvous, do livro
    The Little Book of Semaphores, cap. 3.3

    ...

    Attributes
    ----------
    a_arrived : Semaphore
        Semaforo para garantir a ordem de execução
        dos statements da primeira thread dentre
        duas threads arbitrárias.

    b_arrived : Semaphore
        Semaforo para garantir a ordem de execução
        dos statements da segunda thread dentre
        duas threads arbitrárias.
    """
    def __init__(self):
        self.a_arrived = Semaphore(0)
        self.b_arrived = Semaphore(0)


class A(Thread):
    """
    Classe que representa a thread A
    do problema Rendezvous, do livro
    The Little Book of Semaphores, cap. 3.3

    ...

    Attributes
    ----------
    name : str
        Nome da classe.

    c : Counter
        Contador com referências dos semáforos para
        controle da ordem de execução das threads
        do rendezvous.
    """
    def __init__(self, counter):
        Thread.__init__(self)
        self.name = "A"
        self.c = counter

    def run(self):
        """
        Execução da thread A baseada na
        solução dada no cap. 3.3 do livro
        The Little Book of Semaphores.
        """
        _print(f"{self.name}{1}")
        self.c.a_arrived.release()
        self.c.b_arrived.acquire()
        _print(f"{self.name}{2}")


class B(Thread):
    """
    Classe que representa a thread B
    do problema Rendezvous, do livro
    The Little Book of Semaphores, cap. 3.3

    ...

    Attributes
    ----------
    name : str
        Nome da classe.

    c : Counter
        Contador com referências dos semáforos para
        controle da ordem de execução das threads
        do rendezvous.
    """
    def __init__(self, counter):
        Thread.__init__(self)
        self.name = "B"
        self.c = counter

    def run(self):
        """
        Execução da thread A baseada na
        solução dada no cap. 3.3 do livro
        The Little Book of Semaphores.
        """
        _print(f"{self.name}{1}")
        self.c.b_arrived.release()
        self.c.a_arrived.acquire()
        _print(f"{self.name}{2}")


if __name__ == "__main__":

    counter = Counter()
    for thread in [A(counter), B(counter)]:
        thread.start()
