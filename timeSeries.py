import argparse,csv, sys, os
from datetime import date,datetime,timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
from collections import OrderedDict,defaultdict
import matplotlib
print (matplotlib.__version__)
plt.style.use('ggplot')
get_ipython().magic(u'matplotlib inline')

csv_filename = "csv/2012.csv"
num = 1
sDate =  "2012/10/01-00:00:00"
eDate =  "2012/11/30-23:59:00"


# Sandy affected zipcodes:
affectedZipCodes = [11109,
                    11224,
                    11697,
                    11694,
                    11692,
                    11235,
                    11414,
                    11693,
                    11371,
                    11251,
                    10004,
                    11430,
                    11691,
                    11231,
                    10305,
                    10009,
                    10303,
                    10005,
                    10306,
                    11234,
                    11214,
                    11236,
                    10038,
                    11422,
                    10464,
                    10014,
                    10280,
                    10002,
                    11223,
                    11222,
                    10314,
                    10037,
                    10013,
                    10454,
                    11356,
                    10044,
                    11367,
                    10029,
                    10007,
                    10011,
                    10307,
                    10001,
                    10010,
                    11101,
                    11229,
                    11232,
                    10035,
                    11368,
                    11413,
                    11363,
                    10039,
                    11211,
                    11359,
                    10016,
                    10465,
                    11201,
                    11102,
                    11239,
                    10455,
                    10308,
                    10309,
                    10451,
                    10018,
                    11106,
                    10023,
                    10034,
                    10128,
                    10474,
                    10475,
                    10453,
                    10019,
                    10310,
                    10463,
                    11434,
                    11237,
                    11354,
                    10301,
                    11209,
                    10031,
                    11105,
                    10473,
                    11220,
                    10040,
                    10461,
                    11215,
                    11362,
                    11378,
                    10452,
                    10033,
                    10302,
                    11361,
                    10036,
                    10032,
                    10312,
                    10024,
                    11217,
                    10022,
                    11228,
                    10021,
                    11208,
                    11360,
                    10462,
                    10027,
                    10304,
                    10468,
                    11207,
                    10471,
                    10472,
                    10459,
                    10017,
                    11357,
                    11420,
                    10460,
                    10012,
                    10028,
                    11206,
                    10469,
                    11355,
                    11205,
                    11385,
                    11203,
                    11375,
                    11364]


def daterange(startDate, endDate):
  for n in range(int ((endDate - startDate).days)):
    yield startDate + timedelta(n)


data = {}
dataZip = {}
sumOpenComplaint = {}

#limit start and end time    
startDate = datetime.strptime(sDate,"%Y/%m/%d-%H:%M:%S")
endDate = datetime.strptime(eDate,"%Y/%m/%d-%H:%M:%S")
  
#Reading the files
with open(csv_filename, 'rb') as f:
  csvReader = csv.reader(f)
  headers = next(csvReader)

  for row in csvReader:
    try:
        createdDate = row[1]
        closedDate = row[2]
        complaintType = row[5].rstrip()
        zipCode = int(row[8])

        if zipCode in affectedZipCodes:

            curDate = datetime.strptime(createdDate,"%m/%d/%Y %I:%M:%S %p")
            cloDate = datetime.strptime(closedDate,"%m/%d/%Y %I:%M:%S %p")

            #if curDate>=startDate and curDate<=endDate:                
            if curDate>=startDate and curDate<=endDate and (complaintType == 'APPLIANCE' \
                       or complaintType == 'Building Condition' \
                       or complaintType == 'Building/Use'\
                       or complaintType == 'Construction'\
                       or complaintType == 'ELECTRIC' \
                       or complaintType == 'Electrical' \
                       or complaintType == 'HEATING' \
                       or complaintType == 'Maintenance or Facility' \
                       or complaintType == 'Mold' \
                       or complaintType == 'OEM Literature Request' \
                       or complaintType == 'Tunnel Condition' \
                       or complaintType == 'Water System' \
                       or complaintType == 'Water System  '):
              
              for singleDate in daterange(curDate, cloDate):

                  singDateStr = singleDate.strftime("%Y/%m/%d")

                  if zipCode in data:
                    if singDateStr in data[zipCode]:
                      data[zipCode][singDateStr] += 1
                      sumOpenComplaint[zipCode] += 1
                    else:
                      data[zipCode][singDateStr] = 1
                      sumOpenComplaint[zipCode] += 1
                  else:
                    data[zipCode] = {}
                    data[zipCode][singDateStr] = 1
                    sumOpenComplaint[zipCode]=1

            else:
                pass

        else:
            pass

    except:
        pass

f.close()

#sorting from the top-k complaint
sumOpenComplaintSorted = sorted(sumOpenComplaint.iteritems(), key=lambda x: (-x[1]))

#sorting date and appending into lists
zipName = []
x=[]
y=[]
index = 0
#set limit for number of max num
lenData = len(data)
#if num > lenData: num = lenData
num = lenData
ind = np.arange(num)

#iterate only for agency name that is in top-k
for elem in sumOpenComplaintSorted[:num]:
  #append agency name
  zipName.append(elem[0])
  x.append([])
  y.append([])

#iterating per-day data
for zipc in data:
  data[zipc]= OrderedDict(sorted(data[zipc].items(), key=lambda x: (x[0])))
  #iterating into lists
  for iterdate, counts in data[zipc].iteritems():
    iterdateNum = dates.datestr2num(iterdate)
    x[index].append(iterdateNum)
    y[index].append(counts)
  index+=1

#line plot variable
title = "Sandy recovery time distribution based on 311 open data %s - %s" % (sDate,eDate)
#colorlist = np.random.random(len(x))
#colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
colors = ('#EA5455','#8743D4', '#66A7E1', '#45C966','#F4DF46','#E97F31','#7D7F72','#AE8E3B') 

lineType = 'r-'
lineWid=2

# Create plots with pre-defined labels.
plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
plt.title(title)

axisNum = 0
for n in xrange(0,num):
    axisNum += 1
    color = colors[axisNum % len(colors)]
    plt.plot_date(x[n], y[n], lineType, linewidth=lineWid, color=color, label=zipName[n], alpha = 1)
    #plt.fill_between(x[n], 0, y[n],alpha = 0.1, color = color)
    #plt.plot_date(x[n], y[n], lineType, linewidth=0.001, color='grey', label=zipName[n])



#plt.legend(loc='upper right', shadow=True, fontsize='x-small')
plt.grid(True)
plt.xlabel('Date')
plt.ylabel('Number of open complaints period')

#plt.savefig('recoveryDistribution-fill.png')
#plt.savefig('recoveryDistribution.png')
plt.show()
