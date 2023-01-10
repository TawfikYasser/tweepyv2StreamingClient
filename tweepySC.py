import sys
import socket
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

## Extract the text from the tweet object and send it to port
class TweetsHandler(tweepy.StreamingClient):

    def __init__(self, bearer_token, socket):
        print ("Tweets handler initialized")
        self.client_socket = socket
        super().__init__(bearer_token)

    # This function gets called when the stream is working
    def on_connect(self):
        print("Connected")

    def on_tweet(self, tweet):
        try:
            if tweet.referenced_tweets == None:
                msg = tweet.text.encode("utf-8")
                self.client_socket.send(msg)

        except BaseException as e:
            print('ERROR: ',e)
        return True

    def on_error(self, status):
        print('on_error msg: ',status)
        return True
    
    
### End of Class ###

def connect_to_twitter(connection, tracks):

    # write your own keys
    api_key = ""
    api_secret = ""
    bearer_token = ""
    access_token = ""
    access_token_secret = ""

    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = TweetsHandler(socket=connection, bearer_token=bearer_token)
    for term in tracks:
        stream.add_rules(tweepy.StreamRule(term))

    # Starting streams
    stream.filter(tweet_fields=["referenced_tweets"])

############################################

host = "localhost"
port = 9948
tracks = sys.argv[1:]

s = socket.socket()
s.bind((host, port))

print("Listening on port: %s" % str(port))
#5 the "backlog" which is the number of unaccepted connections that the system will allow before refusing new connections
s.listen(5)

connection, client_address = s.accept()

print("Received request from: " + str(client_address))
print("Initializing listener for these tracks: ", tracks)

connect_to_twitter(connection, tracks)
