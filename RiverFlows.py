#!/usr/bin/python3.8
print('Content-type: text/html\n')
print('<html>')
print('<HEAD>')
print('</meta>')
print('<meta charset="UTF-8">')
print('</meta>')
print('</HEAD>')
print('<body>')
print('<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">')
print('Provo River CFS Flows:')
print('</div>')
print('<img src="/static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="provoriverflows.com/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="/static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="/static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
print('</body>')
print('</html>')

import cgi
import cgitb
import requests
import json
import pygal
import datetime
import platform
from datetime import datetime
#from backports.datetime_fromisoformat import MonkeyPatch
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
import re

#print(platform.python_version())
cgitb.enable(display=0, logdir="/var/log/apache2/cgilog.log")
url = "https://waterservices.usgs.gov/nwis/iv/?sites=10163000,10155200&format=json,1.1&period=P7D"
prwuascadaurl = "https://www.prwua.org/operations/scada-system-data/?q=csvdisplay"
prwuawaterreporttxt = "https://www.prwua.org/operations/water-report/?q=txt"
prwua800naqueductflow = "https://www.prwua.org/operations/daily-average-flow-data/?q=csvdisplay"

response = requests.get(url)
prwuascadaresponse = requests.get(prwuascadaurl)
prwuawaterreportresponse = requests.get(prwuawaterreporttxt)
prwua800naqueductflowresponse = requests.get(prwua800naqueductflow)

a = []
b = []
c = []
adate = []
bdate = []
cdate = []

newscadaresponse = prwuascadaresponse.text.split("\n")

for list in newscadaresponse:
	x = re.search("S16_FIT_1M", list)
	if x != None:
#		print(x)
#		print(list)
#		print("space")
		y = list.split(',')
		a.append(y[2])
		adate.append(y[1])
#		print("space")
#		print(a)
aqueduct800nflow = a[0]

newwatertext = prwuawaterreportresponse.text.split("\n")
#print(newwatertext)
for line in newwatertext:
	w = re.search("Deer Creek Reservoir", line)
	x = re.search("Provo River", line)
	if w != None:
		u = line.split(" ")
#		print(u)
		bdate.append(u[6])
	if x != None:
		y = line.split(" ")
#		print(y)
		if y[3] == "" and y[6] == "":
			b.append(y[11])

newaqueducttext = prwua800naqueductflowresponse.text.split("\n")

for line in newaqueducttext:
	t = re.search("Tag Name", line)
	if t != None:
#		print(line)
		u = line.split(",")
		u.pop(0)
		u.pop(0)
		cdate.append(u)
	w = re.search("800 North Provo River Aqueduct Flow", line)
	if w != None:
#		print(line)
		x = line.split(",")
		x.pop(0)
		x.pop(0)
#		print(x)
		c.append(x)
#filtered7dayswaterlist = response.Content

response_dict = response.json()



#print ("water content:", response_dict.keys())



sevendayswaterlist = response_dict['value']


#print("water content:", response_dict['value'])
#.timeseries[0].values[0].value])
#print(sevendayswaterlist.keys())

#gather data from index0 which contains USGS 10155200 PROVO RIV AT RIV ROAD BRIDGE NR HEBER CITY, UT
middletimeseriessevendayswaterlist = sevendayswaterlist['timeSeries'][0]

#print(middletimeseriessevendayswaterlist.keys())

msevendayswaterlistvalues = middletimeseriessevendayswaterlist['values'][0]
middlesevendayswaterlistresults = msevendayswaterlistvalues['value']

#print (middlesevendayswaterlistresults)

#gather data from index2 which contains USGS 10163000 PROVO RIVER AT PROVO, UT
lowertimeseriessevendayswaterlist = sevendayswaterlist['timeSeries'][2]

#print(lowertimeseriessevendayswaterlist.keys())

lsevendayswaterlistvalues = lowertimeseriessevendayswaterlist['values'][0]
lowersevendayswaterlistresults = lsevendayswaterlistvalues['value']
#print (lowersevendayswaterlistresults)


lconvertedsevendayswaterlistresults = []
mconvertedsevendayswaterlistresults = []


lowerstoredvalues = []
middlestoredvalues = []
storedvalues = []



for sampling in lowersevendayswaterlistresults:
 lconvertedsevendayswaterlistresults.append(sampling)

for sampling in middlesevendayswaterlistresults:
 mconvertedsevendayswaterlistresults.append(sampling)

#print (mconvertedsevendayswaterlistresults[0])

#filter through all the sampling for the values at 6 am and store in middlestorevalues
for storedvalue in mconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        middlestoredvalues.append(storedvalue)

#print(middlestoredvalues)

#print (lconvertedsevendayswaterlistresults[0])

#filter through all the sampling for the values at 6 am and store in lowerstorevalues
for storedvalue in lconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        lowerstoredvalues.append(storedvalue)

#print(type(lowerstoredvalues))

#import pdb; pdb.set_trace()


#convertedlstoredvalues = []

#for jsonobject in lowerstoredvalues:
#   print (jsonobject)
#   jsonstring = str(jsonobject)
#   doublejsonstring = jsonstring.replace("\'","\"")
#   print (doublejsonstring)

#   convertedlstoredvalues.append(json.loads(doublejsonstring))
#print (convertedlstoredvalues[0])
#convertedmstoredvalues = json.loads(middlestoredvalues)

#print (type(convertedlstoredvalues))
#print(type(middlestoredvalues))

mflow, mdate = [],[]
lflow, ldate = [],[]
aflows, adates = [],[]
bflows, bdates = [],[]
cflows, cdates = [],[]

formattedmdate = []
formattedldate = []
formattedadate = []
formattedbdate = []
formattedcdate = []
adictionary = {}
bdictionary = {}
cdictionary = {}

newadates = []


for sampling in middlestoredvalues:
    mflow.append(int(float(sampling['value'])))
    mdate.append(sampling['dateTime'])

for sampling in lowerstoredvalues:
    lflow.append(int(float(sampling['value'])))
    ldate.append(sampling['dateTime'])

for dates in adate:
	x = dates.split(" ")[0]
	#x = x + "/2021"
	newadates.append(x)

adate = newadates

for i, j in zip(a, adate):
        x = ""
        y = ""
        adictionary.update({j: i})
        aflows.append(int(float(i)))
        adates.append(j)

for i, j in zip(b, bdate):
        bdictionary.update({j: i})
        bflows.append(int(float(i)))
        bdates.append(j)

for i, j in zip(c, cdate):
        x = ""
        y = ""
        for count, k in enumerate(cdate[0]):
                x = i[count]
 #               print(x)
 #               print(" ")
                y = j[count]
 #               print(y)
                cdictionary.update({y: x})
                cflows.append(int(float(x)))
                cdates.append(y)

for date in mdate:
    somedate = datetime.fromisoformat(date)
    middlesampledate = str(somedate.month) + "-" + str(somedate.day) + "-" + str(somedate.year)
    formattedmdate.append(middlesampledate)

for date in ldate:
    somedate = datetime.fromisoformat(date)
    lowersampledate = str(somedate.month) + "-" + str(somedate.day) + "-" + str(somedate.year)
    formattedldate.append(lowersampledate)

for date in adates:
	newadate = date.replace("/", ",")
	newadate = newadate.split(",")
	x = int(newadate[0])
	y = int(newadate[1])
	z = int(newadate[2])
	somedate = datetime.fromisocalendar(z,x,y)
#	print(somedate)
	asampledate = str(somedate.month) + "-" + str(somedate.day) + "-" + str(somedate.year)
	formattedadate.append(asampledate)

for date in bdates:
#	print(date)
	newbdate = date.replace("-",",")
#	print(newbdate)
	dateb = str(datetime.strptime(newbdate, '%d,%b,%y'))
#	print(dateb)
	newbdate = re.split('-| ', dateb)
#	print(newbdate)
	x = int(newbdate[0])
	y = int(newbdate[1])
	z = int(newbdate[2])
	somedate = newbdate[0] + "-" + newbdate[1] + "-" + newbdate[2]
	somebdate = datetime.fromisoformat(somedate)
#	print(somedate)
#	print(somebdate)
	bsampledate = str(somebdate.month) + "-" + str(somebdate.day) + "-" + str(somebdate.year)
	formattedbdate.append(bsampledate)

for date in cdate:
#	print(date)
#	print(type(date))
	for item in date:
		#print(item)
		year = str(datetime.now().year)
		item = item + "/" + year
#		print(item)
		newcdate = item.replace("/", ",")
		newcdate = newcdate.split(",")
#		print(newcdate)
		v = newcdate[0].split("0")[1]
		w = newcdate[2].split("20")[1]
#		print(w)
		x = int(newcdate[0])
		y = int(newcdate[1])
		z = int(newcdate[2])
		somedate = newcdate[2] + "-" + newcdate[0] + "-" + newcdate[1]
		somecdate = datetime.fromisoformat(somedate)
#		print(somecdate)
		csampledate = str(somecdate.month) + "-" + str(somecdate.day) + "-" + str(somecdate.year)
		formattedcdate.append(csampledate)

#print(mflow)
#print(lflow)
#make visualization


chart1 = pygal.Bar()
chart1.title = "Middle Provo flows from past week"
chart1.x_labels = formattedmdate

#chart1.add('', [535,523,548,528,516,535])
chart1.add('Flows', mflow)
#chart1.render()
#chart1.render_to_file('python_usgs_middle_repo.svg')

#style2 = LS('#333366', base_style=LCS)
#chart2 = pygal.Bar(style = style2, x_label_rotation=45, show_legend=true)
chart2 = pygal.Bar()
chart2.title = "Lower Provo flows from past week"
chart2.x_labels = formattedldate

chart2.add('Flows',lflow)
#chart2.render_to_file('python_usgs_lower_repo.svg')

chart3 = pygal.Bar()
chart3.title = "Lower and Middle Provo flows from past week"
chart3.x_labels = formattedldate
chart3.add('Lower Flows',lflow)
chart3.add('Middle Flows',mflow)
chart3.render_to_file('/var/www/provoriverflows.com/static/images/Lower_and_Middle_Provo.svg')
lcurrentdate = formattedldate[-1]
lyesterday = formattedldate[-2]

chart4 = pygal.Bar()
chart4.truncate_legend = -1
chart4.title = "Lower and Middle Provo flows (CFS) from past week"
chart4.y_title = ('Flows (CFS)')
chart4.x_labels = formattedldate
#chart4.y_labels = Flows(cfs)
chart4.add('Lower Flows',lflow)
chart4.add('Middle Flows',mflow)
chart4.add('PRWUA Scada Flow 800n',aflows)
chart4.add('PRWUA Deer Creek Release Flows',bflows)
chart4.add('PRWUA 800n weekly flow',cflows)
chart4.render_to_file('/var/www/provoriverflows.com/static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg')
#print(formattedmdate)
#print(formattedldate)

lcfsflowdifference = lflow[-1] - lflow[-2]
mcfsflowdifference = mflow[-1] - mflow[-2]

#print (lcfsflowdifference)
#print (mcfsflowdifference)

cfsflowthresholdreached = 0
cfsflowthresholdbreached = False

if lcfsflowdifference >= 200 or lcfsflowdifference <= -200:
    cfsflowthresholdreached +=1    
    cfsflowthresholdbreached = True
    
if mcfsflowdifference >= 200 or mcfsflowdifference <= -200:
    cfsflowthresholdreached += 1
    cfsflowthresholdbreached = True


lprovothreshold = "null"
mprovothreshold = "null"

#lcfsflowdifference = -301
#mcfsflowdifference = 300

if lcfsflowdifference <= -1:
    lprovothreshold = "negative"
if lcfsflowdifference >= 1:
    lprovothreshold = "positive"
    
if mcfsflowdifference <= -1:
    mprovothreshold = "negative"
if mcfsflowdifference >= 1:
    mprovothreshold = "positive"

emaildecreaseflowsmessage = "There has been at least a 200 cfs flow decrease"
emailincreaseflowsmessage = "There has been at least a 200 cfs flow increase"



recipientemail = "dyeman20@gmail.com"

server = smtplib.SMTP(host="smtp.gmail.com",port = 587)
server.starttls()
server.login("dyeman20", "qztjgfohlkkwivrr")
msg = MIMEMultipart()
msg['From']="dyeman20@gmail.com"
msg['To']="dyeman20@gmail.com"
#msg['subject']=""


#import pdb; pdb.set_trace()

if cfsflowthresholdbreached == True:
    while cfsflowthresholdreached >=1 :

        if lcfsflowdifference >= 200 or lcfsflowdifference <= -200:
                    
            print("lthreshold:",lprovothreshold)
            if lprovothreshold == "positive":
                msg['subject']="Lower Provo Flows change"
                msg.attach(MIMEText(emailincreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1
            
            if lprovothreshold == "negative":
                msg['subject']="Lower Provo Flows change"
                msg.attach(MIMEText(emaildecreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1

        if mcfsflowdifference >= 200 or mcfsflowdifference <= -200:
            
            print ("Entered middle provo flows difference")
            print ("mthreshold:",mprovothreshold)

            

            if mprovothreshold == "positive":
                print ("Entered middle provo p threshold")
                msg['subject']="Middle Provo Flows change"
                msg.attach(MIMEText(emailincreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1
            if mprovothreshold == "negative":
                print ("Entered middle provo n threshold")
                msg['subject']="Middle Provo Flows change"
                msg.attach(MIMEText(emaildecreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreachedd -= 1
#def application(environ,start_response):

#print (msg)
#import pdb; pdb.set_trace()
#from flask import Markup
#from flask import Flask, render_template
#import os
#import mimetypes
# -*- coding: utf-8 -*-
#app = Flask(__name__)
#print(Flask(__name__)
#@app.route('/')
#def application(environ,start_response):
# -*- coding: utf-8 -*-
 #   status = '200 OK'
        #response_header = [('Content-type','text/html')]
#'<meta content="image/svg+xml;charset=utf-8" http-equiv="Content-Type">\n' \
#print("Content-type: text/html\n")
#print('<html>')
#print('<HEAD>')
#print('</meta>')
#print('<meta charset="UTF-8">')
#print('</meta>')
#print('</HEAD>')
#print('<body>')
#print('<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">')
#print('Provo River CFS Flows:')
#print('</div>')
#print('<img src="/static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="provoriverflows.com/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="/static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('<img src="/static/images/lower_and_middle_provo_plusdeerdreek.jpg" alt="/static Lower and Middle provo plus Deer Creek flows for past 7 days"/>')
#print('</body>')
#print('</html>')
#    mimetypes.add_type('image/svg+xml','.svg')
    #html = bytes(html,encoding = 'utf-8')
#    html = bytes(html,encoding = 'utf-8') #html.encode('utf-8')
#    img = 'static/images/Lower_and_Middle_Provo_PlusDeerCreek.svg'
#    response_header = [('Content-type','image/svg+xml'), ('mimetype','image/svg+xml')]
#    response_header = [('mimetype','image/svg+xml')]
 #   start_response(status,response_header)
#    full_filename = '/static/Lower_and_Middle_Provo_PlusDeerCreek.svg'
#    mimetypes.add_type('image/svg+xml','.svg')
#response_header = [('Content-type','text/html')]
#,('mimetype','image/svg')]
#    start_response(status,response_header)
#    return [html]
#    with app.app_context():
#       return render_template("index.html", user_image = full_filename)
       #return render_template(html, user_image = full_filename)
    #return render_template("index.html", user_image = full_filename)
