import hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from textblob import TextBlob
from datetime import datetime, timedelta
from pytrends.request import TrendReq


news_api_key = '46b12d445c11418e8711a4e34889a675'
reddit_api_id = 'yeA7B3vkMUk1Jw'
reddit_api_secret = 'wR2C-76iL_2W7YCs5s82t2nj9FA'
reddit_username = 'Financial_Suit'
reddit_password = 'Ilovesuits1[]'
coinbase_passphrase = 'lavenderluckystrike'
coinbase_secret = '8fe4802ae9750a8705eb383d81ec925f'
coinbase_api_key = 'AU1Zr/eDeIsnere8E4ExLbugjZVq+7Liv5wd1D3Bm16PZ933n5as0Co6B0KTvnIN/Jm1oaZraopI21c88lr9QA=='


class CoinbaseAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class DataMiner():

    def __init__(self, date):
        self.date = date
        self.search_pop = None
        self.news_articles = None
        self.news_sentiment = None
        self.reddit_posts = None
        self.reddit_sentiment = None
        self.btc_price = None

    def __call__(self):
        # date, search popularity, number of news articles, btc price
        self.row = [self.date, self.search_pop, self.news_articles, self.news_sentiment, self.reddit_posts, self.reddit_sentiment, self.btc_price]


    # News API data
    def btc_news_query(self):
        if self.date is not None:
            # get single day results
            fromdate = 'from=' + self.date
            todate = 'to=' + self.date
            headers = {'X-Api-Key': news_api_key}
            url = 'https://newsapi.org/v2/everything?q=bitcoin&from=' + fromdate + "&to=" + todate
            response = requests.get(url, headers=headers)
            response = response.json()
            return response['totalResults']
        else:
            raise TypeError('Must supply date to btc_query')

    def good_news_bad_news(self):
        if self.date is not None:
            # get top articles from that day
            fromdate = 'from=' + self.date
            todate = 'to=' + self.date
            headers = {'X-Api-key': news_api_key}
            url = ('https://newsapi.org/v2/everything?'
                   'q=+bitcoin&'
                   'sortBy=popular&'
                   'pagesize=100&'
                   'from=' + fromdate + '&'
                   'to=' + todate + '&'
                   'language=en')
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response = response.json()
                count = 0
                polarity = 0
                subjectivity = 0
                if response['articles']:
                    for article in response['articles']:
                        # do text blob stuff
                        description = article['description']
                        if description is not None:
                            description = TextBlob(description)
                            for sentence in description.sentences:
                                count += 1
                                polarity += sentence.polarity
                                subjectivity += sentence.subjectivity
                    avgpolarity = (polarity/count)
                    avgsubjectivity = (subjectivity/count)
                    return avgpolarity, avgsubjectivity
                else:
                    return polarity, subjectivity
            else:
                return "Invalid API request"
        else:
            raise TypeError('Must supply a date to good_news_bad_news')

    # Coinbase API data
    def get_btc_price(self):
        datetimeobj = datetime.strptime(self.date, '%Y-%m-%d')
        enddate = datetimeobj + timedelta(days=1)
        enddate = datetime.strftime(enddate, '%Y-%m-%d')
        api_url = 'https://api.pro.coinbase.com/'
        auth = CoinbaseAuth(coinbase_api_key, coinbase_secret, coinbase_passphrase)
        url = api_url + '/products/BTC-USD/candles?start=' + self.date + '&end=' + enddate + '&granularity=3600'
        request = requests.get(url, auth=auth)
        data = request.json()
        total = 0
        for candle in data:
            total += candle[1]
            total += candle[2]
        avg = total/(2*(len(data)))
        return avg
    
    def get_btc_spread(self):
        datetimeobj = datetime.strptime(self.date, '%Y-%m-%d')
        enddate = datetimeobj + timedelta(days=1)
        enddate = datetime.strftime(enddate, '%Y-%m-%d')
        api_url = 'https://api.pro.coinbase.com/'
        auth = CoinbaseAuth(coinbase_api_key, coinbase_secret, coinbase_passphrase)
        url = api_url + '/products/BTC-USD/candles?start=' + self.date + '&end=' + enddate + '&granularity=86400'
        request = requests.get(url, auth=auth)
        data = request.json()
        low = data[0][1]
        high = data[0][2]
        return low, high

    # Get reddit token
    def get_reddit_token(self):
        client_auth = requests.auth.HTTPBasicAuth(reddit_api_id, reddit_api_secret)
        post_data = {"grant_type": "password", "username": reddit_username, "password": reddit_password}
        headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        url = "https://www.reddit.com/api/v1/access_token"
        response = requests.post(url, auth=client_auth, data=post_data, headers=headers)
        return response.json()['access_token']

    # use reddit token and search for btc posts
    def search_reddit(self):
        headers = {"Authorization": "bearer " + self.get_reddit_token(), "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.get("https://oauth.reddit.com/search?q=bitcoin&t=day&sort=top", headers=headers)
        posts = (response.json()['data']['children'])
        polarity = 0
        subjectivity = 0
        count = 0
        for post in posts:
            count += 1
            title = TextBlob(post['data']['title'])
            polarity += title.polarity
            subjectivity += title.subjectivity
        avgpolarity = (polarity/count)
        avgsubjectivity = (subjectivity/count)
        return avgpolarity, avgsubjectivity

    # Google Trends data
    def get_gtrends_data(self):
        # create pytrends object
        pytrends = TrendReq(hl='en-US', tz=480)
        keyword_list = ["bitcoin"]
        pytrends.build_payload(keyword_list, cat=0, timeframe='now 1-d', geo='', gprop='')
        interest = pytrends.interest_over_time()
        mean = (interest["bitcoin"].mean())
        return mean
