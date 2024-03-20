# routers.py

class CustomDBRouter:
    """
    A router to control all database operations on models in the
    your_app_label application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read your_app_label models go to custom_db.
        """
        if model._meta.app_label == 'CrimeAnalysis':
            return 'custom_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write your_app_label models go to custom_db.
        """
        if model._meta.app_label == 'CrimeAnalysis':
            return 'custom_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the your_app_label app only appears in the 'custom_db'
        database.
        """
        if app_label == 'CrimeAnalysis':
            return db == 'custom_db'
        return None
