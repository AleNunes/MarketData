from flask import Flask, jsonify, request
import datetime
import pandas as pd
import json

import functions as f
from cdi import CDI
from fundo import Fundo



app = Flask(__name__)

# Definindo rota padrao
@app.route('/')
def home():
    return jsonify(''), 200

# Testes iniciais com a api
@app.route('/teste', methods=['GET'])
def teste():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        resp, msg = f.check_date_interval(dt_ini, dt_fim)
        if(resp):
            return 'teste: {} - {}'.format(dt_ini, dt_fim), 200

    return msg, 400

# Rota de consulta ao CDI
@app.route('/cdi', methods=['GET'])
def cdi():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        try:
            f.check_date_interval(dt_ini, dt_fim)
        except Exception as err:
            # Erro na verificação das datas
            return 'Erro: {}'.format(err), 400

        # Chmando a classe e definindo intervalo
        cdi = CDI(dt_ini, dt_fim)

        # Buscando dataframe com dados do CDI
        df_cdi = cdi.dataframe()
        ftr_cdi_periodo = cdi.fator()

        # Montando dicionário com as informações do CDI
        js = {
            'Data_Inicio': dt_ini,
            'Data_Fim': dt_fim,
            'fator_periodo':ftr_cdi_periodo,
            'Serie': json.loads(df_cdi.to_json(orient='index', date_format='iso'))
        }

        # Retorna dicionario completo
        return js #df_cdi.to_json(orient='index', date_format='iso' )

    # Erro caso uma das datas não seja informada
    return 'Por favor, informe um intervalo de datas no formato dt_ini=aaaa-mm-dd & dt_fim=aaaa-mm-dd', 400





@app.route('/fundo', methods=['GET'])
def fundo():
    dt_ini = request.args.get('dt_ini')
    dt_fim = request.args.get('dt_fim')

    if dt_ini and dt_fim: 
        try:
            f.check_date_interval(dt_ini, dt_fim)
        except Exception as err:
            # Erro na validação da datas
            return 'Erro: {}'.format(err), 400

        # Instancia a classe de fundo
        fz = Fundo()

        # Busca dataframe filtrado
        df = fz.dataframe(dt_ini, dt_fim)
        
        # Cria dicionario com as metricas
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

        #retorna o dicionario completo
        return js #df_cdi.to_json(orient='index', date_format='iso' )
    
    # Data não informada corretamente
    return 'Por favor, informe um intervalo de datas no formato dt_ini=aaaa-mm-dd & dt_fim=aaaa-mm-dd', 400



if __name__ == '__main__':
    app.run(debug=True, port=5000)

