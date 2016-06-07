# -*- coding: utf-8 -*-
# author: Alfred

from __future__ import unicode_literals
from collections import OrderedDict
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.commands.inspectdb import Command as inspectdbCommand
from django.db import connections
import keyword
import os
import re

class inspectdb(inspectdbCommand):
    def handle_inspection(self, options):
        connection = connections[options['database']]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        table2model = lambda table_name: re.sub(r'[^a-zA-Z0-9]', '', table_name.title())
        strip_prefix = lambda s: s[1:] if s.startswith("u'") else s

        with connection.cursor() as cursor:
            yield "# This is an auto-generated Django model module."
            yield "# You'll have to do the following manually to clean this up:"
            yield "#   * Rearrange models' order"
            yield "#   * Make sure each model has one field with primary_key=True"
            yield (
                "#   * Remove `managed = False` lines if you wish to allow "
                "Django to create, modify, and delete the table"
            )
            yield "# Feel free to rename the models, but don't rename db_table values or field names."
            yield "#"
            yield "# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'"
            yield "# into your database."
            yield "from __future__ import unicode_literals"
            yield ''
            yield 'from %s import models' % self.db_module
            known_models = []
            for table_name in connection.introspection.table_names(cursor):
                if table_name_filter is not None and callable(table_name_filter):
                    if not table_name_filter(table_name):
                        continue
                yield ''
                yield ''
                yield 'class %s(models.Model):' % table2model(table_name)
                known_models.append(table2model(table_name))
                try:
                    relations = connection.introspection.get_relations(cursor, table_name)
                except NotImplementedError:
                    relations = {}
                try:
                    indexes = connection.introspection.get_indexes(cursor, table_name)
                except NotImplementedError:
                    indexes = {}
                try:
                    constraints = connection.introspection.get_constraints(cursor, table_name)
                except NotImplementedError:
                    constraints = {}
                used_column_names = []  # Holds column names used in the table so far
                column_to_field_name = {}  # Maps column names to names of model fields
                for row in connection.introspection.get_table_description(cursor, table_name):
                    comment_notes = []  # Holds Field notes, to be displayed in a Python comment.
                    extra_params = OrderedDict()  # Holds Field parameters such as 'db_column'.
                    column_name = row[0]
                    is_relation = column_name in relations

                    att_name, params, notes = self.normalize_col_name(
                        column_name, used_column_names, is_relation)
                    extra_params.update(params)
                    comment_notes.extend(notes)

                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name

                    # Add primary_key and unique, if necessary.
                    if column_name in indexes:
                        if indexes[column_name]['primary_key']:
                            extra_params['primary_key'] = True
                        elif indexes[column_name]['unique']:
                            extra_params['unique'] = True

                    if is_relation:
                        rel_to = "self" if relations[column_name][1] == table_name else table2model(relations[column_name][1])
                        if rel_to in known_models:
                            field_type = 'ForeignKey(%s' % rel_to
                        else:
                            field_type = "ForeignKey('%s'" % rel_to
                        # this line is customized to generated a non ERROR model file
                        extra_params['related_name'] = '%s_%s' % (table_name, att_name)
                    else:
                        # Calling `get_field_type` to get the field type string and any
                        # additional parameters and notes.
                        field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                        extra_params.update(field_params)
                        comment_notes.extend(field_notes)

                        field_type += '('

                    # Don't output 'id = meta.AutoField(primary_key=True)', because
                    # that's assumed if it doesn't exist.
                    if att_name == 'id' and extra_params == {'primary_key': True}:
                        if field_type == 'AutoField(':
                            continue
                        elif field_type == 'IntegerField(' and not connection.features.can_introspect_autofield:
                            comment_notes.append('AutoField?')

                    # Add 'null' and 'blank', if the 'null_ok' flag was present in the
                    # table description.
                    if row[6]:  # If it's NULL...
                        if field_type == 'BooleanField(':
                            field_type = 'NullBooleanField('
                        else:
                            extra_params['blank'] = True
                            extra_params['null'] = True

                    field_desc = '%s = %s%s' % (
                        att_name,
                        # Custom fields will have a dotted path
                        '' if '.' in field_type else 'models.',
                        field_type,
                    )
                    if extra_params:
                        if not field_desc.endswith('('):
                            field_desc += ', '
                        field_desc += ', '.join(
                            '%s=%s' % (k, strip_prefix(repr(v)))
                            for k, v in extra_params.items())
                    field_desc += ')'
                    if comment_notes:
                        field_desc += '  # ' + ' '.join(comment_notes)
                    yield '    %s' % field_desc
                for meta_line in self.get_meta(table_name, constraints, column_to_field_name):
                    yield meta_line

class Command(BaseCommand):
    def handle(self, **options):
        settings.DATABASES.update(settings.DB2CHARTS_DB)
        try:
            if not os.path.exists('./db2charts_models'):
                os.mkdir('./db2charts_models')
            if not os.path.exists('./db2charts_models/__init__.py'):
                with open('./db2charts_models/__init__.py', 'w'):
                    pass
        except OSError, e:
            raise e
        for (key, value) in settings.DB2CHARTS_DB.items():
            with open('./db2charts_models/%s_models.py'%key, 'w') as f:
                inspectdb().execute(database=key, stdout=f)
                f.flush()
            