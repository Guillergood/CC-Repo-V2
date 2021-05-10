import pandas as lectorCsv
import pymongo
from pymongo import MongoClient

def captura():
    
    temperatura = lectorCsv.read_csv("./Datos/temperature.csv")
    humedad = lectorCsv.read_csv("./Datos/humidity.csv")

    temperatura = temperatura[['datetime','San Francisco']]
    temperatura = temperatura.rename(columns={'San Francisco': 'Temperatura'})

    humedad = humedad[['datetime','San Francisco']]
    humedad = humedad.rename(columns={'San Francisco': 'Humedad'})

    datos = lectorCsv.merge(temperatura,humedad, on= 'datetime')
    # Limpiar datos https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
    datos = datos.dropna()
    # Coge los 100 ultimos, empezando por abajo https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.tail.html
    datos = datos.tail(100)

    # How to connect with MongoClient https://mongodb.github.io/node-mongodb-native/driver-articles/mongoclient.html
    # https://stackoverflow.com/questions/40346767/pymongo-auth-failed-in-python-script
    # https://pymongo.readthedocs.io/en/stable/examples/authentication.html
    client = MongoClient('mongodb+srv://%s:%s@p2gbv.lpeag.mongodb.net/SanFrancisco?retryWrites=true&w=majority' % ('admin', 'admin'))
    # El nombre de la base de datos
    baseDeDatos = client["SanFrancisco"]
    # La columna que voy a usar
    columna = baseDeDatos["Pronostico"]
    # Poner un indice, pero sin hacer ninguna copia (inplace=True) https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html
    datos.reset_index(inplace=True)
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
    data_dict = datos.to_dict("records")
    # Bulk insert https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/
    # https://pymongo.readthedocs.io/en/stable/tutorial.html TIENE QUE SER UN CLIENTE NO UN DATABASE OBJECT
    columna.insert_many(data_dict)

if __name__ == '__main__':
    captura()