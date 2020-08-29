import pandas as pd
import functions as f



class CDI:
    def __init__(self, ini='2012-03-07', fim='2012-12-31'):
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()


        # Lendo Serie hitórica do CDI
        self.__df = pd.read_csv('data/cdi.csv', index_col=0, parse_dates=True)

        # Renomeando series e ajustando numeros
        self.__df.columns = ['tx_ano','var_dia']
        self.__df.tx_ano = self.__df.tx_ano / 100
        self.__df.var_dia = self.__df.var_dia.str.rstrip('%').astype(float)/100

        # recalculando fator diário do cdi
        self.__df['ftr_dia'] = (1 + self.__df.tx_ano)  ** (1/252)

        self.__df = self.__df[ini:fim]
        
        # Altera tipo de Data para String, para padronizar o formato da data
        self.__df.index = self.__df.index.strftime('%Y-%m-%d')

    def dataframe(self):
        return self.__df


    def fator(self):
        return self.__df['ftr_dia'].product(axis=0) - 1



cdi = CDI("2020-01-1", '2020-01-31')

print( cdi.dataframe())
print( cdi.fator())
