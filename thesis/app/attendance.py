
from .models import *
from django.db.models import Min, Q, F
from django.db.models.functions import ExtractDay, ExtractHour
from django.db.models import Subquery

from datetime import datetime, timedelta
import calendar

def Recog_attendance():
    time_now = datetime.now().hour 
    int_now = datetime.now().day
    today = calendar.day_name[datetime.now().weekday()]
    sec_now = Section.objects.annotate(sec_time_start=ExtractHour('schedule_fk__time_start'),sec_time_end=ExtractHour('schedule_fk__time_end')).filter(Q(schedule_fk__day=today)&Q(sec_time_start__lte=time_now)&Q(sec_time_end__gte=time_now))
    rec_sec = Recorded.objects.annotate(day_now=ExtractDay('time_detected')).filter(day_now=int_now)

    def addMins(tm, mins):
        fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + timedelta(minutes=mins)
        return fulldate. time()



    on_time = []
    late = []
    for sec in sec_now:
         sec_late = addMins(sec.schedule_fk.time_start, 15)
         sect.append(sec_late)
         for rec in rec_sec:
                 if rec.time_detected.time() <= sec_late and rec.time_detected.time() >= sec.schedule_fk.time_start:
                         on_time.append(rec.student_name)
                         distinct_on_time = list(set(on_time))
                 elif rec.time_detected.time() >= sec_late and rec.time_detected.time() <= sec.schedule_fk.time_end:
                         late.append(rec.student_name)
                         distinct_late = list(set(late))

    ##### Refine arrays
    on_time= list(set(on_time))    
    late = list(set(late))     
    late = [x for x in on_time if x not in late]
    #Aggregate the lists
    detected  = on_time + late

    ##### Update query

    for sec in sec_now:
        for early in on_time:
            StudentAttendance.objects.filter(Q(section_fk__section_code = sec.section_code)&Q(student_fk__name=early)).update(attendance_on_time=F('attendance_on_time')+1)
          
        for tardy in late:
            StudentAttendance.objects.filter(Q(section_fk__section_code = sec.section_code)&Q(student_fk__name = tardy)).update(attendance_late=F('attendance_late')+1)

            #THIS has to be outside or conditioned to be executed 1 minute before section_time end
        StudentAttendance.objects.filter(section_fk__section_code = sec.section_code).exclude(student_fk__name__in=detected).distinct().update(attendance_absent=F('attendance_absent')+1)



