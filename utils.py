from datetime import datetime, timedelta

# 計算當前時間與設定鬧鐘時間的剩餘時間
def get_remaining_time(alarm_time):
    now = datetime.now()
    time_diff = alarm_time - now
    return time_diff.total_seconds()

# 計算並返回鬧鐘應該設置的時間
def calculate_alarm_time(alarm_time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(alarm_time_str, '%H:%M')
    alarm_datetime = datetime.combine(now.date(), alarm_time.time())

    # 如果設定時間已經過去，則設為明天
    if alarm_datetime < now:
        alarm_datetime += timedelta(days=1)

    return alarm_datetime
