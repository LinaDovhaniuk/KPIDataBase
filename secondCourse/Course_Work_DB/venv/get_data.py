from pymongo import MongoClient
import csv
import json
import pandas
import sys, getopt, pprint
from schema import webpage

class Database:
    db = None

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['db'].collection

    def importDatatoMongo(self):
        client = MongoClient('localhost', 27017)
        db = client.db

        with open('L:\KPI\DataBase\Second_Course\Course_Work_DB\Web_Scrapped_websites.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                pass
            db.webCollection.insert({'Country_Rank': row[0],
                                     'Website': row[1],
                                     'Trustworthiness': row[2],
                                     'Avg_Daily_Visitors': row[3],
                                     'Child_Safety': row[4],
                                     'Avg_Daily_Pageviews': row[5],
                                     'Privacy': row[6],
                                     'Facebook_likes': row[7],
                                     'Twitter_mentions': row[8],
                                     'Google_pluses': row[9],
                                     'LinkedIn_mentions': row[10],
                                     'Pinterest_pins': row[11],
                                     'StumbleUpon_views': row[12],
                                     'Status': row[13],
                                     'Traffic_Rank': row[14],
                                     'Reach_Day': row[15],
                                     'Month_Average_Daily_Reach': row[16],
                                     'Daily_Pageviews': row[17],
                                     'Month_Average_Daily_Pageviews': row[18],
                                     'Daily_Pageviews_per_user': row[19],
                                     'Reach_Day_percentage': row[20],
                                     'Month_Average_Daily_Reach_percentage': row[21],
                                     'Daily_Pageviews_percentage': row[22],
                                     'Month_Average_Daily_Pageviews_percentage': row[23],
                                     'Daily_Pageviews_per_user_percentage': row[24],
                                     'Location': row[25],
                                     'Hosted_by': row[26],
                                     'Subnetworks': row[27],
                                     'Registrant': row[28],
                                     'Registrar': row[29],
                                     'country': row[30]})

    def writeDataStream(self, dataframe):
        for index, row in dataframe.iterrows():
            webpage_entry = webpage(row)
            self.db.insert_one(webpage_entry)

    def writeDataPackage(self, dataframe):
        list_of_enrties = []
        for index, row in dataframe.iterrows():
            webpage_entry = webpage(row)
            list_of_enrties.append(webpage_entry)
        self.db.insertMany(list_of_enrties)

    def getAll(self):
        return self.db.find()
    def getGoogle(self):
        return self.db.find({"Child_Safety" : "Good"})

    def getSitesCount(self):
        return self.db.aggregate([
            {"$group" : {"_id": '$Websites', "count" : {"$sum" : 1}}},
            {"sort" : {"count" : -1}}
        ])
    def getHostedByCount(self):
        return self.db.aggregate([
            {"$group" : {"_id": '$Hosted_by', "count" : {"$sum" : 1}}},
            {"$sort" : {"count" : -1}}
        ])

    # def getHostedByToSites(self):
    #     return self.db.find({}, {"Websites": 1, "Hosted_by": 1})

    def getLikesAndDailyPageViews(self):
        return self.db.find({},{"Child_Safety" : "Good", "Facebook_likes" : 1, "Daily_Pageviews" : 1})

    def getTrafficRankAndDailyPageViewsPerUser(self):
        return self.db.find({},{"Child_Safety" : "Good","Traffic_Rank" : 1, "Daily_Pageviews_per_user" : 1})

    def getMonth_Average_Daily_Reach(self):
        return self.db.find({"Month_Average_Daily_Pageviews":  [ '0.308544', '2.01696', '0.265728', '0.000063', '0.10176', '0.092285', '0.037219', '0.24288', '0.112224']})