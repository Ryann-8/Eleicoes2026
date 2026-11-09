import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
from calculos import calcular_bloco, juntar_resultados

ARQUIVO = 'dados/votacao_candidato_munzona_2026_SP.csv'
COLUNAS = ['NM_MUNICIPIO', 'SG_PARTIDO', 'DS_CARGO', 'QT_VOTOS_NOMINAIS_VALIDOS']


def executar(tipo):
    inicio = time.perf_counter()

    blocos = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', usecols=COLUNAS, chunksize=100000, low_memory=False)

    if tipo == 'Processos':
        executor = ProcessPoolExecutor
    else:
        executor = ThreadPoolExecutor

    with executor(max_workers=8) as grupo:
        resultados = grupo.map(calcular_bloco, blocos)
        resumo = juntar_resultados(resultados)

    tempo = time.perf_counter() - inicio
    return resumo, tempo



def mostrar_resultados(nome, resultado, tempo):
    print('\n=-=', nome, '=-=')
    print('Cidade: Ilhabela')
    print('Registros:', resultado['registros'])
    print('Média geral:', resultado['media_geral'])
    print('Partido com maior média:', resultado['partido'],
          '-', resultado['media_partido'], 2)
    print('Cargo com maior média:', resultado['cargo'],
          '-', resultado['media_cargo'])
    print('Tempo:', tempo, 'segundos')


if __name__ == '__main__':
    print('Analisando os votos de Ilhabela...')

    dados_processos, tempo_processos = executar('Processos')
    dados_threads, tempo_threads = executar('Threads')

    mostrar_resultados('Multiprocessing', dados_processos, tempo_processos)
    mostrar_resultados('Multithreading', dados_threads, tempo_threads)

    print('\n--- Comparação ---')
    if tempo_processos < tempo_threads:
        print('Melhor desempenho: Multiprocessing')
    elif tempo_threads < tempo_processos:
        print('Melhor desempenho: Multithreading')
    else:
        print('Empate')