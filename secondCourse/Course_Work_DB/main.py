from pymongo import MongoClient
import csv
#
#
# window = Tk()
# window.title("WebPages analysis")
#
# b1 = Button(text="Зчитати дані та записати в БД", command=load_data_todb)
# b1.grid(row=0, column=0)
#
# b2 = Button(text="Analysis of companies that hosted sites", command=hostedBy)
# b2.grid(row=1, column=0)
#
# b3 = Button(text="Websites analysis", command=website)
# b3.grid(row=2, column=0)
#
# b4 = Button(text="Likes based on pageviews", command=likes)
# b4.grid(row=3, column=0)
#
#
# b5 = Button(text="Traffic Rank based on daile pageviews per user", command=TrafficRank)
# b5.grid(row=4, column=0)
#
#
# b6 = Button(text="Month average of daily_pageviews", command=Month_Average)
# b6.grid(row=5, column=0)
#
#
# if __name__ == '__main__':
#     window.mainloop()

# def pandasFunction():
#     data = pandas.read_csv('L:\KPI\DataBase\Second_Course\Course_Work_DB\Web_Scrapped_websites.csv')
#     data.head()
#
#
# def read_mongo():
#     """ Read from Mongo and Store into DataFrame """
#     client = MongoClient('localhost', 27017)
#     db = client.db
#
#     query = {}
#     no_id = True
#
#     # Make a query to the specific DB and Collection
#     data = db.webCollection.find(query)
#
#     # Expand the cursor and construct the DataFrame
#     dataframe =  pandas.DataFrame(list(data))
#     pandas.to_numeric(dataframe, errors='ignore')
#     dataframe_neededInfo = pandas.DataFrame(dataframe, colums=['Facebook_likes', 'Daily_Pageviews'])
#     data_sorted = dataframe_neededInfo.sort_values(['Facebook_likes'], descending = True)
#     data_sorted.set_index("Facebook_likes", inplace=True)
#
#     data_sorted.plot()
#     plt.show()
#
#     # Delete the _id
#     if no_id:
#         del dataframe['_id']
#
#     return dataframe
#
#
def read_mongo():
    client = MongoClient('localhost', 27701)
    db = client.courseworkdb

    with open('L:\KPI\DataBase\Second_Course\Course_Work_DB\Web_Scrapped_websites.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            db.webPages.insert({'Country_Rank': row[0],
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

if __name__ == '__main__':
    read_mongo()
#
