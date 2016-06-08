# -*- coding: utf-8 -*-
# author: Alfred

from db2charts.settings import analysis_db_modules
from django.db import models as django_models

class AnalysisBase(object):
    def __init__(self):
        super(AnalysisBase, self).__init__()
        self.modules = analysis_db_modules

    def get_dbs(self):
        return self.modules.keys()

    def get_models(self, db):
        module = self.modules[db]
        models = []
        for model_name in dir(module):
            try:
                klass = getattr(module, model_name)
                if issubclass(klass, django_models.Model):
                    models.append({
                        'model_name': '%s.%s' % (db, model_name), 
                        'cols': [x for x in klass._meta.concrete_fields]
                        })
            except Exception, e:
                pass
        return models

    def get_columns(self, db, model):
        model_class = getattr(self.modules[db], model)
        return [x for x in model_class._meta.concrete_fields]