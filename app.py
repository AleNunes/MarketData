from flask import Flask, jsonify, request
import datetime
import pandas as pd
import json

def check_date(dt):
    y, m, d = dt.split('-')

    is_valid = True
    try:
        datetime.datetime(int(y),int(m),int(d))
    except :
        is_valid = False
    return is_valid


def check_date_interval(dt_ini, dt_fim):
    if check_date(dt_ini) & check_date(dt_fim):
        if dt_ini <= dt_fim:
            return True, 'OK'
        else:
            return False, 'Verifique o intervalo de Datas. Data inicial deve ser menos que a Data Final'
    else:
        return False, 'Verifique o formato das datas (aaaa-mm-dd)'




app = Flask(__name__)


devs = [
    {'name':'Alex', 'lang':'python'},
    {'name':'Luca', 'lang':'go'}
]

@app.route('/')
def home():
    return jsonify(devs), 200






@app.route('/teste', methods=['GET'])
def teste():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        resp, msg = check_date_interval(dt_ini, dt_fim)
        if(resp):
            return 'teste: {} - {}'.format(dt_ini, dt_fim), 200

    return msg, 400







@app.route('/cdi', methods=['GET'])
def cdi():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        resp, msg = check_date_interval(dt_ini, dt_fim)
        if(resp):


            df_cdi = pd.read_csv('data/cdi.csv', index_col=0, parse_dates=True)
            df_cdi.columns = ['tx_ano','var_dia']

            df_cdi.tx_ano = df_cdi.tx_ano / 100
            df_cdi.var_dia = df_cdi.var_dia.str.rstrip('%').astype(float)/100

            df_cdi['ftr_dia'] = (1 + df_cdi.tx_ano)  ** (1/252)


            df_cdi = df_cdi[dt_ini:dt_fim]
            
            ftr_cdi_periodo = df_cdi['ftr_dia'].product(axis=0) - 1

            
            # Altera tipo de Data para String, para padronizar o formato da data
            df_cdi.index = df_cdi.index.strftime('%Y-%m-%d')
            
            js = {
                'Data_Inicio': dt_ini,
                'Data_Fim': dt_fim,
                'fator_periodo':ftr_cdi_periodo,
                'Serie': json.loads(df_cdi.to_json(orient='index', date_format='iso'))
            }


            return js #df_cdi.to_json(orient='index', date_format='iso' )


            #return 'teste: {} - {}'.format(dt_ini, dt_fim), 200

    return msg, 400









if __name__ == '__main__':
    app.run(debug=True, port=5000)





