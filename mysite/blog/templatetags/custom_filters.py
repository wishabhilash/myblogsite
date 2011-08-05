from django import template
import re
from datetime import datetime

register = template.Library()

months = {1 : "January",
		  2 : "February",
		  3 : "March",
		  4 : "April",
		  5 : "May",
		  6 : "June",
		  7 : "July",
		  8 : "August",
		  9 : "September",
		  10 : "October",
		  11 : "November",
		  12 : "December"}


@register.filter(name = 'display_date')
def display_date(value):
	year = value.date().year
	month = value.date().month
	day = value.date().day
	if day is 1:
		supsct = 'st'
	elif day is 2:
		supsct = 'nd'
	elif day is 3:
		supsct = 'rd'
	else:
		supsct = 'th'
	return "%s<sup>%s</sup> %s, %s" % (day, supsct, months[month], year)

@register.filter(name = "convertIntoMonth")
def convertIntoMonth(value):
	return months[value]
	
@register.filter(name = 'bold')
def bold(value):
	return "<b>%s</b>" % value

@register.filter(name = 'poemsinyear')
def poemsinyear(value):
	count = 0
	poems = value[1]
	for poem in poems:
		count += len(poem[1])
	return count

@register.filter(name = 'urlTitleArgFormat')
def urlTitleArgFormat(value):
	return value.lower().replace(' ','_')

@register.filter(name = "urlArgFormat")
def urlArgFormat(value, title):
	return str(value.year)+'/'+str(value.month)+'/'+urlTitleArgFormat(title)

@register.filter(name = "doublequotify")
def dquote(value):
	return '"' + value + '"'
