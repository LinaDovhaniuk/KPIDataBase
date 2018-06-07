

from tkinter import Tk, Button
from get_data import *
from viewCommands import *


window = Tk()
window.title("WebPages analysis")


b1 = Button(text="Analysis of companies that hosted sites", command=hostedBy)
b1.grid(row=1, column=0)


b2 = Button(text="Child safety", command=likes)
b2.grid(row=2, column=0)

b3 = Button(text = "Get Top of services", command=topHostedBy)
b3.grid(row=3,column=0)

# b4 = Button(text = "Get Services of hosting", command=host_site)
# b4.grid(row=4,column=0)


# b5 = Button(text="Traffic Rank based on daile pageviews per user", command=TrafficRank)
# b5.grid(row=4, column=0)


# b6 = Button(text="Month average of daily_pageviews", command=host_site)
# b6.grid(row=5, column=0)


if __name__ == '__main__':
    window.mainloop()
