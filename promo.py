from csv import DictReader
import pandas as pd
# Crie um algoritmo que, informando o resultado do Concurso 05318 da loteria
# federal o sistema retorne o CPF do ganhador e a quantidade de participações
# do mesmo nessa promoção.
# entrada = str(input('Digite um elemento sorteavel '))
# 05318 = 35 01176
# 05128 mais de 1 vez    

def abrir_arquivo(filename):
    arquivo = open(filename)
    tabela = DictReader(arquivo)
    return tabela

"""
Encontrar a maior serie dentro da tabela
"""
def encontrar_maior_serie(tabela):
    maior_valor = 0
    for linha in tabela:
        if maior_valor < int(linha['numero_da_sorte'][:2]):
            maior_valor = int(linha['numero_da_sorte'][:2])
    return maior_valor

"""
Verificar se a serie existe, se nao, diminuir seu valor ate ser
"""

def verificar_serie(serie_sorteada, maior_serie):
    if maior_serie == serie_sorteada: 
        return serie_sorteada
    while True:
        if abs(serie_sorteada) > maior_serie:
            serie_sorteada = abs(serie_sorteada - maior_serie)
        else :
            if (serie_sorteada >= 0 and serie_sorteada <= 9):
                return f'0{str(abs(serie_sorteada))}'.strip()
            return abs(serie_sorteada)
"""
Cria uma lista com os valores da serie
"""
def sorteaveis(tabela, serie, sorteado):
    import time
    lista_serie = []
    print(serie)
    for linha in tabela.itertuples():
        valor = str(linha.numero_da_sorte)
        if len(valor) == 6:
            valor = f'0{valor}'
        elif len(valor) == 5:
            valor = f'00{valor}'
        elif len(valor) == 4:
            valor = f'000{valor}'
        if (valor.startswith(serie, 0, 2)):
            lista_serie.append(valor)
            if (valor[2:] == sorteado):
                print(valor)
    return lista_serie

"""
verifica a posicao do valor mais proximo acima do sorteado
"""
def listar_sorteaveis(lista_sorteavel, sorteado):
    start = 0
    lista_sorteavel.sort()
    
    for index_value in range(0, len(lista_sorteavel)):
        if lista_sorteavel[index_value] == sorteado:
            return 'Ganhador'
        if lista_sorteavel[index_value] > sorteado:
            start = index_value
            return start
"""
Caso nao haja o valor sorteado, verifique acima, se nao, verifique abaixo do valor
"""
def iterar_lista(lista_sorteavel, starter_index):
    for index_value in range(0, len(lista_sorteavel)):
        check_up = starter_index + index_value
        check_down = abs(starter_index - index_value)
        if check_up < len(lista_sorteavel):
            if (lista_sorteavel[check_up]):
                return lista_sorteavel[check_up]
        if check_down < len(lista_sorteavel) and check_down >= 0:
            if (lista_sorteavel[check_down]):
                return lista_sorteavel[check_down]
        
"""
Encontrado o valor, aqui se faz a coleta do vencedor na tabela do DataFrame original
"""
def encontrar_ganhador(tabela, numero_sorteado):
    ganhadores = []
    qtd_participacoes = 0
    for valor in tabela.itertuples():
        if len(str(valor.numero_da_sorte)) == 6:
            cmp_valor = f'0{valor.numero_da_sorte}'
        elif len(str(valor.numero_da_sorte)) == 5:
            cmp_valor = f'00{valor.numero_da_sorte}'
        elif len(str(valor.numero_da_sorte)) == 4:
            cmp_valor = f'000{valor.numero_da_sorte}'
        else:
            cmp_valor = str(valor.numero_da_sorte)
        if cmp_valor == str(numero_sorteado):
            print(cmp_valor)
            ganhadores.append(valor)
            qtd_participacoes += 1
    return (ganhadores, qtd_participacoes)

if __name__ == '__main__':
    serie_encontrada_sorteio = '35'
    elemento_sorteavel = '01176'
    filename = 'dados_promo.csv'
    with open(filename) as f:
        tabela = DictReader(f)
        maior_serie = encontrar_maior_serie(tabela)
    serie_final = str(verificar_serie(int(serie_encontrada_sorteio), maior_serie))
    f = pd.read_csv(filename)
    tabela = pd.DataFrame(f)
    ls = sorteaveis(tabela, serie_final, elemento_sorteavel)
    start = listar_sorteaveis(ls, (str(serie_final) + elemento_sorteavel))
    ls.sort()
    ganhador = iterar_lista(ls, start)
    
    ganhadores = encontrar_ganhador(tabela, ganhador)
    print(f'Ganhador foi o.O CPF {ganhadores[0][0].cpf}, num. de tentativa(s): {ganhadores[1]}')
