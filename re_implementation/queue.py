import logger
from threading import Semaphore, Thread
from time import sleep
import random

"""
Aqui iremos exemplificar baseado no livro The Little Book of Semaphores
cap. 3.8. Colocando as abstrações para uma pista de Dança e para Pessoas no baile
querendo dançar. Só é possível entrar em pares para dançar. Depois essas pessoas saem
da pista e entra as duas seguintes, e assim por diante.
"""

log = logger.get_logger("Queue")


def pista_livre():
    log.info("A pista está livre para dançar!...")


def esvaziar_pista():
    log.info("As pessoas estão saindo da pista...")


def dancar():
    log.info("A música está tocando! Pessoas estão dançando")


def entrar_na_pista(id):
    log.info(f"Pessoa {id} está entrando na pista...")


def parar():
    log.info("A música parou.")


def sair_da_pista(id):
    log.info(f"Pessoa {id} está saindo da pista...")


def finalizar():
    log.info("Nenhum pessoa esperando para dançar. Fechando boate.")
    exit()


def falta_dancarinos(num, capacidade):
    log.info(f"Não é possível tocar musica. Tem apenas {num} querendo dançar. Só é possível dançar em pares.")
    exit()


class Counter():
    def __init__(self, num_pessoas):
        """
        Classe com atributos baseado na solucao dada no capitulo 5.8
        do livro The Little Book of Semaphores. A classe é usada como
        argumento de construção das classes Carro e Pessoa.
        """
        self.max = 2
        self.num_pessoas = num_pessoas
        self.ja_dancaram = 0
        self.dancando = 0
        self.not_dancando = 0
        self.mutex = Semaphore(1)
        self.mutex2 = Semaphore(1)
        self.queu_to_dance = Semaphore(0)
        self.queue_to_leave = Semaphore(0)
        self.todos_dancando = Semaphore(0)
        self.todos_fora_da_pista = Semaphore(0)


class Pista(Thread):
    def __init__(self, counter):
        """
        Classe pista inicializa herdando da classe Thread
        e a inicializa.
        Params
        ------
        counter : Counter
            Referencia para a contagem de dançarinos, capacidade
            da pista de dança e semaforos utilizados.
        """
        Thread.__init__(self)
        self.counter = counter
        self.start()

    def sobrou_pessoas(self):
        """Verifica se sobrou pessoas esperando para entrar
        que nao contempla a lotacao do da pista.
        """
        return self.counter.ja_dancaram + self.counter.max > self.counter.num_pessoas

    def nao_tem_passageiros(self):
        """Verifica se nao tem mais nenhum passageiro esperando para embarcar."""
        return self.counter.ja_dancaram == self.counter.num_pessoas

    def sinaliza_passageiros(self, sem):
        """Isto eh necessario em python
        notei que o release do semaforo nativo nao aceita argumentos.
        Eu poderia criar o meu proprio semaforo,
        mas para reusar a implementacao nativa percorri a quantidade
        de vezes que eh preciso sinalizar, que seria o C definido no problema
        (capacidade do carro)
        params
        -------
        sem : Semaphore
            Referencia do semaforo que desejo sinalizar
        """
        for i in range(self.counter.max):
            sem.release()
            sleep(random.randrange(0,2))

    def run(self):
        while True:
            pista_livre()

            if self.nao_tem_passageiros():
                finalizar()

            if self.sobrou_pessoas():
                sobraram = self.counter.num_pessoas - self.counter.ja_dancaram
                falta_dancarinos(sobraram, self.counter.max)


            self.sinaliza_passageiros(self.counter.queu_to_dance)
                
            self.counter.todos_dancando.acquire()
            dancar()
            sleep(random.randrange(0,2))
            parar()
            sleep(random.randrange(0,2))
            if self.counter.dancando == 0:
                esvaziar_pista()
                self.sinaliza_passageiros(self.counter.queue_to_leave)
                self.counter.todos_fora_da_pista.acquire()


class Pessoa(Thread):

    def __init__(self, counter, id):
        """
        Classe pessoa inicializa herdando da classe Thread
        e a inicializa.
        Params
        ------
        counter : Counter
            Referencia para a contagem de pessoas, capacidade
            da pista de dança e semaforos utilizados.
        id : str, int
            Identificador da pessoa para mostrar nos logs
        """
        Thread.__init__(self)
        self.id = id
        self.counter = counter
        self.start()

    def run(self):
        self.counter.queu_to_dance.acquire()
        entrar_na_pista(self.id)
        self.counter.mutex.acquire()
        self.counter.dancando += 1
        if self.counter.dancando == self.counter.max:
            self.counter.todos_dancando.release()
            self.counter.dancando = 0

        self.counter.mutex.release()
        self.counter.queue_to_leave.acquire()
        sair_da_pista(self.id)
        self.counter.mutex2.acquire()
        self.counter.not_dancando += 1
        self.counter.ja_dancaram += 1
        if self.counter.not_dancando == self.counter.max:
            self.counter.todos_fora_da_pista.release()
            self.counter.not_dancando = 0

        self.counter.mutex2.release()


if __name__ == "__main__":
    pessoas = int(input("Digite a quantidade de pessoas: "))
    counter = Counter(pessoas)
    _pista = Pista(counter)
    for num in range(pessoas):
        _passageiro = Pessoa(counter, num)