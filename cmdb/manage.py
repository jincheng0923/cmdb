from django.db import connection, models
from django.db import models
import datetime

class workmanage(models.Manager):
    def getwork(self,starttime,endtime):
        cursor = connection.cursor()
        sql="SELECT *  FROM cmdb_gs_work  WHERE work_date > '%s' and work_date < '%s' " %(starttime,endtime)
        cursor.execute(sql)
        info=cursor.fetchall()
        return info
    