#!/usr/bin/python3
import pymysql

class Predictions:

    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", password="root", port=3307)
        self.cursor = self.db.cursor()
        self.cursor.execute("""USE crypto_predicto""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS btc_predictions_staging (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ltc_predictions_staging (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS eth_predictions_staging (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS xrp_predictions_staging (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS btc_predictions (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ltc_predictions (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS eth_predictions (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS xrp_predictions (actual_price VARCHAR(20), date_created VARCHAR(10), prediction VARCHAR(20))""")
        self.prediction_data = "prediction_data/"

    def get_btc_predictions(self):

        with open(self.prediction_data + "bitcoin_predictions.csv", 'r') as btc_predictions:
            list_of_tuples = []
            btc_predictions = iter(btc_predictions)
            next(btc_predictions)
            for line in btc_predictions:
                date, price, price_prediction = line.split(',')
                price = price.strip()
                price_prediction = price_prediction.strip()
                date = date.strip()
                tuple_data = (price, date, price_prediction)
                list_of_tuples.append(tuple_data)
            self.cursor.executemany("""INSERT INTO btc_predictions_staging (actual_price, date_created, prediction) VALUES (%s, %s, %s) """, list_of_tuples)
            self.db.commit()

    def get_ltc_predictions(self):
        with open(self.prediction_data + "litecoin_predictions.csv", 'r') as ltc_predictions:
            list_of_tuples = []
            ltc_predictions = iter(ltc_predictions)
            next(ltc_predictions)
            for line in ltc_predictions:
                date, price, price_prediction = line.split(',')
                price = price.strip()
                price_prediction.strip()
                date = date.strip()
                tuple_data = (price, date, price_prediction)
                list_of_tuples.append(tuple_data)
            self.cursor.executemany("""INSERT INTO ltc_predictions_staging (actual_price, date_created, prediction) VALUES (%s, %s, %s)""", list_of_tuples)
            self.db.commit()

    def get_eth_predictions(self):
        with open(self.prediction_data + "ethereum_predictions.csv", 'r') as eth_predictions:
            list_of_tuples = []
            eth_predictions = iter(eth_predictions)
            next(eth_predictions)
            for line in eth_predictions:
                date, price, price_prediction = line.split(',')
                price = price.strip()
                price_prediction = price_prediction.strip()
                date = date.strip()
                tuple_data = (price, date, price_prediction)
                list_of_tuples.append(tuple_data)
            self.cursor.executemany("""INSERT INTO eth_predictions_staging (actual_price, date_created, prediction) VALUES (%s, %s, %s)""", list_of_tuples)
            self.db.commit()

    def get_xrp_predictions(self):
        with open(self.prediction_data + "xrp_predictions.csv", 'r') as xrp_predictions:
            list_of_tuples = []
            xrp_predictions = iter(xrp_predictions)
            next(xrp_predictions)
            for line in xrp_predictions:
                date, price, price_prediction = line.split(',')
                price = price.strip()
                price_prediction = price_prediction.strip()
                date = date.strip()
                tuple_data = (price, date, price_prediction)
                list_of_tuples.append(tuple_data)
            self.cursor.executemany("""INSERT INTO xrp_predictions_staging (actual_price, date_created, prediction) VALUES (%s, %s, %s)""", list_of_tuples)
            self.db.commit()

    def dump_predictions(self):
        self.cursor.execute("""SELECT * FROM btc_predictions""")
        data = self.cursor.fetchall()
        print(data)

    def cycle_tables(self):
        rename_btc = "RENAME TABLE btc_predictions TO btc_backup, btc_predictions_staging TO btc_predictions"
        rename_ltc = "RENAME TABLE ltc_predictions TO ltc_backup, ltc_predictions_staging TO ltc_predictions"
        rename_eth = "RENAME TABLE eth_predictions TO eth_backup, eth_predictions_staging TO eth_predictions"
        rename_xrp = "RENAME TABLE xrp_predictions TO xrp_backup, xrp_predictions_staging TO xrp_predictions"
        delete_tables = "DROP TABLE btc_backup, ltc_backup, eth_backup, xrp_backup"
        self.cursor.execute(rename_btc)
        self.cursor.execute(rename_ltc)
        self.cursor.execute(rename_eth)
        self.cursor.execute(rename_xrp)
        self.cursor.execute(delete_tables)
        self.db.commit()

    def close_db(self):
        self.db.commit()
        self.db.close()

prediction = Predictions()
prediction.get_btc_predictions()
prediction.get_ltc_predictions()
prediction.get_eth_predictions()
prediction.get_xrp_predictions()
prediction.cycle_tables()
prediction.close_db()