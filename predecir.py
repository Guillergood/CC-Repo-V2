import pandas as lectorCsv
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import joblib as jb
#https://stackoverflow.com/questions/61893719/importerror-cannot-import-name-joblib-from-sklearn-externals
#from sklearn.externals import joblib


def predecir(n):

    # Carga modelos https://joblib.readthedocs.io/en/latest/persistence.html
    modeloTemperatura = jb.load('./modeloTemperatura.pkl')
    modeloHumedad = jb.load('./modeloHumedad.pkl')
    
    # Intervalo de confianza https://github.com/manuparra/MaterialCC2020/blob/master/exampleARIMA_humidity.py
    prediccionTemperatura = modeloTemperatura.predict(n_periods=n, return_conf_int=True)
    prediccionHumidity = modeloHumedad.predict(n_periods=n, return_conf_int=True)
    
    hoy = datetime.now()
    #https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.html
    indice = lectorCsv.date_range(hoy, periods=n, freq='H')
    
    datosPrediccion = lectorCsv.DataFrame(index=indice, columns=['Hora','Temperatura','Humedad'])
    # Crear array https://numpy.org/doc/stable/reference/generated/numpy.array.html
    temperatura = np.array(prediccionTemperatura)
    humedad = np.array(prediccionHumidity)
    # Meter en la columna hora los indices, que es la fecha https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.strftime.html#pandas.DatetimeIndex.strftime
    datosPrediccion['Hora'] = indice.strftime('%B %d, %Y, %r')
    datosPrediccion['Temperatura'] = np.ndarray((n,), buffer=temperatura)
    datosPrediccion['Humedad'] = np.ndarray((n,), buffer=humedad)

    return datosPrediccion.to_json(orient='records')
