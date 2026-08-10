import threading

from comum import INICIO_PADRAO, FIM_PADRAO, QTD_PADRAO


class EstadoLoteria:
    def __init__(self):
        self.lock = threading.Lock()
        self.inicio = INICIO_PADRAO
        self.fim = FIM_PADRAO
        self.qtd = QTD_PADRAO
        self.apostas = {}

    def set_inicio(self, valor):
        with self.lock:
            self.inicio = valor

    def set_fim(self, valor):
        with self.lock:
            self.fim = valor

    def set_qtd(self, valor):
        with self.lock:
            self.qtd = valor

    def get_config(self):
        # os tres juntos numa leitura so, senao o sorteio pega config
        # metade velha metade nova se alguem configurar no meio
        with self.lock:
            return self.inicio, self.fim, self.qtd

    def adicionar_cliente(self, cliente):
        with self.lock:
            self.apostas[cliente] = []

    def remover_cliente(self, cliente):
        with self.lock:
            self.apostas.pop(cliente, None)

    def registrar_aposta(self, cliente, numeros):
        with self.lock:
            self.apostas.setdefault(cliente, []).append(numeros)

    def pegar_apostas_e_limpar(self):
        # ler e zerar tem que ser a MESMA operacao dentro do lock. se
        # soltar o lock no meio, aposta que chegar nesse intervalo some
        # sem ser conferida. as chaves ficam pra saber quem esta conectado
        with self.lock:
            apostas = self.apostas
            self.apostas = {cliente: [] for cliente in apostas}
            return apostas
