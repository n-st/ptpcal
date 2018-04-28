#!/usr/bin/env python3
# encoding: utf-8 (as per PEP 263)

import os
import locale
import jinja2
import datetime
import calendar
import icalendar

year = 2018
locale_str = 'de_DE.utf8'
holiday_ics_file = 'holidays.ics'

locale.setlocale(locale.LC_TIME, locale_str)

holidays = []

if os.path.exists(holiday_ics_file):
    with open(holiday_ics_file) as f:
        calstr = f.read()

    cal = icalendar.Calendar.from_ical(calstr)

    for event in cal.walk('vevent'):
        startdate = event.get('dtstart').dt if event.get('dtstart') else None
        enddate = event.get('dtend').dt if event.get('dtend') else None
        # Add every day affected by a holiday individually (since a holiday
        # calendar entry may span multiple days)
        while startdate and enddate and startdate < enddate:
            day_tuple = (startdate.day, startdate.month, startdate.year)
            holidays.append(day_tuple)
            startdate += datetime.timedelta(days=1)

c = calendar.Calendar()

weekday_abbrs = calendar.day_abbr

field_length = len(weekday_abbrs[0])
cal_line_fmt = '%%%ds %%%ds %%%ds %%%ds %%%ds %%%ds %%%ds' % ((field_length,)*7)

def format_day(day, month, year, length):
    if day not in range(0, 32):
        return day
    elif (day, month, year) in holidays:
        return ' ' * (length - len(str(day))) + r'\holiday{%s}' % day
    elif calendar.weekday(year, month, day) == 6:
        return ' ' * (length - len(str(day))) + r'\sunday{%s}' % day
    else:
        return day

latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%!',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

calendar_months = []
for month in range(1,13):
    callines = []
    callines += [r'\weekdays{' + cal_line_fmt % tuple(weekday_abbrs) + '}']
    for week in c.monthdayscalendar(year, month):
        days = [(day or '') for day in week]
        days = [format_day(day, month, year, field_length) for day in days]
        days = tuple(days)
        callines += [cal_line_fmt % days]

    this_month = {}
    this_month['imagefile'] = 'month%02d' % month
    this_month['name'] = calendar.month_name[month]
    this_month['caltext'] = '\n'.join(callines)

    calendar_months.append(this_month)

template = latex_jinja_env.get_template('calendar.tex.j2')
output_tex = template.render(months=calendar_months)
print(output_tex)
