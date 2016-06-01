# -*- coding: utf-8 -*-
# author: Alfred

from django.template.context_processors import csrf
from django.utils import timezone
import datetime
import json

def get_basic_ctx(request):
    ctx = {}
    ctx['csrf_token'] = csrf(request).get('csrf_token')
    return ctx


def get_today_zero():
    now = timezone.make_naive(timezone.now())
    delta = datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second)
    today_zero = timezone.now() - delta
    return today_zero


def get_month_zero():
    now = timezone.make_naive(timezone.now())
    delta = datetime.timedelta(
        days=now.day - 1, hours=now.hour, minutes=now.minute, seconds=now.second)
    return timezone.now() - delta


# 获取普通view中post方法的参数公共方法
def get_post_args(request, *args):
    # 后台默认接收application/json数据
    try:
        args_info = json.loads(request.body)
    except Exception, e:
        args_info = {}

    return [request.POST.get(item, None) or args_info.get(item, None) for item in args]


# 获取view中get方法的参数公共方法
def get_get_args(request, *args):
    get_args = []
    for item in args:
        if item == 'limit':
            item_value = int(request.GET.get(item, LIMIT))
        elif item == 'offset':
            item_value = int(request.GET.get(item, OFFSET))
        else:
            item_value = request.GET.get(item, None)

        get_args.append(item_value)

    return get_args