import time

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_days = [31, (28, 29), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
wd = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

def get_1st_day(date, day):
    for i in reversed(range(date)):
        if day == -1:
            day = 6
        day -= 1
    
    day += 1
    
    return day

def get_inverted_color(text):
    return "\33[38;5;0;48;5;255m" + text + "\33[m"

def print_cal(_user_data):

    if _user_data.exists("TZ_OFFSET"):
        tz_offset = _user_data.read("TZ_OFFSET")
    else:
        tz_offset = 0

    year, month, month_day, hour, min, second, weekday, year_day = time.localtime(time.time() + tz_offset)
    month -= 1

    day_1 = get_1st_day(month_day, weekday)

    weekDays = ""
    for i in wd:
        weekDays += i + " "
    weekDays.rstrip(" ")

    _month = months[month] + " " + str(year)
    _space_offset = round((len(weekDays) - len(_month)) / 2)
    print(" " * _space_offset + _month + " " * _space_offset)
    print(weekDays)
    date_str = ""
    date_str += " " * (day_1 * 3)
    day_idx = day_1
    for i in range(month_days[month]):
        _i = i + 1
        if _i < 10:
            date_str += " "
        date_str += get_inverted_color(str(_i)) if _i == month_day else str(_i)
        day_idx += 1
        if day_idx <= 6:
            date_str += " "
        else:
            day_idx = 0
            date_str += "\n"
    
    print(date_str)
