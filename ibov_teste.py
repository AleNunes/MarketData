from urllib.request import urlretrieve
import zipfile
import pandas as pd


def get_bvsp_url(year):
    return f'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP'


def download_bvsp_file(year):
    url = get_bvsp_url(year)
    filename = f'data/zipfiles/{year}.zip'
    urlretrieve(url, filename=filename)
    print(f'Fazendo download de {year}')


def unzip_file(year):
    zip_path = f'data/zipfiles/{year}.zip'
    with zipfile.ZipFile(zip_path, 'r') as zfile:
        zfile.extractall('data/bvmf')
    print(f'Arquivo {zip_path} extraido')

def get_bvsp_file(year):
    download_bvsp_file(year)
    unzip_file(year)

def to_float(s):
    if s != '':
        return float(f'{s}')

def parse_line(line):
    data={
        'date':line[2:10],
        'code':line[12:23].strip(),
        'name':line[27:38].strip(),
        #tp_mercado
        'open':to_float(line[56:69].strip()),
        'high':to_float(line[69:82].strip()),
        'low':to_float(line[82:95].strip()),
        'close':to_float(line[108:121].strip()),
        'volume':to_float(line[170:188].strip()),
        #quant_tit
        #quant_neg
    }
    return data

    # tp_mercado:
    # 010 VISTA
    # 012 EXERCÍCIO DE OPÇÕES DE COMPRA
    # 013 EXERCÍCIO DE OPÇÕES DE VENDA
    # 017 LEILÃO
    # 020 FRACIONÁRIO
    # 030 TERMO
    # 050 FUTURO COM RETENÇÃO DE GANHO
    # 060 FUTURO COM MOVIMENTAÇÃO CONTÍNUA
    # 070 OPÇÕES DE COMPRA
    # 080 OPÇÕES DE VENDA



def parse_file(year):
    path = f'data/bvmf/COTAHIST_A{year}.TXT'
    data = []
    print(f'Lendo arquivo {path}')
    with open(path, 'r') as file:
        for line in file.readlines()[1:-1]:
            datum = parse_line(line)
            data.append(datum)
    return data





#get_bvsp_file(2020)


ano_ini = 2015
ano_fim = 2021

for year in range(ano_ini, ano_fim):
    get_bvsp_file(year)


all_data = []
for year in range(ano_ini, ano_fim):
    data = parse_file(year)
    all_data = all_data + data


df = pd.DataFrame(all_data)
df.date = pd.to_datetime(df.date)

print(df.head())

petr4 = df[df.code == 'PETR4'].sort_values('date')
petr4.set_index('date', inplace=True)


