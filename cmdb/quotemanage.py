# coding:utf-8
'''
__author__ = 'ZengKing'
'''
from django.contrib import auth
import urllib
import urllib2
import json
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Demo.cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.db import connection, transaction
import uuid
from tools import *
from optionclass import *
import csv
import time


@require_login
@csrf_exempt
def bj(request):
    dates = request.POST.getlist('date')
    for i in range(len(dates)):
        work = gs_work(work_date=request.POST.getlist('date')[i], work_content=request.POST.getlist('content')[i],
                       work_class=request.POST.getlist('lb')[i], work_num=request.POST.getlist('num')[i],
                       work_total=request.POST.getlist('total')[i])
        work.save()
    return HttpResponseRedirect('/cmdb/bjlist/')


@require_login
def bjlist(request):
    lp = request.session.get('page', 1)
    abj = gs_work.objects.order_by('-work_date')
    olen = 25
    pages = (len(abj) + olen - 1) / olen
    action = request.GET.get('action', '')
    request.session['total'] = pages
    if action == 'next' and lp < pages:
        bjs = gs_work.objects.order_by('-work_date')[(lp - 1) * olen:lp * olen]
        request.session['page'] = lp + 1
    elif action == 'previous' and lp > 1:
        bjs = gs_work.objects.order_by('-work_date')[(lp - 2) * olen:(lp - 1) * olen]
        request.session['page'] = lp - 1
    else:
        bjs = gs_work.objects.order_by('-work_date')[0:olen]
        request.session['page'] = 1
    return render_to_response('bjlist.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def outrecords(request):
    td = datetime.datetime.now()
    ld = td - datetime.timedelta(days=30)
    starttime = request.GET.get('stdate', str(ld.strftime('%Y-%m-%d')))
    endtime = request.GET.get('eddate', str(td.strftime('%Y-%m-%d')))
    response = HttpResponse(mimetype='text/csv')
    month = time.strftime('%m', time.localtime(time.time()))
    filename = month + '月份服务费.csv'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response)
    infos = gs_work.objects.getwork(starttime, endtime)
    writer.writerow(['时间'.encode('gb2312'), '内容'.encode('gb2312'), '种类'.encode('gb2312'), '数目'.encode('gb2312'),
                     '总价'.encode('gb2312')])
    for info in infos:
        writer.writerow([info[1], info[2].encode('gb2312'), info[3], info[4], info[5]])
    return response


@require_login
@csrf_exempt
def generatequote(request):
    cursor = connection.cursor()
    td = datetime.datetime.now()
    ld = td - datetime.timedelta(days=30)
    author = request.session.get('username')
    starttime = request.POST.get('stdate', str(ld.strftime('%Y-%m-%d')))
    endtime = request.POST.get('eddate', str(td.strftime('%Y-%m-%d')))
    sql = 'select CAST(dailywork_date as CHAR),dailywork_content from cmdb_gs_dailywork ' \
          'where dailywork_date > "%s" and dailywork_date < "%s" and dailywork_author="%s" ' \
          % (starttime, endtime, author)
    cursor.execute(sql)
    quotes = cursor.fetchall()
    return render_to_response('generatequote.html', locals(), context_instance=RequestContext(request))
