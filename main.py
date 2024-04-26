import serial
import os
from datetime import datetime
import configparser

# Defina a porta serial e a velocidade de comunicação
##porta_serial = 'COM1'
velocidade = 9600
diretorio_arquivo = "C:/TESTE/"

# Ler opções de tamanho do arquivo e do buffer do arquivo de configuração
config = configparser.ConfigParser()
config.read('config.ini')  # Ler o arquivo config.ini

porta_serial = config['SocketConn']['Port']
limite_tamanho_arquivo = int(config['FileOptions']['MaxSize'])
limite_tamanho_buffer = int(config['BufferOptions']['MaxSize'])
# Função para criar um nome de arquivo com "TARIFADOR" e data e hora
def criar_nome_arquivo():
    data_hora_atual = datetime.now()
    nome_arquivo = f"TARIFADOR_{data_hora_atual.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    return os.path.join(diretorio_arquivo, nome_arquivo)

# Inicialize a comunicação serial
conexao_serial = serial.Serial(porta_serial, velocidade)
conexao_serial.flushInput()

if conexao_serial.is_open:
    print(f"Conexão estabelecida com sucesso na porta {porta_serial}")
else:
    print(f"Não foi possível estabelecer conexão na porta {porta_serial}")
    exit()

arquivo_atual = None
tamanho_atual = 0

def verificar_tamanho_arquivo():
    if arquivo_atual:
        arquivo_atual.seek(0, os.SEEK_END)
        return arquivo_atual.tell()
    return 0

try:
    while conexao_serial.is_open:
        dados = conexao_serial.read(limite_tamanho_buffer)  # Usar limite_tamanho_buffer
        if dados:
            linha = dados.decode('utf-8').strip()
            print("Dados recebidos:", linha)

            if arquivo_atual == None: #or tamanho_atual >= limite_tamanho_arquivo:
                nome_arquivo_atual = criar_nome_arquivo()
                arquivo_atual = open(nome_arquivo_atual, 'a')
                #tamanho_atual = verificar_tamanho_arquivo()

            if arquivo_atual != None:

                if tamanho_atual >= limite_tamanho_arquivo:
                    arquivo_atual.close()
                    nome_arquivo_atual = criar_nome_arquivo()
                    arquivo_atual = open(nome_arquivo_atual, 'a')
                    #tamanho_atual = verificar_tamanho_arquivo()

                arquivo_atual.write(linha + "\n")
                tamanho_atual = verificar_tamanho_arquivo()

finally:
    if arquivo_atual:
        arquivo_atual.close()
    conexao_serial.close()
