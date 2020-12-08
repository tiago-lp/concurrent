from threading import Semaphore, Thread
import logger


log = logger.get_logger("Exclusão mútua")


def _print(name):
    log.info(f"Seção crítica onde a thread {name} modifica a variável 'count'")


mutex = Semaphore(1)
count = 0


class T(Thread):
    """
    Classe que representa uma thread
    do problema de exclusão mútua, do livro
    The Little Book of Semaphores, cap. 3.4

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
        solução dada no cap. 3.4 do livro
        The Little Book of Semaphores.
        """
        mutex.acquire()
        _print(self.name)
        global count
        count += 1
        log.info(f"Valor atual de count: {count}")
        mutex.release()



if __name__ == "__main__":

    log.info("Exclusão mútua controla que as threads possam acessar uma variavel compartilhada")
    log.info("É possível replicar o exemplo para N threads. Exemplo:")
    log.info("O primeiro exemplo será com threads A e B como no livro.")
    log.info("Em seguida farei com 5 threads de 0 a 4. Os logs poderão sair embaraçados")
    log.info("entre a execução do exemplo 1 e 2, por se tratar de algo concorrente")
    log.info(f"Valor atual de count: {count}")
    for thread in [T("A"), T("B"),]:
        thread.start()


    N = 5

    for i in range(N):
        thread = T(str(i))
        thread.start()
