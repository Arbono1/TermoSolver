import ast
import base64
import calendar
import os
import struct
import sys
from datetime import datetime, timezone

# Correspondências com o JS original do jogo:
# "JB", "ZB" e "getUint16" presente na função "decodificar_indices_do_array"
# "HB" presente em dueto_indices_base64
# "XB" presente em quarteto_indices_base64
# "WB" renomeada para "dueto_indices"
# "$B" renomeada para "quarteto_indices"
# "Pf" renomeada para "respostas_palavras"
# "bc" renomeada para "modo"
# "Eh()" renomeada para "indice_do_dia_a_partir_de_string"
# "bc()" e "ey()" presentes na função "solucoes_diarias"

# Função dinâmica para carregar os arquivos de dados com o script puro e no executável
def carregar_arquivo(nome_arquivo):
    try:
        base_path = sys._MEIPASS  # se estiver no executável
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # se estiver no script em Python

    caminho = os.path.join(base_path, 'dados', nome_arquivo)

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado em '{caminho}'")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Erro: Problema de codificação no arquivo '{nome_arquivo}'")
        sys.exit(1)

# Strings codificadas em base64
dueto_indices_base64 = carregar_arquivo('Dueto índices.txt')  # string "HB"
quarteto_indices_base64 = carregar_arquivo('Quarteto índices.txt')  # string "XB"

# Função para decodificar um array de índices, codificado em base64
def decodificar_indices_do_array(string_base64):
    binario = base64.b64decode(string_base64)
    return list(struct.unpack('<' + 'H' * (len(binario) // 2), binario))

# Decodificar para obter os arrays de índices
dueto_indices = decodificar_indices_do_array(dueto_indices_base64)  # comportamento de "JB"
quarteto_indices = decodificar_indices_do_array(quarteto_indices_base64)  # comportamento de "ZB"

# Lista completa de palavras
respostas_palavras = ast.literal_eval(carregar_arquivo('Palavras.txt'))  # string Pf

# Converter uma data em string para o número de dias desde 2 de janeiro de 2022
def indice_do_dia_a_partir_de_string(data_str):
    data_usuario = datetime.strptime(data_str, "%d/%m/%Y").replace(tzinfo=timezone.utc)
    data_base = datetime(2022, 1, 2, tzinfo=timezone.utc)
    return (data_usuario - data_base).days

# Função para consultar respostas
def solucoes_diarias(respostas_palavras, dueto_indices, quarteto_indices, dia):
    respostas = {}

    # Termo
    modo1 = 1  # função "bc()"
    r1 = (modo1 * dia) % len(respostas_palavras)
    respostas[1] = [respostas_palavras[r1]]

    # Dueto
    modo2 = 2  # função "bc()"
    dia2 = dia - 51 # função "ey()"
    r2 = (modo2 * dia2) % len(dueto_indices)
    i2 = dueto_indices[r2:r2 + modo2]
    respostas[2] = [respostas_palavras[idx] for idx in i2]

    # Quarteto
    modo4 = 4  # função "bc()"
    dia4 = dia - 51  # função "ey()"
    r4 = (modo4 * dia4) % len(quarteto_indices)
    i4 = quarteto_indices[r4:r4 + modo4]
    respostas[4] = [respostas_palavras[idx] for idx in i4]

    return respostas

def validar_data(data_str):

    # Verificação inicial do formato
    if not isinstance(data_str, str) or data_str.count('/') != 2:
        raise ValueError("Formato inválido. Utilize DD/MM/AAAA.")
    try:
        dia, mes, ano = map(int, data_str.split('/'))
    except ValueError:
        raise ValueError("Formato inválido. Utilize apenas números e barras (DD/MM/AAAA).")

    # Verificação de erros comuns (dia, mês e ano fora dos limites)
    if dia < 1 or dia > 31:
        raise ValueError("Dia inválido. O dia deve estar entre 1 e 31.")

    if mes < 1 or mes > 12:
        raise ValueError("Mês inválido. O mês deve estar entre 1 e 12.")

    if ano < 1:
        raise ValueError("Ano inválido. O ano deve estar entre 1 e 9999.")

    if ano > 9999:
        raise ValueError(
            "Data fora do limite máximo de 31/12/9999. (Esse programa ou o Termo realmente sobreviveram a todo esse tempo?)")

    # Verificação para falsos fevereiros bissextos
    if mes == 2 and dia == 29:
        if not calendar.isleap(ano):
            raise ValueError("Data inválida: 29/02 só é válida em anos bissextos.")

    # Verificação de dias impossíveis (como 31/04 e 30/02)
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError as erro:
        if "day is out of range" in str(erro):
            raise ValueError("Dia inválido para o mês especificado.")
        raise ValueError("Data inválida. Verifique os valores digitados.")

    return dia, mes, ano

# Solicitar datas do usuário
primeira_vez = True

while True:
    if primeira_vez:
        prompt = "Digite uma data (formato DD/MM/AAAA) ou 'sair' para encerrar: "
        primeira_vez = False
    else:
        prompt = "Digite uma outra data ou 'sair': "

    data_input = input(prompt).strip()

    if data_input.lower() == 'sair':
        break

    try:
        dia, mes, ano = validar_data(data_input)

        # Verifica se a data é anterior a 02/01/2022 e exibe um erro se for o caso
        if (ano < 2022) or (ano == 2022 and mes < 1) or (ano == 2022 and mes == 1 and dia < 2):
            print("\nAtenção: Esta data é anterior ao lançamento oficial do jogo em 02/01/2022);")
            print("Entretato, as hipotéticas respostas dadas ainda seguem o algoritmo original.")

        indice_dia = indice_do_dia_a_partir_de_string(data_input)
        solucoes = solucoes_diarias(respostas_palavras, dueto_indices, quarteto_indices, indice_dia)

        print("\n--- Respostas ---")
        print(f"Termo: {solucoes[1][0]}")
        print(f"Dueto: {solucoes[2][0]} e {solucoes[2][1]}")  # formato "palavra1 e palavra2"
        print(f"Quarteto: {', '.join(solucoes[4][:-1]) + ' e ' + solucoes[4][-1]}\n")  # formato "palavra1, palavra2, palavra3 e palavra4", além de uma nova linha para espaçamento

    except ValueError as ve:
        print(f"\nErro de validação: {ve}\n")
    except Exception as e:
        print(f"\nErro inesperado: {e}\n")
