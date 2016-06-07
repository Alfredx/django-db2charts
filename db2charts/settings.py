from django.conf import settings
import sys

if hasattr(settings, 'DB2CHARTS_DB'):
    settings.DATABASES.update(settings.DB2CHARTS_DB)
else:
    settings.DB2CHARTS_DB = {}

analysis_db_modules = {}
if not 'autogen' in sys.argv:
    for (key, value) in settings.DB2CHARTS_DB.items():
        db2charts_models = __import__('db2charts_models.%s_models'%key)
        analysis_db_modules[key] = getattr(db2charts_models, '%s_models'%key)
