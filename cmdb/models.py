# coding:utf-8
from django.db import models
from django.contrib import admin
from manage import *


class gs_staff(models.Model):
    staff_id = models.IntegerField(verbose_name='员工工号')
    staff_name = models.CharField(max_length=50, verbose_name='员工姓名')
    staff_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='员工手机号')
    staff_postition = models.CharField(max_length=50, null=True, blank=True, verbose_name='员工职位')
    staff_department = models.CharField(max_length=50, null=True, blank=True, verbose_name='员工部门')
    staff_manage = models.ForeignKey('self', null=True, blank=True, verbose_name='部门经理')
    staff_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='员工信息')

    def __unicode__(self):
        return self.staff_name

    class Meta:
        ordering = ['staff_name']


class gs_idc(models.Model):
    idc_id = models.CharField(max_length=50, verbose_name='机房号')
    idc_name = models.CharField(max_length=50, verbose_name='机房名')
    idc_location = models.CharField(max_length=50, verbose_name='机房位置')
    idc_iprange = models.CharField(max_length=100, null=True, blank=True, verbose_name='IP地址段')

    def __unicode__(self):
        return self.idc_name

    class Meta:
        ordering = ['idc_name']


class gs_cab(models.Model):
    cab_id = models.CharField(max_length=50, verbose_name='机柜序列号')
    cab_idc = models.ForeignKey(gs_idc, verbose_name='机柜所在机房')
    cab_size = models.CharField(max_length=50, null=True, blank=True, verbose_name='机柜大小')

    def __unicode__(self):
        return self.cab_idc

    class Meta:
        ordering = ['cab_id']


class gs_system(models.Model):
    sys_cname = models.CharField(max_length=50, verbose_name='系统中文名')
    sys_ename = models.CharField(max_length=50, null=True, blank=True, verbose_name='系统英文名')
    sys_sa = models.ForeignKey(gs_staff, related_name='system administrator', verbose_name='系统管理员')
    sys_manage = models.ManyToManyField(gs_staff, related_name='system developer', verbose_name='系统负责人')
    sys_stime = models.DateField(verbose_name='系统上线日期', null=True, blank=True)
    sys_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='系统信息')

    def __unicode__(self):
        return self.sys_ename

    class Meta:
        ordering = ['sys_cname']


class gs_soft(models.Model):
    soft_name = models.CharField(max_length=40, verbose_name='软件名'.decode('utf8'))
    soft_version = models.CharField(max_length=40, verbose_name='软件版本'.decode('utf8'))
    soft_source = models.CharField(max_length=100, null=True, blank=True, verbose_name='软件安装源')
    soft_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='软件信息')

    def __unicode__(self):
        return self.soft_name + ' ' + self.soft_version

    class Meta:
        ordering = ['soft_name']


class gs_phy(models.Model):
    phy_ip = models.CharField(max_length=100, verbose_name='物理机IP')
    phy_location = models.ForeignKey(gs_cab, verbose_name='物理机机柜')
    phy_sdate = models.DateField(verbose_name='物理机使用时间')
    phy_describe = models.CharField(max_length=100, verbose_name='物理机描述')
    phy_Maintenance = models.CharField(max_length=100, null=True, blank=True, verbose_name='物理机维保号')
    pyh_warranty = models.CharField(max_length=100, null=True, blank=True, verbose_name='物理机保修期')
    phy_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='物理机备注')

    def __unicode__(self):
        return self.phy_ip


class gs_vm(models.Model):
    vm_ip = models.CharField(max_length=50, verbose_name='虚拟机IP')
    vm_hostname = models.CharField(max_length=50, null=True, blank=True, verbose_name='虚拟机主机名')
    vm_os = models.ForeignKey(gs_soft, related_name='os_name', verbose_name='虚拟机操作系统')
    vm_manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='负责')
    vm_system = models.ForeignKey(gs_system, null=True, blank=True, verbose_name='虚拟机所属系统')
    vm_soft = models.ManyToManyField(gs_soft, null=True, blank=True, related_name='install_soft',
                                     verbose_name='虚拟机安装软件'.decode('utf8'))
    vm_phy = models.ForeignKey(gs_phy, null=True, blank=True, verbose_name='虚拟机所属物理机')
    vm_mem = models.IntegerField(null=True, blank=True, verbose_name='虚拟机内存  G')
    vm_cpu = models.IntegerField(null=True, blank=True, verbose_name='虚拟机cpu 核')
    vm_disk = models.IntegerField(null=True, blank=True, verbose_name='虚拟机磁盘  G')
    vm_sdate = models.DateField(verbose_name='虚拟机启用时间')
    vm_describe = models.CharField(max_length=100, null=True, blank=True, verbose_name='虚拟机描述')
    vm_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='虚拟机备注')

    def __unicode__(self):
        return self.vm_ip

    class Meta:
        ordering = ['vm_ip']


