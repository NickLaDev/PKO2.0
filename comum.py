from datetime import datetime

HOST = '0.0.0.0'
PORTA = 5000

# 10s pra nao esperar 1 minuto a cada teste. NA ENTREGA VOLTA PRA 60.
INTERVALO_SORTEIO = 10

INICIO_PADRAO = 0
FIM_PADRAO = 100
QTD_PADRAO = 5


def agora():
    return datetime.now().strftime('%H:%M:%S')


def enviar_linha(sock, texto):
    sock.sendall((texto + '\n').encode('utf-8'))


def ler_linhas(sock):
    # o makefile junta os pedacos que o TCP entrega picado
    for linha in sock.makefile('r', encoding='utf-8'):
        yield linha.strip()
