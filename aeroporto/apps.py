from django.apps import AppConfig

class AeroportoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aeroporto'

    def ready(self):
        from .conexao import init_mongo
        init_mongo()
