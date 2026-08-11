import os
import socket
import sys
import threading

from comum import PORTA, enviar_linha, ler_linhas

# o HOST do comum e 0.0.0.0, que so vale pro bind do servidor. pra
# conectar precisa de um endereco de verdade
HOST_PADRAO = '127.0.0.1'


def avisa_e_sai():
    print('conexao com o servidor encerrada, saindo')
    # sys.exit aqui so mataria a thread, e a principal ficaria travada
    # pra sempre esperando o input()
    os._exit(0)


def recebe_do_servidor(sock):
    try:
        for linha in ler_linhas(sock):
            print(linha)
    except OSError:
        pass
    avisa_e_sai()


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST_PADRAO
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else PORTA

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, porta))
    print(f'conectado em {host}:{porta}')

    threading.Thread(target=recebe_do_servidor, args=(sock,), daemon=True).start()

    try:
        while True:
            enviar_linha(sock, input())
    except OSError:
        avisa_e_sai()


if __name__ == '__main__':
    main()
