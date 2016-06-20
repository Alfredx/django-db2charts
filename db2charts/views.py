# -*- coding: utf-8 -*-
# author: Alfred

from django.shortcuts import render_to_response
from django.template import RequestContext
from db2charts.utils import *


def datatable(request):
    ctx = get_basic_ctx(request)
    return render_to_response('datatable.html', RequestContext(request, ctx))


def analysis_manage(request):
	ctx = get_basic_ctx(request)
	return render_to_response('analysis_manage.html', RequestContext(request, ctx))


def analysis_create(request):
	ctx = get_basic_ctx(request)
	f = open('db2charts/templates/analysis_create.vue')
	ctx['analysis_create_vue_html'] = f.read()
	f.close()
	return render_to_response('analysis_create.html', RequestContext(request, ctx))

def analysis_report(request):
    ctx = get_basic_ctx(request)
    f = open('db2charts/templates/analysis_report.vue')
    ctx['analysis_report_vue_html'] = f.read()
    f.close()
    return render_to_response('analysis_report.html', RequestContext(request, ctx))