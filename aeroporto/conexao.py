from mongoengine import connect

def init_mongo():
    connect(
        db="gerenciamento_aeroporto",
        host="localhost",
        port=27017
    )
