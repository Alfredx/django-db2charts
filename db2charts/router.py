# -*- coding: utf-8 -*-
# author: Alfred

import os
import re

DB_MODULE_PATTERN = re.compile(r'db2charts_models\.(?P<module>.*)_models')

class DB2ChartsRouter(object):
    def db_for_module(self, module):
        match = DB_MODULE_PATTERN.match(module)
        if match:
            return match.groupdict()['module']
        return None

    def db_for_read(self, model, **hints):
        return self.db_for_module(model.__module__)

    def db_for_write(self, model, **hints):
        return self.db_for_module(model.__module__)

    def allow_migrate(self, db, app_label, model=None, **hints):
        return False