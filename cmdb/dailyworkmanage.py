# coding:utf-8
__author__ = 'ZengKing'

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from Demo.cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from tools import *


@require_login
@csrf_exempt
def save_dailywork(request):
    username = request.session.get('username')
    dates = request.POST.getlist('date')
    for i in range(len(dates)):
        daily_work = gs_dailywork(dailywork_date=request.POST.getlist('date')[i],
                                  dailywork_content=request.POST.getlist('content')[i],
                                  dailywork_type=request.POST.getlist('type')[i],
                                  dailywork_subtype=request.POST.getlist('subtype')[i],
                                  dailywork_cost=request.POST.getlist('costname')[i],
                                  dailywork_info=request.POST.getlist('info')[i],
                                  dailywork_author=username)
        daily_work.save()
    return HttpResponseRedirect('/cmdb/daily_work_list/')


@require_login
def daily_work_list(request):
    username = request.session.get('username')
    Destation_Page = int(request.GET.get('p', '1'))
    all_work_list = gs_dailywork.objects.filter(dailywork_author=username).order_by('-dailywork_date')
    olen = 25
    pages = (len(all_work_list) + olen - 1) / olen
    request.session['total'] = pages
    works = gs_dailywork.objects.filter(dailywork_author=username).order_by('-dailywork_date')[(Destation_Page - 1) * olen:Destation_Page * olen]
    Previous_Page = Destation_Page - 1
    Next_Page = Destation_Page + 1
    request.session['page'] = Destation_Page
    return render_to_response('worklist.html', locals(), context_instance=RequestContext(request))
