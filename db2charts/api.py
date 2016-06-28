# -*- coding: utf-8 -*-
# author: Alfred

from db2charts import settings
from db2charts.analysis import AnalysisManage, AnalysisCreate, AnalysisReport
from db2charts.models import *
from db2charts.utils.basic import *
from db2charts.utils.datatables import makeDataTable
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from tastypie.serializers import Serializer
import datetime
import json
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
    model = getattr(AnalysisManage().modules['analysis_db_artenterdefault'], model)
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


def analysis_model_available(request):
    info = {
        'data':AnalysisManage().get_availables()
    }
    return JsonResponse(info, safe=False)



def analysis_model_all(request):
    info = {
        'data': AnalysisManage().get_candidates()
    }
    return JsonCusResponse(info, safe=False)


def analysis_manage_submit(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_name, translated_model_name, cols = get_post_args(
        request, 'model_name', 'translated_model_name', 'cols')
    try:
        AnalysisManage().add_available(model_name, translated_model_name, cols)
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid params ' + e.message
    return JsonResponse(info)


def analysis_manage_update(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_name, translated_model_name, cols = get_post_args(
        request, 'model_name', 'translated_model_name', 'cols')
    try:
        AnalysisManage().update_available(model_name, translated_model_name, cols)
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid params ' + e.message
    return JsonResponse(info)


def analysis_manage_delete(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_name, = get_post_args(request, 'model_name')
    try:
        AnalysisManage().delete_available(model_name)
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid model_name ' + e.message
    return JsonResponse(info)


def analysis_manage_active(request):
    info = {
        'status': 0,
        'message': 'success',
    }
    model_name, active = get_post_args(request, 'model_name', 'active')
    try:
        AnalysisManage().set_active(model_name, bool(active))
    except Exception, e:
        info['status'] = 1
        info['message'] = 'invalid model_name ' + e.message
    return JsonResponse(info)


def analysis_create_dbs(request):
    return JsonResponse(AnalysisCreate().get_dbs(), safe=False)

def analysis_create_tables(request):
    db, = get_get_args(request, 'db')
    return JsonResponse(AnalysisCreate().get_available_tables(db), safe=False)

def analysis_create_tablecols(request):
    model_name, = get_get_args(request, 'model_name')
    info = {
        'data': AnalysisCreate().get_translated_cols(model_name)
    }
    return JsonCusResponse(info, safe=False)


def analysis_create_preview(request):
    model_full_name, xAxis_group, yAxis_group = get_get_args(request, 'model_name', 'xAxis', 'yAxis')
    if not model_full_name or not xAxis_group or not yAxis_group:
        return JsonCusResponse({}, safe=False)
    model_full_name = model_full_name.split('.')
    db_name = model_full_name[0]
    model_name = model_full_name[1]
    xAxis_group = xAxis_group.split(',')
    yAxis_group = yAxis_group.split(',')
    yAxis = yAxis_group[0].split('.')[-1]
    info = AnalysisCreate().fetch_preview_data(db_name, model_name, xAxis_group, yAxis)
    return JsonCusResponse(info, safe=False)


def analysis_create_submit(request):
    chartOptions, = get_post_args(request, 'options')
    report_id = AnalysisCreate().save_report(chartOptions)
    return JsonCusResponse({'result':'success', 'report_id': report_id}, safe=False)


def analysis_report(request):
    report_id, = get_get_args(request, 'report_id')
    return JsonCusResponse(AnalysisReport(report_id).get_report_data(), safe=False)