##############################################
##############################################
#      Sandy School Tweets Monitor           # 
#      Dimas Rinarso Putro | drp354@nyu.edu  #
#      Urban Science Intensive               #
##############################################
#Consumer Key (API Key)	11jjIaDtu65d7i0Otw6Xk6SGl
#Consumer Secret (API Secret) u8ejLMzmHAJgS34eXDf4UGGwuul2QianbIeTqfqCFPi8RJSXmI

import tweepy
import matplotlib.pyplot as plt
import csv
import shapefile
import sys
from bokeh.plotting import *
from bokeh.sampledata.iris import flowers


#tweepy and twitter API
CONSUMER_KEY = '11jjIaDtu65d7i0Otw6Xk6SGl'
CONSUMER_SECRET = 'u8ejLMzmHAJgS34eXDf4UGGwuul2QianbIeTqfqCFPi8RJSXmI'
ACCESS_KEY = '3051641614-P5iZKOwJISpMS6SA5W4t4un63piXofipftevtL7'
ACCESS_SECRET = 'yx2FLAdH4dXVLvmaMtCog5hF2xthFUjemQdGUSYLhxayM'
# setup authorization
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Global map Parameter
twodim = []
center = []
xmin = -74.3 
xmax = -73.6
ymax = 40.92 
ymin = 40.46 


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True 

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True 

# init lists for mapping per dimension N
def initTwoDim(n):
	for i in range(n):
		twodim.append([])
		center.append([])
		for j in range(n):
			twodim[i].append(0) 
			center[i].append((0,0))
	return None

# mapping tweets location per dimension N  
def mapTwoDim(p,n):
	winx = (xmax-xmin)/n
	winy = (ymax-ymin)/n
	x = (p[0]-xmin)/(xmax-xmin)
	y = (p[1]-ymin)/(ymax-ymin)
	index_x = int(x * n)
	index_y = int(y * n)
	twodim[index_x][index_y] += 1
	center[index_x][index_y] = (float(xmin+(index_x*winx)+(0.5*winx)),float(ymin+(index_y*winy)+(0.5*winy)))   
	return None

# Function to fetch user's timeline data
def printTweetStream():
	sandyStream = tweepy.streaming.Stream(auth, CustomStreamListener())    
	sandyStream.filter(locations=[-74,40,-73,41])

def printTweetTimeRange(n): 
	lat = []
	lng = [] 
	num = []
	initTwoDim(n)

	csvFile = open('output.csv', 'a')
	csvWriter = csv.writer(csvFile)
 	runTweet  =  tweepy.Cursor(api.search,q="the",since="2015-02-17",until="2015-02-21",lang="en",geocode="40.78,-73.8,30mi").items()
 	tweetCount = -1
 	while True:
		try:
			c = runTweet.next()
			if c.coordinates:
				print 'coords:', c.coordinates['coordinates']
	 			csvWriter.writerow([c.created_at, c.coordinates,c.text.encode('utf-8')])
	 			longitude = float(c.coordinates['coordinates'][0])
	 			latitude = float(c.coordinates['coordinates'][1])
	 			#check if within new york area
	 			if longitude < xmax and longitude > xmin and latitude < ymax and latitude > ymin:
			 	 	tweetCount += 1
	 				points = (longitude,latitude)
					mapTwoDim(points,n)
					if tweetCount == 1000: break

		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break

	for i in range(n):
		for j in range(n):
			if twodim[i][j] !=0:
				lng.append(center[i][j][0])
				lat.append(center[i][j][1])
				num.append(twodim[i][j])
			else:
				pass


	return {'lat_list': lat, 'lng_list': lng, 'num_dots': num}


def setMarkerSize(complaints):
	outputSize = []
	outputOpac = []
	minSize = 3
	maxSize = 12
	minComp= min(complaints) 
	maxComp= max(complaints) 
	print minComp, maxComp

	if minComp != maxComp:
		for item in complaints:
			normSize = int((float(item-minComp)/(maxComp-minComp))*(maxSize-minSize))+minSize
			outputSize.append(normSize)
			#set opacity 
			#set to off to simplify matters
			"""
			if normSize >=3 and normSize<6:
				outputOpac.append(0.1)
			elif normSize >=6 and normSize<9:
				outputOpac.append(0.3)
			elif normSize >=9:
				outputOpac.append(0.6)
			"""
			outputOpac.append(0.7)
	else:
		for item in complaints:
			outputSize.append(3)
			outputOpac.append(0.7)

	return outputSize,outputOpac

def getZipBorough(zipBoroughFilename):
	# Reads all complaints and keeps zips which have complaints.
	with open(zipBoroughFilename) as f:
		csvReader = csv.reader(f)
		csvReader.next()
		return {row[0]: row[1] for row in csvReader}

def drawPlot(shapeFilename, mapPoints, zipBorough):
	# Read the ShapeFile
	dat = shapefile.Reader(shapeFilename)

	# Creates a dictionary for zip: {lat_list: [], lng_list: []}.
	zipCodes = []
	polygons = {'lat_list': [], 'lng_list': []}

	record_index = 0

	for r in dat.iterRecords():
		currentZip = r[0]

		# Keeps only zip codes in NY area.
		if currentZip in zipBorough:
			zipCodes.append(currentZip)
			shape = dat.shapeRecord(record_index).shape
			points = shape.points

			# Breaks into lists for lat/lng.
			lngs = [p[0] for p in points]
			lats = [p[1] for p in points]

			# Stores lat/lng for current zip shape.
			polygons['lng_list'].append(lngs)
			polygons['lat_list'].append(lats)

		record_index += 1

	#process the size
	sizes, alp = setMarkerSize(mapPoints['num_dots']) 

	# Creates the Plot
	output_file("shapeAndPoints.html", title="shape and points example")
	# hold()

	TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"

	# Creates the polygons.
	patches(polygons['lng_list'], polygons['lat_list'], \
			fill_color='#C8C6C4', line_color="gray", \
			tools=TOOLS, plot_width=1100, plot_height=700, \
			title="Twitter posts during Sandy")

	# Draws mapPoints on top of map.
	hold()

	#TODO: Apply transformation to lat/lng points: all fall in the same
	#position on the map.
	scatter(mapPoints['lng_list'], mapPoints['lat_list'],
			fill_color='#00A368',color='#00A368', fill_alpha=alp, 
			line_alpha=alp, size=sizes, name="mapPoints")
	show()


# Getting argument from user's command line input
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'Usage:'
		print sys.argv[0] \
		+ ' <numberofwindow> <zipboroughfilename> <shapefilename>'
		print '\ne.g.: ' + sys.argv[0] \
		+ ' 100 zip_borough.csv data/nyshape.shp'
	else:
		mapPoints = printTweetTimeRange(int(sys.argv[1]))
		zipBorough = getZipBorough(sys.argv[2])
		drawPlot(sys.argv[3], mapPoints, zipBorough)
