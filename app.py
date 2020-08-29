from flask import Flask, jsonify, request
import datetime
import pandas as pd
import json

import functions as f
from cdi import CDI
from fundo import Fundo



app = Flask(__name__)


@app.route('/')
def home():
    return jsonify(''), 200


@app.route('/teste', methods=['GET'])
def teste():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        resp, msg = f.check_date_interval(dt_ini, dt_fim)
        if(resp):
            return 'teste: {} - {}'.format(dt_ini, dt_fim), 200

    return msg, 400


@app.route('/cdi', methods=['GET'])
def cdi():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        try:
            f.check_date_interval(dt_ini, dt_fim)
        except Exception as err:
            return 'Erro: {}'.format(err), 400

        cdi = CDI(dt_ini, dt_fim)

        df_cdi = cdi.dataframe()
        ftr_cdi_periodo = cdi.fator()


        js = {
            'Data_Inicio': dt_ini,
            'Data_Fim': dt_fim,
            'fator_periodo':ftr_cdi_periodo,
            'Serie': json.loads(df_cdi.to_json(orient='index', date_format='iso'))
        }

        return js #df_cdi.to_json(orient='index', date_format='iso' )

    return 'Por favor, informe um intervalo de datas no formato dt_ini=aaaa-mm-dd & dt_fim=aaaa-mm-dd', 400





@app.route('/fundo', methods=['GET'])
def fundo():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        try:
            f.check_date_interval(dt_ini, dt_fim)
        except Exception as err:
            return 'Erro: {}'.format(err), 400

        fz = Fundo()

        df = fz.dataframe(dt_ini, dt_fim)
        
        js = {
            'Data_Inicio': dt_ini,
            'Data_Fim': dt_fim,
            'Rent_Periodo':fz.rent_periodo(dt_ini, dt_fim),
            'Rent_CDI':fz.rent_periodo_cdi(dt_ini, dt_fim),
            'Evolucao_PL': fz.evolucao_pl(dt_ini, dt_fim),
            'Max_Rent':fz.max(dt_ini, dt_fim),
            'Min_Rent':fz.min(dt_ini, dt_fim),
            'Serie': json.loads(df.to_json(orient='index', date_format='iso'))
        }

        return js #df_cdi.to_json(orient='index', date_format='iso' )

    return 'Por favor, informe um intervalo de datas no formato dt_ini=aaaa-mm-dd & dt_fim=aaaa-mm-dd', 400






if __name__ == '__main__':
    app.run(debug=True, port=5000)



