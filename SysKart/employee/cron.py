from django_cron import CronJobBase, Schedule

from .models import *


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "employee.my_cron_job"

    def do(self):
        import calendar
        from datetime import datetime

        date = datetime.now().strftime("%d/%m/%Y")
        month = date[3:5]
        year = date[6:10]

        current_month_days = calendar.monthrange(int(year), int(month))[1]
        salary = {}
        ids = EmployeeDetails.objects.all().values('id')
        for x in range(1, len(ids)+1):
            qs = EmployeeDetails.objects.get(id=x)
            sdate = "01/{m}/{y}".format(m=month, y=year)
            edate = "{d}/{m}/{y}".format(d=current_month_days, m=month, y=year)
            th = EmployeeAttandance.objects.filter(employee_id=qs.id, date__range=[sdate, edate]).values("total_hours")
            timeList = []
            for y in range(len(th)):
                timeList.append(th[y]["total_hours"])
                totalSecs = 0
            for tm in timeList:
                timeParts = [int(s) for s in tm.split(":")]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
            totalSecs, sec = divmod(totalSecs, 60)
            hr, min = divmod(totalSecs, 60)
            print("%d:%02d:%02d" % (hr, min, sec))
            t_h = float(EmployeeDetails.objects.filter(id=1).values("salary")[0]["salary"])
            dh = current_month_days * 8
            sall = t_h / dh
            total_salary = float(sall) * float(hr)
            salary[x] = total_salary
        return salary
