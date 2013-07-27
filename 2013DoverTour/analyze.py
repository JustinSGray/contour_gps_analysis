import csv
import datetime
import numpy as np


from matplotlib import pylab as p

#from openmdao.lib.surrogatemodels.api import FloatKrigingSurrogate

class NoWhiteSpace(csv.excel): 
    skipinitialspace = True

tim_reader = csv.DictReader(open('tim_run3-GPS-Data.csv','rb'),dialect=NoWhiteSpace)

justin_reader = csv.DictReader(open('justin_run1-GPS-Data.csv','rb'),dialect=NoWhiteSpace)

#header row
data = tim_reader.next()

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


tim_data = transform(tim_reader)
justin_data = transform(justin_reader)

#################################################
fig = p.figure()
#ax = fig.add_subplot(1,2,1)
ax = p.gca()
ax.plot(tim_data['longitude'],tim_data['latitude'],label="Tim")
ax.plot(justin_data['longitude'],justin_data['latitude'],label="Justin")
ax.set_aspect('equal')
p.legend(loc=0)


fig = p.figure()
ax = fig.add_subplot(1,2,2)
ax.plot(tim_data['media time'],tim_data['speed [m/s]'],label="Tim")
ax.plot(justin_data['media time'],justin_data['speed [m/s]'],label="Justin")
p.legend(loc=0)
p.title('Velocity vs time')

p.show()



