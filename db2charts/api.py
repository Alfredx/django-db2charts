# -*- coding: utf-8 -*-
# author: Alfred

from db2charts.db_models import models as analysis_models
from db2charts.models import *
from db2charts.utils.basic import *
from db2charts.utils.datatables import makeDataTable
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
import datetime
import logging
import sys
logger = logging.getLogger(__name__)
DEFAULT_TIME_SPAN_COUNTS = 12


def calculate_timespan(start_time, end_time, timespan=None):
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    if not timespan:
        counts = DEFAULT_TIME_SPAN_COUNTS
        timespan = (end_time - start_time) / DEFAULT_TIME_SPAN_COUNTS
    else:
        counts = int(((end_time - start_time).total_seconds() +
                      60) / timespan.total_seconds())
    xAxisSpan = {'timespan': timespan,
                 'counts': counts,
                 'set': [start_time + i * timespan for i in range(counts)]}
    return xAxisSpan


def arrange_data(xAxisSpan, query_set):
    span_counts = xAxisSpan['counts']
    result = [0 for i in range(span_counts)]
    start_time = xAxisSpan['set'][0]
    timespan = xAxisSpan['timespan']
    for entry in query_set:
        if hasattr(entry, 'create_date'):
            date = entry.create_date
        elif hasattr(entry, 'date_joined'):
            date = entry.date_joined
        else:
            raise Exception('can not resolve any date field')
        actual_seconds = (timezone.make_naive(
            date) - start_time).total_seconds()
        span_seconds = timespan.total_seconds()
        slot = int(actual_seconds / span_seconds)
        if slot < span_counts:
            if hasattr(entry, 'count'):
                if hasattr(entry, 'repeat_add'):
                    if entry.repeat_add:
                        result[slot] += entry.count
                    else:
                        result[slot] = entry.count
                else:
                    result[slot] += entry.count
            else:
                result[slot] += 1
    return result


def xAxis_timeformat(date, no_hms=False):
    format_str = '%Y-%m-%d' if no_hms else '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strftime(date, format_str)


def get_entry_counts_by_time(start_time, end_time, timespan, ModelObjects=None, entrys=None):
    no_hms = False
    if timespan != u'0.0.0':
        # timespan format WEEKS.DAYS.HOURS
        timespan = timespan.split('.')
        timespan = [int(i) for i in timespan]
        timespan = datetime.timedelta(weeks=timespan[0],
                                      days=timespan[1],
                                      hours=timespan[2])
        if timespan.days > 0:
            no_hms = True
    else:
        timespan = None
    xAxisSpan = calculate_timespan(start_time, end_time, timespan)
    if ModelObjects is None and entrys is None:
        raise Exception('ModelObjects and entrys can not be both None')
    if ModelObjects:
        entrys = ModelObjects.filter(
            create_date__gte=start_time, create_date__lte=end_time)
    info = {
        'yAxis': arrange_data(xAxisSpan, entrys),
        'xAxis': [xAxis_timeformat(xAxisSpan['set'][i], no_hms).replace(' ', '\n') for i in range(xAxisSpan['counts'])],
    }
    return info


def datatable_data(request):
    dataTable = makeDataTable(request.GET)
    draw = dataTable['draw']
    start = dataTable['start']
    length = dataTable['length']
    search = dataTable['search']['value']
    order_by = dataTable['columns'][dataTable['order']['0']['column']]['data']
    order_dir = '' if dataTable['order']['0']['dir'] == 'asc' else '-'

    start_time, end_time, timespan, model = get_get_args(
        request, 'start_time', 'end_time', 'timespan', 'model')
    model = getattr(analysis_models, model)
    recordsTotal = model.objects.all().count()
    objects = None
    if search:
        objects = model.objects.filter(
            name__contains=search).order_by(order_dir + order_by)
    else:
        objects = model.objects.all().order_by(order_dir + order_by)
    info = {
        'draw': draw,
        'recordsTotal': recordsTotal,
        'recordsFiltered': objects.count(),
        'data': [{f.attname: getattr(x, f.attname) for f in x._meta.concrete_fields} for x in objects[start:start + length]],
        'chart': {
            'legend': model.__name__,
            'serie_name': model.__name__,
            'data': get_entry_counts_by_time(start_time, end_time, timespan, ModelObjects=objects),
        }
    }
    return JsonResponse(info, safe=False)

import sys
import json


