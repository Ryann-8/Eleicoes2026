import pandas as pd

COLUNA_VOTOS = 'QT_VOTOS_NOMINAIS_VALIDOS'

def calcular_bloco(bloco):
    bloco = bloco[bloco['NM_MUNICIPIO'].str.strip().str.upper() == 'ILHABELA'].copy()
    bloco[COLUNA_VOTOS] = pd.to_numeric(bloco[COLUNA_VOTOS], errors='coerce')
    bloco = bloco.dropna(subset=[COLUNA_VOTOS])

    partidos = bloco.groupby('SG_PARTIDO')[COLUNA_VOTOS].agg(['sum', 'count'])
    cargos = bloco.groupby('DS_CARGO')[COLUNA_VOTOS].agg(['sum', 'count'])

    return (bloco[COLUNA_VOTOS].sum(), len(bloco),
            partidos.to_dict('index'), cargos.to_dict('index'))

def juntar_resultados(resultados):
    total_votos = 0
    total_registros = 0
    partidos = {}
    cargos = {}

    for soma, quantidade, dados_partidos, dados_cargos in resultados:
        total_votos += soma
        total_registros += quantidade

        for nome, valores in dados_partidos.items():
            if nome not in partidos:
                partidos[nome] = [0, 0]
            partidos[nome][0] += valores['sum']
            partidos[nome][1] += valores['count']

        for nome, valores in dados_cargos.items():
            if nome not in cargos:
                cargos[nome] = [0, 0]
            cargos[nome][0] += valores['sum']
            cargos[nome][1] += valores['count']

    if total_registros == 0:
        print('Nenhum registro de Ilhabela foi encontrado')
        return

    medias_partidos = {}

    for nome, valores in partidos.items():
        soma = valores[0]
        qtd = valores[1]
        media = soma / qtd
        medias_partidos[nome] = media

    medias_cargos = {}

    for nome, valores in cargos.items():
        soma = valores[0]
        qtd = valores[1]
        media = soma / qtd
        medias_cargos[nome] = media

    return {
        'registros': total_registros,
        'media_geral': total_votos / total_registros,
        'partido': max(medias_partidos, key=medias_partidos.get),
        'media_partido': max(medias_partidos.values()),
        'cargo': max(medias_cargos, key=medias_cargos.get),
        'media_cargo': max(medias_cargos.values()),
    }