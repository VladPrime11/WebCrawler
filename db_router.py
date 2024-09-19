class UrlQueueRouter:
    """
    Маршрутизатор для отправки запросов приложения url_queue в отдельную базу данных.
    """
    def db_for_read(self, model, **hints):
        """
        Указывает, в какую базу данных направлять запросы на чтение для моделей.
        """
        if model._meta.app_label == 'url_queue':
            return 'url_queue_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Указывает, в какую базу данных направлять запросы на запись для моделей.
        """
        if model._meta.app_label == 'url_queue':
            return 'url_queue_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Определяет, можно ли создавать связи между объектами из разных баз данных.
        """
        if obj1._meta.app_label == 'url_queue' or obj2._meta.app_label == 'url_queue':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Определяет, в какую базу данных отправлять команды для миграций.
        """
        if app_label == 'url_queue':
            return db == 'url_queue_db'
        return db == 'default'
