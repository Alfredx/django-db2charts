# -*- coding: utf-8 -*-
# author: Alfred

default_label = ['auth', 'sessions', 'admin', 'contenttypes', 'staticfiles', 'messages',
                     'db2charts']
analysis_db_label = ['db_models',]


class Router(object):
    """    
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_app(self, app_label):
        if app_label in default_label:
            return 'default'
        if app_label in analysis_db_label:
            return 'analysis_db'
        return None

    def db_for_read(self, model, **hints):
        return self.db_for_app(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self.db_for_app(model._meta.app_label)

    def allow_migrate(self, db, app_label, model=None, **hints):
        db_name = self.db_for_app(app_label)
        if db_name is None:
            return None
        return db == db_name
