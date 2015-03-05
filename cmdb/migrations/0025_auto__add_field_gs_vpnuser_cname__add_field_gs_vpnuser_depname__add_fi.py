# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'gs_vpnuser.cname'
        db.add_column(u'cmdb_gs_vpnuser', 'cname',
                      self.gf('django.db.models.fields.CharField')(default='unknow', max_length=300),
                      keep_default=False)

        # Adding field 'gs_vpnuser.depname'
        db.add_column(u'cmdb_gs_vpnuser', 'depname',
                      self.gf('django.db.models.fields.CharField')(default='unknow', max_length=300),
                      keep_default=False)

        # Adding field 'gs_vpnuser.phone'
        db.add_column(u'cmdb_gs_vpnuser', 'phone',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'gs_vpnuser.cname'
        db.delete_column(u'cmdb_gs_vpnuser', 'cname')

        # Deleting field 'gs_vpnuser.depname'
        db.delete_column(u'cmdb_gs_vpnuser', 'depname')

        # Deleting field 'gs_vpnuser.phone'
        db.delete_column(u'cmdb_gs_vpnuser', 'phone')


    models = {
        u'cmdb.gs_account': {
            'Meta': {'ordering': "['account_info']", 'object_name': 'gs_account'},
            'account_info': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'previous_passwd': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'cmdb.gs_cab': {
            'Meta': {'ordering': "['cab_id']", 'object_name': 'gs_cab'},
            'cab_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cab_idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_idc']"}),
            'cab_size': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmdb.gs_crvm': {
            'Meta': {'ordering': "['nvm_name']", 'object_name': 'gs_crvm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nvm_cpu': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_createtime': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_describle': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'nvm_disk': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_jobid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_mem': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nvm_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'nvm_phy': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'nvm_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_domain': {
            'Meta': {'ordering': "['domain_name']", 'object_name': 'gs_domain'},
            'domain_expiration': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'domain_mx': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'domain_mx_priorty': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'domain_supply': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'domain_supplycontact': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'domain_supplylink': ('django.db.models.fields.URLField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmdb.gs_idc': {
            'Meta': {'ordering': "['idc_name']", 'object_name': 'gs_idc'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'idc_iprange': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'idc_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'idc_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cmdb.gs_phy': {
            'Meta': {'object_name': 'gs_phy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phy_Maintenance': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phy_describe': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phy_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phy_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phy_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_cab']"}),
            'phy_sdate': ('django.db.models.fields.DateField', [], {}),
            'pyh_warranty': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_soft': {
            'Meta': {'ordering': "['soft_name']", 'object_name': 'gs_soft'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'soft_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'soft_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'soft_source': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'soft_version': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'cmdb.gs_staff': {
            'Meta': {'ordering': "['staff_name']", 'object_name': 'gs_staff'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff_department': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'staff_id': ('django.db.models.fields.IntegerField', [], {}),
            'staff_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'staff_manage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_staff']", 'null': 'True', 'blank': 'True'}),
            'staff_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'staff_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'staff_postition': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_sub_domain': {
            'Meta': {'ordering': "['sub_domain_name']", 'object_name': 'gs_sub_domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_domain_domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_domain']"}),
            'sub_domain_ip': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sub_domain_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sub_domain_sys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cmdb.gs_system']", 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_system': {
            'Meta': {'ordering': "['sys_cname']", 'object_name': 'gs_system'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sys_cname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sys_ename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sys_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sys_manage': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'system developer'", 'symmetrical': 'False', 'to': u"orm['cmdb.gs_staff']"}),
            'sys_sa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'system administrator'", 'to': u"orm['cmdb.gs_staff']"}),
            'sys_stime': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_user': {
            'Meta': {'ordering': "['user_ip']", 'object_name': 'gs_user'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_device': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_vm']"}),
            'user_login': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_vm': {
            'Meta': {'ordering': "['vm_ip']", 'object_name': 'gs_vm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vm_cpu': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vm_describe': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vm_disk': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vm_hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'vm_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vm_ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vm_manager': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vm_mem': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vm_os': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'os_name'", 'to': u"orm['cmdb.gs_soft']"}),
            'vm_phy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_phy']", 'null': 'True', 'blank': 'True'}),
            'vm_sdate': ('django.db.models.fields.DateField', [], {}),
            'vm_soft': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'install_soft'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cmdb.gs_soft']"}),
            'vm_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_system']", 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_vpnuser': {
            'Meta': {'ordering': "['username']", 'object_name': 'gs_vpnuser'},
            'cname': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'depname': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'update': ('django.db.models.fields.DateField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'cmdb.gs_work': {
            'Meta': {'ordering': "['work_content']", 'object_name': 'gs_work'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_class': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'work_content': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'work_date': ('django.db.models.fields.DateField', [], {}),
            'work_num': ('django.db.models.fields.IntegerField', [], {}),
            'work_total': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['cmdb']