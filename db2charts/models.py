# -*- coding: utf-8 -*-
# author: Alfred

from django.db import models
import django
import json

__all__ = [
    "BaseStatisticsColumn",
    "AvailableAnalysisModel",
    "AnalysisReportData",
]

class BaseStatisticsColumn(models.Model):
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        abstract = True


class AvailableAnalysisModel(BaseStatisticsColumn):
    db_name = models.CharField(max_length=128, default="")
    model_name = models.CharField(max_length=128, default="")
    translated_name = models.CharField(max_length=128, default="")
    active = models.BooleanField(default=True)
    _translated_cols = models.TextField(default="")

    @property
    def translated_cols(self):
        return json.loads(self._translated_cols)

    @translated_cols.setter
    def translated_cols(self, cols):
        self._translated_cols = jsom.dumps(cols)
    


class AnalysisReportData(BaseStatisticsColumn):
    open_state_choice = ((0, 'private'), (1, 'public'))
    related_models = models.TextField(default="")
    conditions = models.TextField(default="")
    report_name = models.CharField(max_length=128, default="自定义报表")
    open_state = models.IntegerField(choices=open_state_choice, default=0)
    creator_name = models.CharField(max_length=128, default="")

    @property
    def options(self):
        return json.loads(self.conditions)

    @options.setter
    def options(self, options):
        self.conditions = json.dumps(options)
    
    
    