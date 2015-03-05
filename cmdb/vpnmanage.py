# coding:utf-8
'''
__author__ = 'ZengKing'
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Demo.cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import connection, transaction
from tools import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


@require_login
def getvpnuser(request):
    error_msg = request.GET.get('error', '')
    Destation_Page = int(request.GET.get('p', '1'))
    cursor = connection.cursor()
    sql = 'SELECT * FROM cmdb_gs_vpnvip'
    cursor.execute(sql)
    vipuser = [i[0] for i in cursor.fetchall()]
    vpnusers = gs_vpnmailinform.objects.all()
    for name in vipuser:
        vpnusers = vpnusers.exclude(username__exact=name)
    olen = 15
    pages = (len(vpnusers) + olen - 1) / olen
    users = vpnusers[(Destation_Page - 1) * olen:Destation_Page * olen]
    Previous_Page = Destation_Page - 1
    Next_Page = Destation_Page + 1
    request.session['page'] = Destation_Page
    return render_to_response('vpnuser.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def getdisablevpnuser(request):
    error_msg = request.GET.get('error', '')
    Destation_Page = int(request.GET.get('p', '1'))
    cursor = connection.cursor()
    sql = 'SELECT * FROM cmdb_gs_vpnvip'
    cursor.execute(sql)
    vipuser = [i[0] for i in cursor.fetchall()]
    user_disable = gs_vpndisableuser.objects.all()
    if len(vipuser) != 0:
        for name in vipuser:
            disableusers = user_disable.exclude(username__exact=name)
    else:
        disableusers = user_disable
    olen = 15
    pages = (len(disableusers) + olen - 1) / olen
    users = disableusers[(Destation_Page - 1) * olen:Destation_Page * olen]
    Previous_Page = Destation_Page - 1
    Next_Page = Destation_Page + 1
    request.session['page'] = Destation_Page
    return render_to_response('disablevpnuser.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def getvipvpnuser(request):
    Destation_Page = int(request.GET.get('p', '1'))
    cursor = connection.cursor()
    sql = 'SELECT * FROM cmdb_gs_vpnvip'
    cursor.execute(sql)
    vipuser = [i[0] for i in cursor.fetchall()]
    vipusers = []
    for name in vipuser:
        vipusers.append(gs_vpnuser.objects.get(username=name))
    olen = 15
    pages = (len(vipusers) + olen - 1) / olen
    users = vipusers[(Destation_Page - 1) * olen:Destation_Page * olen]
    Previous_Page = Destation_Page - 1
    Next_Page = Destation_Page + 1
    request.session['page'] = Destation_Page
    return render_to_response('vipvpnuser.html', locals(), context_instance=RequestContext(request))


@require_login
@csrf_exempt
def sendmail(request):
    p = int(request.session.get('page', '1'))
    cursor = connection.cursor()
    users = request.POST.getlist('username', '')
    for user in users:
        try:
            if request.POST.get('sendmail'):
                sql = 'update cmdb_gs_vpnmailinform SET status="Y" where username="%s"' % user
                cursor.execute(sql)
                transaction.commit_unless_managed()
                content = '    %s 的VPN账户已经30天未登录，为了加强VPN权限的管理，提高安全性，' \
                          '本月将会关闭长期不使用VPN功能的用户权限，如果您还需使用VPN，' \
                          '请本周五之前（12月12日）回复邮件，确认继续使用。' \
                          '逾期不回复，默认将关闭。' \
                          '如有任何问题请给我们发送邮件 mailto:sa@genscript.com。谢谢!' % user
                mail_send('sa@genscript.com', 'cheng.jin@genscript.com', 'VPN权限管理', content)
            else:
                sql = 'INSERT INTO  cmdb_gs_vpnvip VALUES ("%s")' % user
                cursor.execute(sql)
                transaction.commit_unless_managed()
        except:
            sql = 'update cmdb_gs_vpnmailinform SET status="E" where username="%s"' % user
            cursor.execute(sql)
            transaction.commit_unless_managed()
    cursor.close()
    return HttpResponseRedirect('/cmdb/getvpnuser/?p=%s' % p)


@require_login
@csrf_exempt
def delvipvpnuser(request):
    cursor = connection.cursor()
    users = request.POST.getlist('username', '')
    for user in users:
        sql = 'DELETE FROM cmdb_gs_vpnvip where username="%s"' % user
        cursor.execute(sql)
        transaction.commit_unless_managed()
    return HttpResponseRedirect('/cmdb/getvipvpnuser/')


@require_login
@csrf_exempt
def generatedisablevpn(request):
    error_msg = ''
    cursor = connection.cursor()
    td = datetime.datetime.now()
    ld = td - datetime.timedelta(days=30)
    starttime = request.GET.get('stdate', str(ld.strftime('%Y-%m-%d')))
    endtime = request.GET.get('eddate', str(td.strftime('%Y-%m-%d')))
    startdate = datetime.datetime.strptime(starttime, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(endtime, '%Y-%m-%d')
    files = []
    if (startdate <= enddate):
        while (startdate <= enddate):
            month = str('%02d') % startdate.month
            day = str('%02d') % startdate.day
            files.append('/log/syslog/all/' + str(startdate.year) + '/10.168.2.56/' + month + '/' + day + '.log')
            delta = datetime.timedelta(days=1)
            startdate += delta
        cmd = 'cat ' + ' '.join(files) + "|grep '[login][success]' |awk '{print $6}' |sed 's/.*]//g' |sort |uniq -d"
        rs, error = ssh_cmd('10.168.2.144', 22, 'root', '2h1av6ax', cmd)
        error_msg += error
        logrs = rs.strip().split('\n')
        a = lambda x: x != ''
        logrs = filter(a, logrs)
        print logrs
        # 生成用户文件，存于AD机器
        cmd1 = "salt nj-148-ad  cmd.run 'C:\\script\\vpnuser.ps1' shell='powershell'"
        error_msg += ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd1)[1]
        # 从AD获取用户文件
        cmd2 = "salt nj-148-ad  cp.push 'C:\\vpnlog\\vpn.txt'"
        error_msg += ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd2)[1]
        # 编码转换
        cmd3 = "dos2unix /var/cache/salt/master/minions/nj-148-ad/files/*"
        print ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd3)[1]
        # 筛选所需数据
        cmd4 = '''cat /var/cache/salt/master/minions/nj-148-ad/files/*.txt|grep TRUE |awk -F '"' '{print $3}' | awk -vOFS="|" -F ',' '{print $3,$4,$2,$5}' '''
        vpnuser = ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd4)[0].strip().split('\n')
        sql = 'TRUNCATE TABLE cmdb_gs_vpndisableuser'
        cursor.execute(sql)
        for user in vpnuser:
            name, cname, deptname, phone = user.split('|')
            name = name.split('@')[0]
            cname = 'NULL' if cname == '' else cname
            deptname = 'NULL' if deptname == '' else deptname
            phone = '0' if phone == ''else phone
            if name not in logrs:
                sql = 'insert into cmdb_gs_vpndisableuser VALUES (NULL,"%s","%s","N","%s","%s","%s","%s")' % (
                    name, str(td.strftime('%Y-%m-%d %H:%M:%S')), cname.decode('utf-8'), deptname, phone,
                    starttime + '~' + endtime + " didn't use VPN!")
                cursor.execute(sql)
                transaction.commit_unless_managed()
    else:
        error_msg = '结束时间早于开始时间，未生成数据。'
    print error_msg
    return HttpResponseRedirect('/cmdb/getdisablevpnuser/?error=%s' % error_msg)


@require_login
@csrf_exempt
def GenerateVpnInform(request):
    error_msg = ''
    cursor = connection.cursor()
    td = datetime.datetime.now()
    ld = td - datetime.timedelta(days=30)
    starttime = request.GET.get('stdate', str(ld.strftime('%Y-%m-%d')))
    endtime = request.GET.get('eddate', str(td.strftime('%Y-%m-%d')))
    startdate = datetime.datetime.strptime(starttime, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(endtime, '%Y-%m-%d')
    files = []
    if (startdate <= enddate):
        while (startdate <= enddate):
            month = str('%02d') % startdate.month
            day = str('%02d') % startdate.day
            files.append('/log/syslog/all/' + str(startdate.year) + '/10.168.2.56/' + month + '/' + day + '.log')
            delta = datetime.timedelta(days=1)
            startdate += delta
        cmd = 'cat ' + ' '.join(files) + "|grep '[login][success]' |awk '{print $6}' |sed 's/.*]//g' |sort |uniq -d"
        rs, error = ssh_cmd('10.168.2.144', 22, 'root', '2h1av6ax', cmd)
        print error
        error_msg += error
        logrs = rs.strip().split('\n')
        a = lambda x: x != ''
        logrs = filter(a, logrs)
        print len(logrs)
        # 生成用户文件，存于AD机器
        cmd1 = "salt nj-148-ad  cmd.run 'C:\\script\\vpnuser.ps1' shell='powershell'"
        error_msg += ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd1)[1]
        # 从AD获取用户文件
        cmd2 = "salt nj-148-ad  cp.push 'C:\\vpnlog\\vpn.txt'"
        error_msg += ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd2)[1]
        # 编码转换
        cmd3 = "dos2unix /var/cache/salt/master/minions/nj-148-ad/files/*"
        print ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd3)[1]
        # 筛选所需数据
        cmd4 = '''cat /var/cache/salt/master/minions/nj-148-ad/files/*.txt|grep TRUE |awk -F '"' '{print $3}' | awk -vOFS="|" -F ',' '{print $3,$4,$2,$5}' '''
        vpnuser = ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd4)[0].strip().split('\n')
        sql = 'TRUNCATE TABLE cmdb_gs_vpnuser'
        cursor.execute(sql)
        sql2 = 'TRUNCATE TABLE cmdb_gs_vpnmailinform'
        cursor.execute(sql2)
        transaction.commit_unless_managed()
        for user in vpnuser:
            name, cname, deptname, phone = user.split('|')
            name = name.split('@')[0]
            cname = 'NULL' if cname == '' else cname
            deptname = 'NULL' if deptname == '' else deptname
            phone = '0' if phone == ''else phone
            sql = 'insert into cmdb_gs_vpnuser VALUES (NULL,"%s","%s","N","%s","%s","%s","%s")' % (
                name, str(td.strftime('%Y-%m-%d %H:%M:%S')), cname.decode('utf-8'), deptname, phone,
                starttime + '~' + endtime + " didn't use VPN!")
            cursor.execute(sql)
            transaction.commit_unless_managed()
            if name not in logrs:
                sql = 'insert into cmdb_gs_vpnmailinform VALUES (NULL,"%s","%s","N","%s","%s","%s","%s")' % (
                    name, str(td.strftime('%Y-%m-%d %H:%M:%S')), cname.decode('utf-8'), deptname, phone,
                    starttime + '~' + endtime + " didn't use VPN!")
                cursor.execute(sql)
                transaction.commit_unless_managed()
    else:
        error_msg = '结束时间早于开始时间，未生成数据。'
    print error_msg
    return HttpResponseRedirect('/cmdb/getvpnuser/?error=%s' % error_msg)


@require_login
@csrf_exempt
def vpndisable(request):
    error_msg = ''
    cursor = connection.cursor()
    users = request.POST.getlist('username', '')
    for user in users:
        try:
            sql = 'UPDATE cmdb_gs_vpndisableuser SET status="Y" where username="%s"' % user
            cursor.execute(sql)
            transaction.commit_unless_managed()
            cmd = '''salt nj-148-ad cmd.run "C:\\script\\vpnclose.ps1 %s " shell='powershell' ''' % user
            info, error_msg = ssh_cmd('10.168.2.118', 22, 'root', 'qazwsx', cmd)
        except:
            sql = 'UPDATE cmdb_gs_vpndisableuser SET status="E" where username="%s"' % user
            cursor.execute(sql)
            transaction.commit_unless_managed()
    return HttpResponseRedirect('/cmdb/getdisablevpnuser/?error=%s' % error_msg)
