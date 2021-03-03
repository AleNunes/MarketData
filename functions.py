from datetime import datetime
import pandas as pd
import json



def check_date(dt):
    '''
    check_date(DateRef): Verifica se a data fornecida é uma data válida no formato YYYY-MM-DD
    Verificar se a data está contida na série
    ''' 
    
    y, m, d = dt.split('-')

    is_valid = True
    try:
        dt = datetime(int(y),int(m),int(d))
        df_datas = pd.read_csv('data/cdi.csv', parse_dates=True)
        
        dt_min = str(df_datas['date'].min())
        dt_max = str(df_datas['date'].max())

        #datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

        print('{} - {} - {}'.format(dt_min, dt, dt_max))
        
        #if dt < df_datas['date'].min() or dt > df_datas['date'].max():
        #    is_valid = False
        #    print('{}'.format(dt))
            #raise TypeError('Data fora do intervalo permitido. ')

    except :
        is_valid = False
        raise TypeError('Formato de data invalido')
    
    

    print(df_datas)
    return is_valid


def check_date_interval(dt_ini, dt_fim):
    if check_date(dt_ini) & check_date(dt_fim):
        if dt_ini <= dt_fim:
            return True
        else:
            raise TypeError('Verifique o intervalo de Datas. Data inicial deve ser menos que a Data Final')
    else:
        raise TypeError('Verifique o formato das datas (aaaa-mm-dd)')






#print(check_date('2020-05-01')) 