class gs_user(models.Model):
    user_ip = models.ForeignKey(gs_vm, verbose_name='虚拟机IP')
    user_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='用户名')
    user_password = models.CharField(max_length=100, null=True, blank=True, verbose_name='密码')
    user_device = models.CharField(max_length=100, null=True, blank=True, verbose_name='设别类型')
    user_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='用户类型')
    user_login = models.CharField(max_length=50, null=True, blank=True, verbose_name='用户登录方式')
    user_info = models.CharField(max_length=100, null=True, blank=True, verbose_name='虚拟机备注')

    def __unicode__(self):
        return self.user_ip.vm_ip

    class Meta:
        ordering = ['user_ip']


class gs_domain(models.Model):
    domain_name = models.CharField(max_length=50, verbose_name='域名名称')
    domain_expiration = models.CharField(max_length=50, null=True, blank=True, verbose_name='域名过期时间')
    domain_supply = models.CharField(max_length=50, null=True, blank=True, verbose_name='供应商')
    domain_supplylink = models.URLField(max_length=50, null=True, blank=True, verbose_name='供应商链接')
    domain_supplycontact = models.CharField(max_length=50, null=True, blank=True, verbose_name='供应商联系人')
    domain_mx = models.CharField(max_length=50, null=True, blank=True, verbose_name='域名映射MX记录')
    domain_mx_priorty = models.CharField(max_length=300, null=True, blank=True, verbose_name='域名映射MX记录优先级')

    def __unicode__(self):
        return self.domain_name

    class Meta:
        ordering = ['domain_name']


class gs_sub_domain(models.Model):
    sub_domain_name = models.CharField(max_length=50, verbose_name='二级域名名称')
    sub_domain_domain = models.ForeignKey(gs_domain, verbose_name='父域名')
    sub_domain_ip = models.CharField(max_length=50, null=True, blank=True, verbose_name='域名映射IP')
    sub_domain_sys = models.ManyToManyField(gs_system, null=True, blank=True, verbose_name='域名关联系统'.decode('utf8'))

    def __unicode__(self):
        return self.sub_domain_name

    class Meta:
        ordering = ['sub_domain_name']


class gs_work(models.Model):
    work_date = models.DateField()
    work_content = models.CharField(max_length=300)
    work_class = models.CharField(max_length=10)
    work_num = models.IntegerField()
    work_total = models.IntegerField()
    objects = workmanage()

    def __unicode__(self):
        return self.work_content

    class Meta:
        ordering = ['work_content']


class gs_crvm(models.Model):
    nvm_id = models.IntegerField(null=True, blank=True, )
    nvm_jobid = models.IntegerField(null=True, blank=True, )
    nvm_name = models.CharField(max_length=300, null=True, blank=True, )
    nvm_cpu = models.IntegerField(null=True, blank=True, )
    nvm_mem = models.IntegerField(null=True, blank=True, )
    nvm_disk = models.IntegerField(null=True, blank=True, )
    nvm_describle = models.CharField(max_length=500, null=True, blank=True, )
    nvm_phy = models.CharField(max_length=300, null=True, blank=True, )
    nvm_status = models.CharField(max_length=100, null=True, blank=True, )
    nvm_createtime = models.DateField(null=True, blank=True, )

    def __unicode__(self):
        return self.nvm_name

    class Meta:
        ordering = ['nvm_name']


class gs_account(models.Model):
    link = models.CharField(max_length=300)
    account_info = models.CharField(max_length=300)
    user = models.CharField(max_length=300)
    previous_passwd = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300)

    def __unicode__(self):
        return self.account_info

    class Meta:
        ordering = ['account_info']


class gs_vpnuser(models.Model):
    username = models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    depname = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    update = models.CharField(max_length=300)
    info = models.CharField(max_length=500)
    status = models.CharField(max_length=300, null=True, blank=True, )

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-update']


class gs_vpnmailinform(models.Model):
    '''status 状态为Y 的已发送邮件通知，N的未发送邮件通知，VIP的为VIP用户
        E的为邮件发送失败，D的为已禁用用户，C的为将要禁用的用户'''
    username = models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    depname = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    update = models.CharField(max_length=300)
    info = models.CharField(max_length=500)
    status = models.CharField(max_length=300, null=True, blank=True, )

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-update']


class gs_vpndisableuser(models.Model):
    '''status 状态为Y 的已成功禁用，未N的未禁用，未E的禁用失败'''
    username = models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    depname = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    update = models.CharField(max_length=300)
    info = models.CharField(max_length=500)
    status = models.CharField(max_length=300, null=True, blank=True, )

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-update']


class gs_dailywork(models.Model):
    dailywork_date = models.DateField()
    dailywork_content = models.CharField(max_length=300)
    dailywork_type = models.CharField(max_length=20)
    dailywork_subtype = models.CharField(max_length=20)
    dailywork_cost = models.FloatField(null=True, blank=True)
    dailywork_info = models.CharField(null=True, blank=True, max_length=300)
    dailywork_author = models.CharField(max_length=50)

    def __unicode__(self):
        return self.dailywork_content

    class Meta:
        ordering = ['dailywork_content']
