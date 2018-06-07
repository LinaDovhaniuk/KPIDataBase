from analysis import *
from get_data import Database

db = Database()


# def load_data_todb():
#     db.writeDataStreamWise(clean_data(download_data()))


def hostedBy():
    hostedBy_analysis(db)


def topHostedBy():
    hostedBy_Top_analysis(db)


def likes():
    likes_on_views(db)

def host_site():
    hostedBy_on_sites(db)
#
#
# def TrafficRank():
#     getTrafficRank_on_DailyPageViewsPerUser(db)


# def Month_Average():
#     getMonth_Average_Daily_Reach_plot(db)

