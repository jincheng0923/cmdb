# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'gs_staff'
        db.create_table(u'cmdb_gs_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff_id', self.gf('django.db.models.fields.IntegerField')()),
            ('staff_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('staff_phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('staff_postition', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('staff_department', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('staff_manage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmdb.gs_staff'], null=True, blank=True)),
            ('staff_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_staff'])

        # Adding model 'gs_idc'
        db.create_table(u'cmdb_gs_idc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idc_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('idc_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('idc_location', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'cmdb', ['gs_idc'])

        # Adding model 'gs_cab'
        db.create_table(u'cmdb_gs_cab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cab_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cab_idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmdb.gs_idc'])),
            ('cab_size', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_cab'])

        # Adding model 'gs_system'
        db.create_table(u'cmdb_gs_system', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sys_cname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sys_ename', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sys_sa', self.gf('django.db.models.fields.related.ForeignKey')(related_name='system administrator', to=orm['cmdb.gs_staff'])),
            ('sys_stime', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sys_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_system'])

        # Adding M2M table for field sys_manage on 'gs_system'
        m2m_table_name = db.shorten_name(u'cmdb_gs_system_sys_manage')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gs_system', models.ForeignKey(orm[u'cmdb.gs_system'], null=False)),
            ('gs_staff', models.ForeignKey(orm[u'cmdb.gs_staff'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gs_system_id', 'gs_staff_id'])

        # Adding model 'gs_soft'
        db.create_table(u'cmdb_gs_soft', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('soft_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('soft_version', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('soft_source', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('soft_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_soft'])

        # Adding model 'gs_phy'
        db.create_table(u'cmdb_gs_phy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phy_ip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phy_location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phy_sdate', self.gf('django.db.models.fields.DateField')()),
            ('phy_describe', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phy_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_phy'])

        # Adding model 'gs_vm'
        db.create_table(u'cmdb_gs_vm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vm_ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vm_hostname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vm_os', self.gf('django.db.models.fields.related.ForeignKey')(related_name='os_name', to=orm['cmdb.gs_soft'])),
            ('vm_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmdb.gs_system'])),
            ('vm_phy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmdb.gs_phy'])),
            ('vm_conf', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vm_sdate', self.gf('django.db.models.fields.DateField')()),
            ('vm_describe', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vm_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_vm'])

        # Adding M2M table for field vm_soft on 'gs_vm'
        m2m_table_name = db.shorten_name(u'cmdb_gs_vm_vm_soft')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gs_vm', models.ForeignKey(orm[u'cmdb.gs_vm'], null=False)),
            ('gs_soft', models.ForeignKey(orm[u'cmdb.gs_soft'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gs_vm_id', 'gs_soft_id'])

        # Adding model 'gs_user'
        db.create_table(u'cmdb_gs_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmdb.gs_vm'])),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('user_password', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('user_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cmdb', ['gs_user'])


    def backwards(self, orm):
        # Deleting model 'gs_staff'
        db.delete_table(u'cmdb_gs_staff')

        # Deleting model 'gs_idc'
        db.delete_table(u'cmdb_gs_idc')

        # Deleting model 'gs_cab'
        db.delete_table(u'cmdb_gs_cab')

        # Deleting model 'gs_system'
        db.delete_table(u'cmdb_gs_system')

        # Removing M2M table for field sys_manage on 'gs_system'
        db.delete_table(db.shorten_name(u'cmdb_gs_system_sys_manage'))

        # Deleting model 'gs_soft'
        db.delete_table(u'cmdb_gs_soft')

        # Deleting model 'gs_phy'
        db.delete_table(u'cmdb_gs_phy')

        # Deleting model 'gs_vm'
        db.delete_table(u'cmdb_gs_vm')

        # Removing M2M table for field vm_soft on 'gs_vm'
        db.delete_table(db.shorten_name(u'cmdb_gs_vm_vm_soft'))

        # Deleting model 'gs_user'
        db.delete_table(u'cmdb_gs_user')


    models = {
        u'cmdb.gs_cab': {
            'Meta': {'ordering': "['cab_id']", 'object_name': 'gs_cab'},
            'cab_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cab_idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_idc']"}),
            'cab_size': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmdb.gs_idc': {
            'Meta': {'ordering': "['idc_name']", 'object_name': 'gs_idc'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'idc_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'idc_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cmdb.gs_phy': {
            'Meta': {'object_name': 'gs_phy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phy_describe': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phy_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phy_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phy_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phy_sdate': ('django.db.models.fields.DateField', [], {})
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
            'user_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_vm']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'cmdb.gs_vm': {
            'Meta': {'ordering': "['vm_ip']", 'object_name': 'gs_vm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vm_conf': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vm_describe': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vm_hostname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vm_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vm_ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vm_os': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'os_name'", 'to': u"orm['cmdb.gs_soft']"}),
            'vm_phy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_phy']"}),
            'vm_sdate': ('django.db.models.fields.DateField', [], {}),
            'vm_soft': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'install_soft'", 'symmetrical': 'False', 'to': u"orm['cmdb.gs_soft']"}),
            'vm_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmdb.gs_system']"})
        }
    }

    complete_apps = ['cmdb']