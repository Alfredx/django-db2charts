# -*- coding: utf-8 -*-
# author: Alfred

import re

def makeDataTable(args):
    """
    dataTable = {
        'draw': 0,
        'start': 0,
        'length': 0,
        'search': {
            'value': '',
            'regex': False,
        },
        'order': {
            0: {'column':0, 'dir':''},
        },
        'columns': {
            0: {
                'searchable': False,
                'orderable': False,
                'data': '',
                'name': '',
                'search': {
                    'value': '',
                    'regex': False
                }
            },

        },
    }
    """
    pattern = re.compile(
        r'(?P<group>(draw|start|length|search|order|columns))($|\[(?P<a1>\w+?)\])($|\[(?P<a2>\w+?)\])($|\[(?P<a3>\w+)\])')
    d = {
        'draw': 0,
        'start': 0,
        'length': 0,
        'search': {
            'value': '',
            'regex': False,
        },
        'order': {},
        'columns': {},
    }
    for item in args:
        match = pattern.match(item)
        if not match:
            continue
        gorupdict = match.groupdict()
        item_val = args.get(item, '')
        if gorupdict['group'] in ['draw', 'start', 'length']:
            d[gorupdict['group']] = int(item_val)
        elif gorupdict['group'] == 'search':
            d['search'][gorupdict['a1']] = item_val
        elif gorupdict['group'] == 'order':
            index, order_dir = gorupdict['a1'], gorupdict['a2']
            if d['order'].has_key(index):
                d['order'][index][order_dir] = item_val
            else:
                d['order'][index] = {
                    order_dir: item_val
                }
        elif gorupdict['group'] == 'columns':
            index, col_key, col_search_key = gorupdict[
                'a1'], gorupdict['a2'], gorupdict['a3']
            if d['columns'].has_key(index):
                if col_key == 'search':
                    if d['columns'][index].has_key('search'):
                        d['columns'][index]['search'][
                            col_search_key] = item_val
                    else:
                        d['columns'][index]['search'] = {
                            col_search_key: item_val
                        }
                else:
                    d['columns'][index][col_key] = item_val
            else:
                if col_key == 'search':
                    d['columns'][index] = {
                        'search': {col_search_key: item_val}
                    }
                else:
                    d['columns'][index] = {
                        col_key: item_val
                    }
    return d