from DataMiner import DataMiner
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

def getData(date):
    dataminer = DataMiner(date)
    goodnewsbadnews = dataminer.good_news_bad_news()
    redditsentiment = dataminer.search_reddit()
    btc_spread = dataminer.get_btc_spread()
    data = [[date, str(dataminer.get_btc_price()), str(dataminer.btc_news_query()), str(goodnewsbadnews[0]), str(goodnewsbadnews[1]), str(redditsentiment[0]), str(redditsentiment[1]), str(dataminer.get_gtrends_data()), str(btc_spread[0]), str(btc_spread[1])]]
    df = pd.DataFrame(data, columns=['Date', 'BTC_Price','Number_of_articles', 'news_sentiment', 'news_subjectivity', 'reddit_sentiment', 'reddit_subjectivity', 'google_trends', 'btc_low', 'btc_high'], dtype=str)
    my_csv = Path('/crypto-predicto/trainingdata.csv')
    if my_csv.is_file():
        df.to_csv('/crypto-predicto/trainingdata.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('/crypto-predicto/trainingdata.csv', mode='w', header=True, index=False)

date = datetime.today().strftime('%Y-%m-%d')
getData(date)