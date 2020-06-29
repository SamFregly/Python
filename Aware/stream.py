#Import the necessary methods from tweepy library
import ssl
from datetime import date 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas
from textblob import TextBlob
from cryptography.fernet import Fernet

#Variables that contains the user credentials to access Twitter API 
access_token ="3648600621-Qr0HWRdUZ4GP7bwk6nzbIFmdriflsgNcqR22gS8"
access_token_secret ="5C9QBwYz8HSw3EhjarMVl0oj4TooAbugkgrjNA4MSCYWc"
consumer_key ="Pz9OLoKLvyr496hZOfS0S5p0l"
consumer_secret ="Vx29mWbIACRRqeTPuBSNAvDA9poWUFy37MnfurpZ19nsCqvvlJ"
today = date.today().strftime("%d-%m-%Y")
filen = 'D:\datasets\Twitter\{}export.json'.format(today)
file_out = open(filen,"wb+")

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    

    def on_error(self, status):
        file_out.close()
        print(status)
    

    ##def _data(self, data):        # only needed for meta data on all twitter events
     #   if self.listener.on_data(data) is False:  # on_status will give status updates only
     #       self.running = False    

    def on_status(self, status): 
        try:
            if status.retweeted_status == True:
                return
        except AttributeError:
            return True
            #print(int('ab'))
        else:
            loc = status.user.location
            user_description = status.user.description
            text = status.text
            coords = status.coordinates
            user_name = status.user.screen_name
            user_created_tm = status.user.created_at
            follower_ct = status.user.followers_count
            id_str = status.id_str
            created_tm = status.created_at
            retweet_ct = status.retweet_count
            bg_color = status.user.profile_background_color
            blob = TextBlob(text)
            sent = blob.sentiment
            text = text.encode('utf-8')
            #print(sent,'##############')
            polarity = sent.polarity
            subjectivity = round(sent.subjectivity,12)
            output = user_description,loc,coords,text,user_name,user_created_tm,follower_ct,id_str,created_tm,retweet_ct,bg_color,polarity,subjectivity
            out1 = str(output)+"\n\n"
            out1 = out1.encode('utf-8')
            print(out1)
            #output.encode('utf8') 
            file_out.write(out1)
          


    def assign_variables():        
        return True
      
    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        return       

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
#stream()
stream.filter(track = ['covid','corona','virus'],languages = ['en'])
