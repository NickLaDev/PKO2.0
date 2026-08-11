import socket
import threading

import sorteio
from comum import HOST, PORTA, agora, enviar_linha, ler_linhas
from estado import EstadoLoteria


def trata_cliente(conexao, endereco, estado):
    quem = f'{endereco[0]}:{endereco[1]}'
    print(f'[{agora()}] conectou: {quem}')
    enviar_linha(conexao, f'{agora()}: CONECTADO!!')
    estado.adicionar_cliente(conexao)
    try:
        for linha in ler_linhas(conexao):
            enviar_linha(conexao, linha)
    except OSError:
        pass
    finally:
        estado.remover_cliente(conexao)
        conexao.close()
        print(f'[{agora()}] desconectou: {quem}')


def main():
    estado = EstadoLoteria()
    threading.Thread(target=sorteio.loop_sorteio, args=(estado,), daemon=True).start()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sem isso a porta fica presa em TIME_WAIT e reiniciar da "Address already in use"
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f'[{agora()}] servidor ouvindo em {HOST}:{PORTA}')

    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=trata_cliente, args=(conexao, endereco, estado), daemon=True).start()


if __name__ == '__main__':
    main()
