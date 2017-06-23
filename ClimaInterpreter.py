import numpy as np
import datetime
import matplotlib.pyplot as plt 
from matplotlib.dates import SecondLocator, MinuteLocator, DayLocator, HourLocator, DateFormatter, drange


file = '/home/chrak/data/2017-06-18_first.log'
my_data = np.genfromtxt(file,  dtype='datetime64[s],float,float,float,float,float,float',usecols=(0,2,3,4,5,6,7), delimiter=';',names=True)

fig, ax = plt.subplots()
ax.plot_date(my_data['Zeit'], my_data['Temperatur_C'])

ax.xaxis.set_major_locator(MinuteLocator(byminute=range(0,60,5)))
#ax.xaxis.set_minor_locator(SecondLocator(np.arange(0, 60, 10)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
#fig.autofmt_xdate()

plt.show()