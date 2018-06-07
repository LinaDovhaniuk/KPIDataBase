import pandas
import seaborn
import brewer2mpl
import matplotlib.pyplot as plt

def hostedBy_analysis(db):
    cursor = db.getAll()
    data = pandas.DataFrame(list(cursor))
    sepeated = ['Google Inc.','Facebook','Yahoo! Inc.', 'CloudFlare', 'Akamai Technologies', 'Amazon Technologies Inc.', 'Microsoft Corporation','Fastly',
                'DataLine Ltd', 'Total Uptime Technologies', 'Hetzner Online GmbH',
                'Twitter Inc.', '"Automattic',
                '"NTT America',
                '"Hosting Services', 'Fornex Hosting S.L.', 'Facebook',
                'OVH SAS', 'WEBSITEWELCOME.COM',
                '"Limited Liability Company ""Ivi.ru"""']

    for hostedBy in sepeated:
        df = data['Hosted_by'].str.contains(hostedBy).fillna(False)
        seaborn.countplot(x='Daily_Pageviews_per_user' , data = data[df], palette="Greens_d")
        plt.title(hostedBy)
        plt.show()

def hostedBy_Top_analysis(db):
    cursor = db.getHostedByCount()
    data = pandas.DataFrame(list(cursor))[:10]
    plt.pie(data['count'], labels=data['_id'], autopct='%1.1f%%')
    plt.title('TOP 10 OF SERVICES FOR HOSTING')
    plt.show()

# def hostedBy_on_sites(db):
#     cursor = db.getHostedByToSites()
#     data = pandas.DataFrame(list(cursor))
#     seaborn.stripplot(x="Service", y="Sites", data=data, jitter=True)
#     plt.show()

# def website_analysis(db):
#     curor = db.getSitesCount()
#     data = pandas.DataFrame(list(cursor))[:10]
#     plt.pie(data['count'], labels = data['_id'], autopct='%1.1f%')
#     plt.title('TOP 10 COMPANIES HOSTEDBY')
#     plt.show()

def likes_on_views(db):
    cursor = db.getAll()
    data = pandas.DataFrame(list(cursor))
    sepeated = ['Google Inc.', 'Akamai Technologies',
                'Amazon Technologies Inc.', 'Fastly',
                'Hetzner Online GmbH'
                ]
    # data = pandas.DataFrame({'hostedBy' : sepeated, 'numbers' : list(cursor)})


    for hostedBy in sepeated:
        df = data['Hosted_by'].str.contains(hostedBy).fillna(False)
        seaborn.countplot(x='Child_Safety', data=data[df], palette="Greens_d")
        plt.title(hostedBy)
        plt.show()
        # dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 7).mpl_colors
        # # df = data['Hosted_by'].str.contains(hostedBy).fillna(False)
        # plt.subplot(aspect=True)
        # plt.pie(data, labels=data.index.values, colors=dark2_colors[0:9])
        # plt.title(hostedBy)
        # plt.show()


def likes_on_2_views(db):

    cursor = db.getLikesAndDailyPageViews()
    data_set = pandas.DataFrame(list(cursor))
    data = data_set.apply(pandas.to_numeric, errors='ignore')
    seaborn.countplot(x="Facebook_likes", data=data)
    plt.show()


def getTrafficRank_on_DailyPageViewsPerUser(db):
    cursor = db.getTrafficRankAndDailyPageViewsPerUser()
    data_set = pandas.DataFrame(list(cursor))
    data = data_set.apply(pandas.to_numeric, errors='ignore')
    seaborn.stripplot(x="Traffic_Rank" , y="Daily_Pageviews_per_user", data=data)
    plt.show()



# def getMonth_Average_Daily_Reach_plot(db):
#     cursor = db.getAll()
#     data = pandas.DataFrame(list(cursor))
#     sepeated = ['0.308544', '2.01696', '0.265728', '0.000063', '0.10176', '0.092285', '0.037219', '0.24288', '0.112224']
#
#     for hostedBy in sepeated:
#         df = data['Month_Average_Daily_Pageviews'].str.contains(hostedBy).fillna(False)
#         seaborn.distplot(data['Month_Average_Daily_Pageviews'], hist=False, rug=True)
#
#         # seaborn.countplot(x='Daily_Pageviews_per_user', data=data[df], palette="Greens_d")
#         plt.show()
#     # cursor = db.getMonth_Average_Daily_Reach()
#     # data_set = pandas.DataFrame(list(cursor))
#     # data = data_set.apply(pandas.to_numeric, errors='ignore')
#     # seaborn.distplot(data['Month_Average_Daily_Pageviews'], hist=False, rug=True)
#     # plt.show()
        
