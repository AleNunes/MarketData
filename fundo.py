import pandas as pd
import functions as f
from cdi import CDI

class Fundo:
    def __init__(self):

        self.__df = pd.read_csv('data/zarathustra.csv', index_col=0, parse_dates=True)
        
        # Garantir que o index (data) está em ordem crescente para não ter problemas com o pct_change()
        self.__df.sort_index(ascending=True, inplace=True)
        self.__df['var_cota'] = self.__df.pct_change()['cota']
        self.__df['ftr_cota'] = self.__df['var_cota'] + 1


        # Altera tipo de Data para String, para padronizar o formato da data
        #self.__df.index = self.__df.index.strftime('%Y-%m-%d')

    # Funcao generica para retornar valor do dataframe
    def __get_valor(self, campo, dt):
        try:
            f.check_date(dt)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        #print(self.__df[campo][dt])
        return self.__df[campo][dt]

    # Retorna PL do fundo em uma data específica
    def pl(self, dt):
        '''Retorna Patrimonio liquido em uma data específica'''
        return(self.__get_valor('pl',dt))

    # Retorna cota do fundo em uma data específica
    def cota(self, dt):
        '''Retorna Valor da Cota em uma data específica'''
        return(self.__get_valor('cota',dt))

    # Retorna Rentabilidade do fundo em uma data específica
    def variacao(self, dt):
        '''Retorna Rentabilidade em uma data específica'''
        return(self.__get_valor('var_cota',dt))

    # Rentabilidade em um periodo
    def rent_periodo(self, ini, fim):
        '''Retorna rentabilidade em um período, onde ini é a data inicial e fim é a data final'''
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        r1 = self.__df.loc[ini:fim]['ftr_cota'].product(axis=0) - 1
        # outra opcao de calculo seria : cota(dt_fim) / cota(dt_ini) - 1
        #print('1 - Rentabilidade do período em porcentagem: {:.4%}'.format(r1))
        return r1
        

    def rent_periodo_cdi(self, ini, fim):
        '''Retorna rentabilidade em %CDI de um período, onde ini é a data inicial e fim é a data final'''
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        rent_fundo = self.__df.loc[ini:fim]['ftr_cota'].product(axis=0) - 1
        cdi = CDI(ini,fim)
        rent = rent_fundo/cdi.fator()

        #print('2 - Rentabilidade do CDI: {:.4%}'.format(rent))
        return rent

    
    def evolucao_pl(self, ini, fim):
        '''Retorna Evolução do PL um período, onde ini é a data inicial e fim é a data final'''
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        idx = self.__df.index.get_loc(ini)
        dt = self.__df.index.strftime('%Y-%m-%d').values[idx-1]
        #print('{} - {}'.format(dt, self.pl(dt)))

        return self.pl(fim) - self.pl(dt)


    def max(self, ini, fim):
        '''Retorna Maior variação e a data dentro de um período, onde ini é a data inicial e fim é a data final'''
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        var = self.__df[ini:fim]['var_cota'].max()
        dt = self.__df[ini:fim]['var_cota'][self.__df[ini:fim]['var_cota']==var].index.item()

        return dt.strftime('%Y-%m-%d'), var

    
    def min(self, ini, fim):
        '''Retorna Menor variação e a data dentro de um período, onde ini é a data inicial e fim é a data final'''
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()
        
        var = self.__df[ini:fim]['var_cota'].min()
        dt = self.__df[ini:fim]['var_cota'][self.__df[ini:fim]['var_cota']==var].index.item()

        return dt.strftime('%Y-%m-%d'), var


    def dataframe(self, ini, fim):
        
        self.ini = ini
        self.fim = fim

        # Verifica se as datas são válidas e se o intervalo é válido (inicio < fim)
        try:
            f.check_date_interval(self.ini, self.fim)
        except Exception as err:
            print('Erro: {}'.format(err))
            exit()

        idx = self.__df.index.get_loc(ini)
        dt = self.__df.index.strftime('%Y-%m-%d').values[idx-1]

        cota_ref = self.cota(dt)
        
        df = self.__df[ini:fim]
        df['rent_acumulada'] = df['cota']/cota_ref - 1

        # Altera tipo de Data para String, para padronizar o formato da data
        df.index = df.index.strftime('%Y-%m-%d')

        return df


    #def fator(self):
    #    return self.__df['ftr_dia'].product(axis=0) - 1



#zara = Fundo()

#dt_inicio = '2019-01-02'
#dt_fim = '2019-01-31'

#print( zara.dataframe(dt_inicio, dt_fim))
#print( zara.rent_periodo(dt_inicio, dt_fim))
#print( zara.rent_periodo_cdi(dt_inicio, dt_fim))
#print(zara.pl(dt_inicio ))
#print(zara.cota(dt_inicio ))
#print(zara.variacao(dt_inicio ))
#print( zara.evolucao_pl(dt_inicio, dt_fim))
#print( zara.max(dt_inicio, dt_fim))
#print( zara.min(dt_inicio, dt_fim))


#print((zara.cota(dt_fim)/ zara.cota('2018-12-31')-1)*100)
