##############################################
##############################################
#      Sandy School Tweets Monitor           # 
#      Dimas Rinarso Putro | drp354@nyu.edu  #
#      No.3                                  #
##############################################
#Consumer Key (API Key)	11jjIaDtu65d7i0Otw6Xk6SGl
#Consumer Secret (API Secret) u8ejLMzmHAJgS34eXDf4UGGwuul2QianbIeTqfqCFPi8RJSXmI

import tweepy
import nltk
import matplotlib.pyplot as plt
import numpy as np


# Global Parameter
CONSUMER_KEY = '11jjIaDtu65d7i0Otw6Xk6SGl'
CONSUMER_SECRET = 'u8ejLMzmHAJgS34eXDf4UGGwuul2QianbIeTqfqCFPi8RJSXmI'
ACCESS_KEY = '3051641614-P5iZKOwJISpMS6SA5W4t4un63piXofipftevtL7'
ACCESS_SECRET = 'yx2FLAdH4dXVLvmaMtCog5hF2xthFUjemQdGUSYLhxayM'

# setup authorization
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True 

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True 


# Function to fetch user's timeline data
def printTweet():
	sandyStream = tweepy.streaming.Stream(auth, CustomStreamListener())    
	sandyStream.filter(locations=[-74,40,-73,41])

def main():
	printTweet()


# Getting argument from user's command line input
if __name__ == '__main__':
	main()

	"""
  if len(sys.argv) != 6:
    print 'Usage:'
    print sys.argv[0] \
    + ' <numberofwindow> <complaintsfilename> <zipboroughfilename> <shapefilename> <username>'
    print '\ne.g.: ' + sys.argv[0] \
    + ' data/nyshape.shp 100 data/complaints.csv zip_borough.csv username'
  else:
  	username = sys.argv[5]
    mapPoints = loadComplaintsPoints(sys.argv[2],int(sys.argv[1]))
    zipBorough = getZipBorough(sys.argv[3])
    drawPlot(sys.argv[4], mapPoints, zipBorough)
    """
