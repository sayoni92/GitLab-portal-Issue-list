from business_duration import businessDuration
import pandas as pd
import holidays as pyholidays
from datetime import time

#Start date must be in standard python datetime format
start_date = pd.to_datetime('2017-07-01 02:02:00')

#Start date must be in standard python datetime format
end_date = pd.to_datetime('2017-07-07 04:48:00')

#Business open hour must be in standard python time format-Hour,Min,Sec
biz_open_time=time(8,0,0)
biz_close_time=time(17,0,0)

#US public holidays
US_holiday_list = pyholidays.US(state='NY')

#Business duration can be 'day', 'hour', 'min', 'sec'
unit_hour='hour'

#Printing output
print(businessDuration(startdate=start_date,enddate=end_date,starttime=biz_open_time,endtime=biz_close_time,holidaylist=US_holiday_list,unit=unit_hour))

#Result
#30.0
