from django.conf import settings
import sys

DB2CHARTS_DB = {}
DB2CHARTS_ROUTER = 'db2charts.router.DB2ChartsRouter'

if not 'makemigrations' in sys.argv:
    if hasattr(settings, 'DB2CHARTS_DB'):
        settings.DATABASES.update(settings.DB2CHARTS_DB)
    else:
        settings.DB2CHARTS_DB = DB2CHARTS_DB

if hasattr(settings, 'DB2CHARTS_ROUTER'):
    DB2CHARTS_ROUTER = settings.DB2CHARTS_ROUTER
if hasattr(settings, 'DATABASE_ROUTERS'):
    if not DB2CHARTS_ROUTER in settings.DATABASE_ROUTERS:
        settings.DATABASE_ROUTERS.insert(0, DB2CHARTS_ROUTER)
    else:
        settings.DATABASE_ROUTERS = [DB2CHARTS_ROUTER,]

analysis_db_modules = {}
if not 'autogen' in sys.argv:
    for (key, value) in settings.DB2CHARTS_DB.items():
        db2charts_models = __import__('db2charts_models.%s_models'%key)
        analysis_db_modules[key] = getattr(db2charts_models, '%s_models'%key)
