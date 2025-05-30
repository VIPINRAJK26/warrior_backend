from django.apps import AppConfig


class WarriorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warrior_app'
    
    def ready(self):
        import warrior_app.signals
