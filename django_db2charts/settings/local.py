from .base import *



DB2CHARTS_DB = {
    'analysis_db_artenterdefault': {
        # Add 'postgresql_psyOrderManager_depaybatchcopg2', 'mysql', 'sqlite3'
        # or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'artenterdefault',
        'USER': 'artenter',  # Not used with sqlite3.
        'PASSWORD': 'a1b2c3d4',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '192.168.1.121',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': 3306,
    },
    'analysis_db_artenterorder': {
        # Add 'postgresql_psyOrderManager_depaybatchcopg2', 'mysql', 'sqlite3'
        # or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'artenterorder',
        'USER': 'artenter',  # Not used with sqlite3.
        'PASSWORD': 'a1b2c3d4',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '192.168.1.121',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': 3306,
    },
}