from twython import TwythonStreamer

TWITTER_ACCESS_TOKEN = '3248261306-H77EHvXe48pbWdmzUawfoRhgGxQDm2VKFlnfacW'
TWITTER_ACCESS_SECRET = 'vTrQ1DrMzAfe2GXeNycVc6oagaz3JDGW5EweinnZytZhZ'
TWITTER_CONSUMER_TOKEN = 'ZuPoSR6v2UW9RRUM3jVNy4lXQ'
TWITTER_CONSUMER_SECRET = 'dMDpqXNxbcCwmTJQSAYCJkFfStpotj8ZDcka1CWbUmwdTzieK6'

class TwitterStream(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code

stream = TwitterStream(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN,
                        TWITTER_CONSUMER_TOKEN, TWITTER_CONSUMER_SECRET)
stream.statuses.filter(track='twitter')