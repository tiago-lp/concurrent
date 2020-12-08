"""
O Multiplex pode ser testado
apenas mudando o número de inicialização
do semáforo na linha 12 de mutex.py

Possui comportamento semelhante em controlar
acesso a variáveis compartilhadas entre threads.
Com a diferença de que inicia o semáforo com o valor N,
que é o número máximo de threads permitidas.
"""

from threading import Semaphore, Thread
import logger


log = logger.get_logger("Multiplex")


class Multiplex(Semaphore):

    def __init__(self, numero_threads):
        Semaphore.__init__(self, numero_threads)


multiplex = Multiplex(4)
count = 0


class T(Thread):
    """
    Classe que representa uma thread
    do problema de exclusão mútua, do livro
    The Little Book of Semaphores, cap. 3.5

    ...

    Attributes
    ----------
    name : str
        Nome da classe.

    """
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        """
        Execução da thread A baseada na
        solução dada no cap. 3.5 do livro
        The Little Book of Semaphores.
        """
        log.info(f"Thread {self.name}")
        multiplex.acquire()
        global count
        count += 1
        log.info(f"Valor atual de count: {count}")
        multiplex.release()



if __name__ == "__main__":

    N = 8

    for i in range(N):
        thread = T(str(i))
        thread.start()
