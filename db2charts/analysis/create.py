# -*- coding: utf-8 -*-
# author: Alfred

from db2charts.analysis.base import AnalysisBase
from db2charts.models import *
import json


class AnalysisCreate(AnalysisBase):
    record_count_col_name = 'recordCount'
    record_count_translated_name = '记录数'

    def __init__(self):
        super(AnalysisCreate, self).__init__()

    def get_available_tables(self, db):
        aams = AvailableAnalysisModel.objects.filter(db_name=db, active=True)
        return [{'model_name':m.model_name, 'translated_name':m.translated_name} for m in aams]

    def get_translated_cols(self, model_name):
        aam = AvailableAnalysisModel.objects.filter(
            model_name=model_name, active=True).first()
        cols = [{
            'col_name': self.record_count_col_name,
            'translated_col_name': self.record_count_translated_name
        }]
        if aam:
            cols += aam.translated_cols
        return cols

    def fetch_preview_data(self, db_name, model_name, xAxis_group, yAxis):
        result = {
            'serie_name': [],
            'data': {
                'xAxis': [],
                'yAxis': [],
            },
            'count': 0,
        }
        module = self.modules[db_name]
        model_class = getattr(module, model_name)
        if not len(xAxis_group) or not yAxis:
            return result
        for xAxis in xAxis_group:
            dataSet = {
                'xAxis': [],
                'yAxis': [],
            }
            xAxis = xAxis.split('.')[-1]
            try:
                all_objects = model_class.objects.all()
                data = {}
                for obj in all_objects:
                    t = getattr(obj, xAxis)
                    if not data.has_key(t):
                        data[t] = getattr(obj, yAxis) if yAxis != self.record_count_col_name else 1
                    else:
                        data[t] += getattr(obj, yAxis) if yAxis != self.record_count_col_name else 1
                for (key, value) in sorted(data.items(), key=lambda x: x[0]):
                    dataSet['xAxis'].append(key)
                    dataSet['yAxis'].append(value)
            except Exception, e:
                raise e
            result['data']['xAxis'].append(dataSet['xAxis'])
            result['data']['yAxis'].append(dataSet['yAxis'])
            result['serie_name'].append(xAxis)
            result['count'] += 1
        return result

    def save_report(self, options):
        report = AnalysisReport()
        report.related_models = options['selectedTable']
        report.options = options
        report.save()
        return True
