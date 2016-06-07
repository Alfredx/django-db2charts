# -*- coding: utf-8 -*-
# author: Alfred

from django.db import models
import django

__all__ = [
    "BaseStatisticsColumn",
    "AvailableAnalysisModel",
    "AnalysisReport",
]

class BaseStatisticsColumn(models.Model):
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        abstract = True


class AvailableAnalysisModel(BaseStatisticsColumn):
    model_name = models.CharField(max_length=128, default="")
    translated_name = models.CharField(max_length=128, default="")
    active = models.BooleanField(default=True)
    translated_cols = models.TextField(default="")


class AnalysisReport(BaseStatisticsColumn):
    open_state_choice = ((0, 'private'), (1, 'public'))
    related_models = models.TextField(default="")
    conditions = models.TextField(default="")
    report_name = models.CharField(max_length=128, default="自定义报表")
    open_state = models.IntegerField(choices=open_state_choice, default=0)
    creator_name = models.CharField(max_length=128, default="")
    