# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render_to_response
from Demo.cmdb.models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import os
from django.db.models import Q
from django.contrib import auth
from django.template import RequestContext
import csv, time
from django.db import connection, transaction
import string
from random import choice
import logging
from tools import *
import sys
import urllib, urllib2, json
from django.conf.urls import patterns, include, url

from vpnmanage import *
from usermanage import *
from dailyworkmanage import *
from quotemanage import *

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/cmdb.log',
                    filemode='a')

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

chars = string.letters + string.digits


@csrf_exempt
def loginindex(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))


@require_login
def foobar_view(request, template_name):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



@require_login
@csrf_exempt
def zhsearch(request):
    search_info = request.POST.get('searchinfo', "null")
    print search_info
    if not request.POST.get('isipfilter'):
        filter = 'true'
    else:
        filter = request.POST['isipfilter']
    if filter == 'true' and search_info:
        users = gs_user.objects.filter(Q(user_ip__vm_ip__icontains=search_info))[:10]
        vms = gs_vm.objects.filter(Q(vm_ip__icontains=search_info))[:10]
        sub_domains = gs_sub_domain.objects.filter(Q(sub_domain_ip__icontains=search_info))[0:10]
    elif filter == 'false' and search_info:
        users = gs_user.objects.filter(Q(user_info__icontains=search_info) | Q(user_name__icontains=search_info))[:10]
        vms = gs_vm.objects.filter(Q(vm_info__icontains=search_info) | Q(vm_soft__soft_name__icontains=search_info) | Q(
            vm_system__sys_ename__icontains=search_info))[:10]
        domains = gs_domain.objects.filter(
            Q(domain_name__icontains=search_info) | Q(domain_supply__icontains=search_info))[:10]
        sub_domains = gs_sub_domain.objects.filter(
            Q(sub_domain_name__icontains=search_info) | Q(sub_domain_domain__domain_name=search_info))[:10]
    return render_to_response('searchindex.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def crvm(request):
    phy = request.POST.get('phy')
    hostname = request.POST.get('hostname')
    cpu = int(request.POST.get('cpu')[0:request.POST.get('cpu').find('C')])
    mem = int(request.POST.get('mem')[0:request.POST.get('mem').find('G')])
    disk = int(request.POST.get('disk'))
    os = request.POST.get('os')
    print hostname, cpu, mem, disk, os
    if phy and hostname and cpu and mem and disk and os:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.168.2.159", 22, "root", "123.com")
        stdin, stdout, stderr = ssh.exec_command("nohup sh /opt/0923.sh &")
        rs = stdout.readlines()
        pid = rs[1]
        ssh.close()
        return render_to_response("newvmrs.html", locals())
    else:
        return HttpResponseRedirect('/cmdb/newvm/')


@require_login
@csrf_exempt
def register(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    print "success!"
    return render_to_response('info.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def randompasswd(request):
    bit = request.POST.get('bit')
    num = request.POST.get('num')
    if bit and num:
        passwdlist = [''.join([choice(chars) for i in range(int(bit))]) for i in range(int(num))]
    return render_to_response('randowpasswd.html', locals(), context_instance=RequestContext(request))





@require_login
@csrf_exempt
def ipaviable(request):
    cursor = connection.cursor()
    sql = 'select * from cmdb_aviip'
    cursor.execute(sql)
    rs = cursor.fetchall()
    print rs
    return render_to_response('aviableiplist.html', locals(), context_instance=RequestContext(request))


