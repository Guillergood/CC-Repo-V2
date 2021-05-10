import pandas as lectorCsv
import pymongo
from pymongo import MongoClient
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import pmdarima as pm
import joblib as jb


def crearModelo():

    # How to connect with MongoClient https://mongodb.github.io/node-mongodb-native/driver-articles/mongoclient.html
    # https://stackoverflow.com/questions/40346767/pymongo-auth-failed-in-python-script
    client = MongoClient('mongodb+srv://%s:%s@p2gbv.lpeag.mongodb.net/SanFrancisco?retryWrites=true&w=majority' % ('admin', 'admin'))
    baseDatos = client["SanFrancisco"]
    columna = baseDatos["Pronostico"]
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    marcoDeDatos = lectorCsv.DataFrame(list(columna.find()))
    marcoDeDatos = marcoDeDatos[['datetime','Temperatura','Humedad']]

    # Guardar el modelo https://scikit-learn.org/stable/modules/model_persistence.html
    # SARIMAX https://www.statsmodels.org/dev/examples/notebooks/generated/statespace_sarimax_stata.html
    modeloTemperatura = SARIMAX(marcoDeDatos['Temperatura'],
                                trend='c', order=(1,1,1),
                                enforce_invertibility=False,
                                enforce_stationarity=False)
    modeloTemperatura = modeloTemperatura.fit()

    modeloHumedad = SARIMAX(marcoDeDatos['Humedad'],
                                    trend='c', order=(1,1,1),
                                    enforce_invertibility=False,
                                    enforce_stationarity=False)
    modeloHumedad = modeloHumedad.fit()

    jb.dump(modeloTemperatura, './modeloTemperatura.pkl')
                        
    # Guardar el modelo https://scikit-learn.org/stable/modules/model_persistence.html
    jb.dump(modeloHumedad, './modeloHumedad.pkl')

if __name__ == '__main__':
    crearModelo()