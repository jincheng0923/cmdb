# coding:utf-8
__author__ = 'ZengKing'
from django.contrib import auth
import urllib, urllib2, json
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Demo.cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.db import connection, transaction
import uuid
from tools import *
from optionclass import *


@csrf_exempt
def login_view(request):
    cursor = connection.cursor()
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    url = "http://restapi.genscript.com/b0026_ldap_auth"
    uid = uuid.uuid1()
    data = '''{
                "uid": "%s",
                "cmd": "",
                "data": {"user_name":"%s" ,
                         "password": "%s"
                }
            }
    ''' % (uid, username, password)
    data = {"data": data}
    data = urllib.urlencode(data)
    P_request = urllib2.Request(url, data)
    P_respose = urllib2.urlopen(P_request)
    return_data = P_respose.read()
    return_data = json.loads(return_data)
    if return_data['result']['return_code'] == "0":
        request.session["username"] = username
        gmods = GrandFatherMods('Tmod')
        sql = "SELECT a.mods,b.mod_father,b.mod_cname,b.mod_url,c.mod_cname from cmdb_func_manage a left join" \
              " cmdb_mods b on a.mods=b.mod_name  LEFT JOIN cmdb_mods  c on b.mod_father=c.mod_name" \
              "  WHERE a.username='%s' ORDER BY c.mod_order " % username
        cursor.execute(sql)
        transaction.commit_unless_managed()
        rs = cursor.fetchall()
        for info in rs:
            son_mod = SonMods(info[0], info[2], info[3])
            father_mod = FatherMods(info[4], son_mod)
            gmods.add_father_mod(father_mod)
        request.session['lmodes'] = gmods
        return HttpResponseRedirect("/cmdb/home")
    elif return_data['result']['return_code'] == "2":
        return render_to_response("login.html", {"msg": "用户名密码错误！"})
    else:
        return render_to_response("login.html", {"msg": "系统故障，请稍后重试！"})


@csrf_exempt
def logout(request):
    del request.session['username']
    auth.logout(request)
    return HttpResponseRedirect('/cmdb/login')


@require_login
def userfunc(request):
    cursor = connection.cursor()
    sql = 'SELECT a.mod_name,a.mod_cname,b.mod_cname,"False" from cmdb_mods a LEFT JOIN cmdb_mods b ON a.mod_father=b.mod_name WHERE a.mod_level=1'
    cursor.execute(sql)
    rs = cursor.fetchall()
    return render_to_response("user_func.html", locals(), context_instance=RequestContext(request))


@require_login
def updatefunc(request):
    cursor = connection.cursor()
    if request.POST.get('usercheck'):
        username=request.POST.get('username')
        sql="SELECT a.mod_name,a.mod_cname,b.mod_cname, IF(a.mod_name in (SELECT mods FROM cmdb_func_manage WHERE username='%s'),'True','False') from cmdb_mods a LEFT JOIN cmdb_mods b ON a.mod_father=b.mod_name WHERE a.mod_level=1" %username
        cursor.execute(sql)
        rs=cursor.fetchall()
        return render_to_response("user_func.html", locals(), context_instance=RequestContext(request))
    else:
        username = request.POST.get('username', '')
        if username:
            mods = request.POST.getlist('privative', '')
        sql="DELETE from cmdb_func_manage WHERE username='%s'" %username
        cursor.execute(sql)
        transaction.commit_unless_managed()
        for mod in mods:
            sql="INSERT INTO cmdb_func_manage VALUES('%s','%s')" %(username,mod)
            cursor.execute(sql)
        transaction.commit_unless_managed()
        return HttpResponseRedirect("/cmdb/userfunc")