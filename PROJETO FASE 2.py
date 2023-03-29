import matplotlib.pyplot as plt
from datetime import datetime
import statistics

#le os arquivos
def carregaDados(arquivo):
    arquivo = open("ArquivoDadosProjeto.csv", "r")
    dados = []
    for linha in arquivo:
        if 'sepal' in linha: continue
        valores = linha[:-1].split(";")
        tupla = ((valores[0]),(valores[1]),(valores[2]),(valores[3]),(valores[4]),(valores[5]),(valores[6]), (valores[7]))
        dados.append(tupla)
    arquivo.close()


#adicionei em um dicionario os dados de precipitacao e as datas
def dadosPrecipitacao(dados):
    dict = {}
    for tupla in dados:
        chave = tupla[0]
        precipitacao = tupla[1]
        dict[chave].append((precipitacao))
    return dict
#Varre o dicionario para encontrar o maior valor da precipitacao
def mesMaisChuvoso(dados):
    maiorPrecipitacao = 0
    for chave, valor in dados.items():
        if valor > maiorPrecipitacao:
            maiorPrecipitacao = valor
            data = chave
    return data, maiorPrecipitacao

#retornar a media enter os ultimos 10 anos 
def mediaModaTempMinimaUmidadeVento(dados):
    dic = {}
    for linha in dados:
        for tupla in linha:
            chave = tupla[0]
            valor_temp = float(tupla[5])
            valor_umidade = float(tupla[6])
            valor_vento = float(tupla[7])
            if chave not in dic:
                dic[chave] = []
            dic[chave].append((valor_temp, valor_umidade, valor_vento))
    data_tabela = datetime.strptime(tupla[0],  '%d/%m/%Y')
    if data_tabela.year >=2006 and data_tabela.year <=2016 and  data_tabela.month == 8:
        moda_temperaturas = {}
        moda_umidade = {}
        moda_vento = {}
        media_temperaturas = {}
        media_umidade = {}
        media_vento = {}
        for chave, valores in dic.items():
            temperaturas = [valor[0] for valor in valores]
            moda_temperaturas[chave] = statistics.mode(temperaturas)
            media_temperaturas[chave] = statistics.mean(temperaturas)
        
            umidades = [valor[1] for valor in valores]
            moda_umidade[chave] = statistics.mode(umidades)
            media_umidade[chave] = statistics.mean(umidades)
        
            ventos = [valor[2] for valor in valores]
            moda_vento[chave] = statistics.mode(ventos)
            media_vento[chave] = statistics.mean(ventos)
    
    return moda_temperaturas, moda_umidade, moda_vento, media_temperaturas, media_umidade, media_vento

def decadaMaisChuvosa(dados):
    dadosFiltrados = []
    for linha in dados:
        linha[0] = datetime.strptime(linha[0], '%d/%m/%Y')
        linha[1] = float(linha[1])
        if linha[0].year >= 1961 and linha[0].year <= 2016:
            dadosFiltrados.append(linha)
    
    dadosPorAno = {}
    for linha in dadosFiltrados:
        ano = linha[0].year
        if ano in dadosPorAno:
            dadosPorAno[ano].append(linha[1])
        else:
            dadosPorAno[ano] = [linha[1]]
    mediaPorAno = {ano: sum(dadosPorAno[ano])/len(dadosPorAno[ano]) for ano in dadosPorAno} 

    mediasPorDecada = {}
    for ano in mediaPorAno:
        decada = ((ano-1961)//10) + 1
        if decada in mediasPorDecada:
            mediasPorDecada[decada].append(mediaPorAno[ano])
        else:
            mediasPorDecada[decada] = [mediaPorAno[ano]]
    mediaPorDecada = {decada: sum(mediasPorDecada[decada])/len(mediasPorDecada[decada]) for decada in mediasPorDecada}

    mediasPorDecada = {}
    for ano in mediaPorAno:
        decada = ((ano-1961)//10) + 1
        if decada in mediasPorDecada:
            mediasPorDecada[decada].append(mediaPorAno[ano])
        else:
            mediasPorDecada[decada] = [mediaPorAno[ano]]
    mediaPorDecada = {decada: sum(mediasPorDecada[decada])/len(mediasPorDecada[decada]) for decada in mediasPorDecada}

    decadaMaisChuvosa = max(mediaPorDecada, key=mediaPorDecada.get)
    return decadaMaisChuvosa, (mediaPorDecada[decadaMaisChuvosa], 2)
    

def geraGrafico(mediasPorDecada):
    plt.bar(mediasPorDecada.key(), mediasPorDecada.values())
    plt.xticks(range(len(mediasPorDecada)), ['Década {}'.format(d+1) for d in mediasPorDecada.keys()])
    plt.ylabel('Média acumulada de chuva')
    plt.xlabel('Décadas')
    plt.show()