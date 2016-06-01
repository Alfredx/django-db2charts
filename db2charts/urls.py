# -*- coding: utf-8 -*-
# author: Alfred

from django.conf.urls import url
from db2charts import views
from db2charts import api

urlpatterns = [
    url(r'^datatable/$', views.datatable),
    url(r'^api/datatable/data/$', api.datatable_data),
    # url(r'^analysis/report/(?P<report_id>[0-9]+)$', ds_analysis_report),
    # url(r'^analysis/create/$', ds_analysis_create),
    url(r'^analysis/manage/$', views.analysis_manage),
    url(r'^analysis/create/$', views.analysis_create),

    url(r'^api/analysis/manage/available/$', api.analysis_model_available),
    url(r'^api/analysis/manage/all/$', api.analysis_model_all),
    url(r'^api/analysis/manage/submit/$', api.analysis_manage_submit),
    url(r'^api/analysis/manage/update/$', api.analysis_manage_update),
    url(r'^api/analysis/manage/delete/$', api.analysis_manage_delete),
    url(r'^api/analysis/manage/active/$', api.analysis_manage_active),
    url(r'^api/analysis/create/tablecols/$', api.analysis_create_tablecols),
    url(r'^api/analysis/modeldata/$', api.analysis_model_data),
]