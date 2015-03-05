# coding:utf-8
from Demo.cmdb.models import *
from django.contrib import admin


class staff_admin(admin.ModelAdmin):
    search_fields = ('staff_name', 'staff_id')


class vm_admin(admin.ModelAdmin):
    list_display = ('vm_ip', 'vm_hostname', 'vm_os', 'vm_system', 'vm_info')
    list_filter = ('vm_os', 'vm_system')
    search_fields = ('vm_ip', 'vm_hostname', 'vm_info')
    filter_horizontal = ('vm_soft',)


class user_admin(admin.ModelAdmin):
    search_fields = ('user_ip__vm_ip', 'user_info')
    list_filter = ('user_type', 'user_login')
    list_display = ('user_ip', 'user_name', 'user_password', 'user_type', 'user_login')


class soft_admin(admin.ModelAdmin):
    search_fields = ('user_ip', 'user_name')


class sys_admin(admin.ModelAdmin):
    list_display = ('sys_cname', 'sys_ename', 'sys_sa')


class domain_admin(admin.ModelAdmin):
    search_fields = ('domain_name', 'domain_expiration')
    list_display = ('domain_name', 'domain_expiration', 'domain_mx')


class sub_domain_admin(admin.ModelAdmin):
    search_fields = ('sub_domain_name', 'sub_domain_ip')
    list_display = ('sub_domain_name', 'sub_domain_ip')


class work_admin(admin.ModelAdmin):
    list_display = ('work_date', 'work_content', 'work_class', 'work_total')


class account_admin(admin.ModelAdmin):
    list_display = ('link', 'account_info', 'user', 'passwd')


class vpnuser_admin(admin.ModelAdmin):
    list_display = ('username', 'update', 'status')


class dailywork_admin(admin.ModelAdmin):
    list_display = (
    'dailywork_date', 'dailywork_author', 'dailywork_content', 'dailywork_type', 'dailywork_info')


admin.site.register(gs_idc)
admin.site.register(gs_cab)
admin.site.register(gs_staff, staff_admin)
admin.site.register(gs_system, sys_admin)
admin.site.register(gs_soft)
admin.site.register(gs_phy)
admin.site.register(gs_vm, vm_admin)
admin.site.register(gs_user, user_admin)
admin.site.register(gs_domain, domain_admin)
admin.site.register(gs_sub_domain, sub_domain_admin)
admin.site.register(gs_work, work_admin)
admin.site.register(gs_account, account_admin)
admin.site.register(gs_vpnuser, vpnuser_admin)
admin.site.register(gs_dailywork, dailywork_admin)

