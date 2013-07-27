import csv
import datetime
import numpy as np

from matplotlib import pylab as p, cm, colors

#from openmdao.lib.surrogatemodels.api import FloatKrigingSurrogate

class NoWhiteSpace(csv.excel): 
    skipinitialspace = True



runs = ["tim-3", "mike-2", "justin-3", "jeff-3",]
#runs = ["justin-3", "jeff-3",]
runs = ["tim-3", "mike-2",]
#runs = ['tim-3','jeff-3']

readers = []

for r in runs: 
    reader = csv.DictReader(open('%s-GPS-Data.csv'%r,'rb'),dialect=NoWhiteSpace)
    readers.append(reader)
 

DATA_MAP = {
    "media time": lambda t: datetime.datetime.strptime(t,"%H:%M:%S.%f"),
    "time": None,
    "latitude": float,
    "longitude": float,
    "elevation [m]": float,
    "speed [m/s]": lambda s:float(s)*2.23694,
    "heading": None,
    "variation": None,
    "position dilution": None, 
    "horizontal dilution": None,
    "vertical dilution": None,
    "fix type": None,
    "satellite count": int,
    "valid": bool,
}

def transform(data):
    """maps the transformation functions from DATA_MAP to the given list of dictionaries. 
    Returns dictionary with same keys, but with ordered lists of transformed data""" 

    t_data = {}
    for k in DATA_MAP: 
        t_data[k] = []

    for row in data: 
        for k,t_func in DATA_MAP.iteritems(): 
            if t_func is not None: 
                t_val = t_func(row[k])
                t_data[k].append(t_val)
            else: 
                t_data[k].append(t_val)   

    return t_data             


data = []
for r in readers: 
    data.append(transform(r))

#################################################
fig = p.figure()
#ax = fig.add_subplot(1,2,1)
ax = p.gca()


speeds = []
for d in data:
    speeds.extend(d['speed [m/s]']) 

s_min= min(speeds)
s_max=max(speeds)
c_Norm  = colors.Normalize(vmin=s_min, vmax=s_max)

#ax = fig.add_subplot(1,2,1)
ax.set_aspect('equal')

markers = ['s','o','^','>']
for d,run,m in zip(data,runs,markers): 

    #points = ax.scatter(d['longitude'],d['latitude'],c=d['speed [m/s]'],cmap=cm.jet, 
    #    norm=c_Norm,label=run,marker=m,s=30)


    ax.plot(d['longitude'],d['latitude'],label=run)

p.legend(loc=0)
#p.colorbar(points)

fig = p.figure()
ax = p.gca()
#ax = fig.add_subplot(1,2,2)
for d,run,m in zip(data,runs,markers): 
    ax.plot(d['media time'],d['speed [m/s]'],label=run)
    #pass
p.legend()
p.title('Velocity vs time')

p.show()



