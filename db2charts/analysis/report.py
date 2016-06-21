# -*- coding: utf-8 -*-
# author: Alfred

from db2charts.analysis.base import AnalysisBase
from db2charts.models import *

class AnalysisReport(AnalysisBase):
    record_count_col_name = 'recordCount'
    record_count_translated_name = '记录数'

    def __init__(self, id):
        super(AnalysisReport, self).__init__()
        self.id = id
        self.report = AnalysisReportData.objects.get(id=id)
        self.options = self.report.options
        self.module = self.modules[self.options['db_name']]
        self.model = getattr(self.module, self.options['model_name'].split('.')[-1])

    def get_chart_data(self):
        xAxis = self.options['chart_options']['xAxis']
        yAxis = self.options['chart_options']['yAxis']
        result = {
            'legend': self.report.report_name,
            'serie_name': [],
            'data': {
                'xAxis': [],
                'yAxis': [],
            },
            'count': 0,
        }
        y = yAxis[0]['col_name'].split('.')[-1]
        for x in xAxis:
            x = x['col_name'].split('.')[-1]
            dataSet = {
                'xAxis': [],
                'yAxis': [],
            }
            try:
                all_objects = self.model.objects.all()
                data = {}
                for obj in all_objects:
                    t = getattr(obj, x)
                    if not data.has_key(t):
                        data[t] = getattr(obj, y) if y != self.record_count_col_name else 1
                    else:
                        data[t] += getattr(obj, y) if y != self.record_count_col_name else 1
                for (key, value) in sorted(data.items(), key=lambda x: x[0]):
                    dataSet['xAxis'].append(key)
                    dataSet['yAxis'].append(value)
            except Exception, e:
                raise e
            result['data']['xAxis'].append(dataSet['xAxis'])
            result['data']['yAxis'].append(dataSet['yAxis'])
            result['serie_name'].append(x)
            result['count'] += 1
        return result

    def get_table_data(self):
        # draw = table_params['draw']
        # start = table_params['start']
        # length = table_params['length']
        # search = table_params['search']['value']
        # order_by = table_params['columns'][table_params['order']['0']['column']]['data']
        # order_dir = '' if table_params['order']['0']['dir'] == 'asc' else '-'
        # objects = None
        # data = {
        #     'draw': draw,
        #     'recordsTotal': models.objects.all().count()
        # }
        result = {
            'table_data': self.model.objects.all(),
            'table_cols': self.get_columns(self.options['db_name'], self.options['model_name'].split('.')[-1]),
        }
        return result

    def get_report_data(self):
        result = {}
        result.update(self.get_chart_data())
        result.update(self.get_table_data())
        return result