def analysis_model_available(request):
    availableModels = AvailableAnalysisModel.objects.all()
    info = {'data': [{'model_name': x.model_name, 'translated_name': x.translated_name,
                      'active': x.active, 'cols': json.loads(x.translated_cols)} for x in availableModels]}
    return JsonResponse(info, safe=False)


from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from tastypie.serializers import Serializer


class JsonCusResponse(HttpResponse):
    """
    为了解决在views中使用django.http.jsonResponse返回数据的时候，时间返回没有转成本地时间，从而导致前台时间显示错误问题。
    这里重写jsonResponse，借用tastypie的序列化对象，对python数据做预处理（主要是对datetime），解决时间问题
    """
    serializer = Serializer()
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = self.serializer.to_simple(data, None)
        data = json.dumps(data, cls=encoder)
        super(JsonCusResponse, self).__init__(content=data, **kwargs)


def analysis_model_all(request):
    info = {
        'data': []
    }
    availableModels = AvailableAnalysisModel.objects.filter(active=True)
    availableModels = [m.model_name for m in availableModels]
    for name in dir(analysis_models):
        try:
            if issubclass(getattr(analysis_models, name), models.Model):
                info['data'].append({'model_name': 'db_models.%s' % name, 'active': True if 'db_models.%s' % name in availableModels else False, 'cols': [
                                    x for x in getattr(analysis_models, name)._meta.concrete_fields]})
        except:
            pass
    return JsonCusResponse(info, safe=False)


def analysis_manage_submit(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_full_name, translated_model_name, cols = get_post_args(
        request, 'model_name', 'translated_model_name', 'cols')
    try:
        aam = AvailableAnalysisModel()
        aam.model_name = model_full_name
        aam.translated_name = translated_model_name
        aam.active = True
        aam.translated_cols = json.dumps(cols)
        aam.save()
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid params ' + e.message
    return JsonResponse(info)


def analysis_manage_update(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_full_name, translated_model_name, cols = get_post_args(
        request, 'model_name', 'translated_model_name', 'cols')
    try:
        aam = AvailableAnalysisModel.objects.filter(
            model_name=model_full_name).first()
        if aam:
            aam.translated_name = translated_model_name
            aam.translated_cols = json.dumps(cols)
            aam.save()
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid params ' + e.message
    return JsonResponse(info)


def analysis_manage_delete(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_full_name, = get_post_args(request, 'model_name')
    try:
        aam = AvailableAnalysisModel.objects.filter(
            model_name=model_full_name).first()
        if aam:
            aam.delete()
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid model_name ' + e.message
    return JsonResponse(info)


def analysis_manage_active(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_full_name, active = get_post_args(request, 'model_name', 'active')
    try:
        aam = AvailableAnalysisModel.objects.filter(
            model_name=model_full_name).first()
        if aam:
            aam.active = bool(active)
            aam.save()
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid model_name ' + e.message
    return JsonResponse(info)


def analysis_create_tablecols(request):
    info = {}
    model_full_name, = get_get_args(request, 'model_name')
    aam = AvailableAnalysisModel.objects.filter(model_name=model_full_name, active=True).first()
    if aam:
        info['data'] = json.loads(aam.translated_cols)
        info['data'].insert(0, {'col_name':'recordCount','translated_col_name':'记录数'})
    return JsonCusResponse(info, safe=False)


moduleRouter = {
    analysis_models.__package__.split('.')[-1]: analysis_models,
}


def analysis_model_data(request):
    info = {
        'legend': 'legend',
        'serie_name': 'NAME',
        'data': {
            'xAxis': [],
            'yAxis': [],
        },
    }
    model_full_name, xAxis, yAxis = get_get_args(request, 'model_name', 'type', 'data')
    xAxis = xAxis.split('.')[-1]
    model_full_name = model_full_name.split('.')
    module = moduleRouter[model_full_name[0]]
    model_name = model_full_name[1]
    try:
        model = getattr(module, model_name)
        allObjects = model.objects.all()
        result = {}
        for obj in allObjects:
            t = getattr(obj, xAxis)
            if not result.has_key(t):
                result[t] = getattr(obj, yAxis) if yAxis != 'recordCount' else 1
            else:
                result[t] += getattr(obj, yAxis) if yAxis != 'recordCount' else 1
        for (key, value) in sorted(result.items(), key=lambda x:x[0]):
            info['data']['xAxis'].append(key)
            info['data']['yAxis'].append(value)
    except Exception, e:
        logger.error(e)
    return JsonCusResponse(info, safe=False)