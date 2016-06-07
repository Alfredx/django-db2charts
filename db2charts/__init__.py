# -*- coding: utf-8 -*-
# author: Alfred


from django.conf import settings

if hasattr(settings, 'DB2CHARTS_DB'):
    settings.DATABASES.update(settings.DB2CHARTS_DB)
