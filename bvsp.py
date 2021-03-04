from urllib.request import urlretrieve
import zipfile
import pandas as pd




class BVSP:
    def __init__(self, ano='2021'):
        self.ano = ano

        self.get_bvsp_file()
        

    def get_bvsp_url(self):
        return f'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{self.ano}.ZIP'


    def download_bvsp_file(self):
        url = self.get_bvsp_url()
        filename = f'data/zipfiles/{self.ano}.zip'
        urlretrieve(url, filename=filename)
        print(f'Fazendo download de {self.ano}')
        return True
    
    def unzip_file(self):
        zip_path = f'data/zipfiles/{self.ano}.zip'
        with zipfile.ZipFile(zip_path, 'r') as zfile:
            zfile.extractall('data/bvmf')
        print(f'Arquivo {zip_path} extraido')
        return True

    def get_bvsp_file(self):
        self.download_bvsp_file()
        self.unzip_file()

    def to_float(self, s):
        if s != '':
            return float(f'{s}')


    def parse_line(self, line):
        data={
            'date':line[2:10],
            'code':line[12:23].strip(),
            'tp_mercado':line[24:27].strip(),
            'name':line[27:38].strip(),
            'open':self.to_float(line[56:69].strip()),
            'high':self.to_float(line[69:82].strip()),
            'low':self.to_float(line[82:95].strip()),
            'close':self.to_float(line[108:121].strip()),
            'volume':self.to_float(line[170:188].strip()),
            'quant_tit':self.to_float(line[152:170].strip()),
            'quant_neg':self.to_float(line[147:152].strip()),
        }
        return data


    def get_data(self):
        path = f'data/bvmf/COTAHIST_A{self.ano}.TXT'
        data = []
        print(f'Lendo arquivo {path}')
        with open(path, 'r') as file:
            for line in file.readlines()[1:-1]:
                datum = self.parse_line( line)
                data.append(datum)
        return data


    def get_dataframe(self):
        df = pd.DataFrame(self.get_data())
        df.date = pd.to_datetime(df.date)
        return df




x = BVSP(2021)
#x.download_bvsp_file()
#x.unzip_file()
#x.get_bvsp_file()


#data = x.get_data()
df = x.get_dataframe()

print(df.head())




 



