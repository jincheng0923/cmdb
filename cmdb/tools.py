# coding:utf-8
__author__ = 'ZengKing'
import paramiko
import threading
import smtplib
import logging
from django.http import Http404, HttpResponse, HttpResponseRedirect


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

lock = threading.RLock()
s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def require_login(func):
    def Islogin(*args, **kwargs):
        username = args[0].session.get('username', False)
        if not username:
            return HttpResponseRedirect('/cmdb/login')
        else:
            res = func(*args, **kwargs)
            return res

    return Islogin


def ssh_cmd(host, port, user, passwd, cmd):
    try:
        s.connect(host, 22, user, passwd)
        stdin, stdout, stderr = s.exec_command(cmd)
        cmd_result = stdout.read(), stderr.read()
        return cmd_result
    except Exception, e:
        print e


def mail_send(sender, receiver, topic, content):
    try:
        smtpserver = smtplib.SMTP('10.168.2.119', timeout=60)
        smtpserver.ehlo()
        header = 'To:' + receiver + '\n' + 'From: ' + sender + '\n' + 'Subject:' + topic + '\n'
        msg = header + '\n' + content + '\n\n'
        logging.info(sender + receiver + topic)
        smtpserver.sendmail(sender, receiver, msg)
        smtpserver.close()
    except Exception, e:
        print e