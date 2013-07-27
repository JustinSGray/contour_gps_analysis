import bisect as b

class datavector(object): 
  """ This object is responsible for storing the tabular data."""
  def __init__(self,indeps,deps):
    """assumes that indeps is a monotonicly increasing list of reals"""
    self.data = [[y,x] for y,x in zip(indeps,deps)]
  def __getitem__(self, index):
    """ returns the independent variable """ 
    return self.data[index][0]
  def __len__(self):
    return len(self.data)    
    
  def getdep(self,index):
    """ returns the dependent variable """
    return self.data[index][1]        
      
class linterp(object):
  """Traverses a datavector tree and linearliy interpolates, returns the interpolated value.""" 

  def __call__(self,table,data,index,x,indeps):
    x1 = data[index-1] 
    x2 = data[index]
    if(len(indeps) == 0): 
      f_R1 = data.getdep(index-1)
      f_R2 = data.getdep(index)
    else:
      y = indeps #the x value was already popped off
      j = b.bisect(data.getdep(index-1),y)
      f_R1 = (x2-x)/(x2-x1)*table.getval(data.getdep(index-1),y) + (x-x1)/(x2-x1)*table.getval(data.getdep(index-1),y)
      f_R2 = (x2-x)/(x2-x1)*table.getval(data.getdep(index),y) + (x-x1)/(x2-x1)*table.getval(data.getdep(index),y)
    P = (x2-x)/(x2-x1)*f_R1 + (x-x1)/(x2-x1)*f_R2
    return P
    
linearinterp = linterp(); # instance to be used for linear interpolation

class linextrap(object):
  def __call__(self,table,data,index,x,indeps):
    if(index == 0):
      i_R1 = index
      i_R2 = index + 1
    else:
      i_R1 = index - 2
      i_R2 = index - 1
      index -= 2
    x1 = data[i_R1]
    x2 = data[i_R2]
    if(len(indeps) == 0):
      f_R1 = data.getdep(i_R1)
      f_R2 = data.getdep(i_R2)
    else:
      y = indeps #the x value was already popped off
      j = b.bisect(data.getdep(index),y)
      f_R1 = (x2-x)/(x2-x1)*table.getval(data.getdep(index),y) + (x-x1)/(x2-x1)*table.getval(data.getdep(index),y)
      f_R2 = (x2-x)/(x2-x1)*table.getval(data.getdep(index+1),y) + (x-x1)/(x2-x1)*table.getval(data.getdep(index+1),y)
    if f_R1 == f_R2: 
      return f_R1
    P = (x2-x)/(x2-x1)*f_R1 + (x-x1)/(x2-x1)*f_R2
    return P
linearextrap = linextrap()
    
class table(object):
  """An N dimensional Table implementation with a number of interpolation routines available."""   
 
  def __init__(self,rawdata,interpolator=linearinterp,extrapolator=linearextrap):
     self.data = self.processdata(rawdata)
     self.interpolator = interpolator
     self.extrapolator = extrapolator
    
  def __call__(self,indeps):
    return self.getval(self.data,indeps)
  def getval(self,data,indeps):
    x = indeps[0]
    indeps = indeps[1:]
    i = b.bisect(data,x)
    if(i == 0 or i == len(data)): #extrapolate below table data
      return self.extrapolator(self,data,i,x,indeps)
    else:
      return self.interpolator(self,data,i,x,indeps)    
 
  def processdata(self,data): 
    indeps = data.keys()
    indeps.sort()
    if(type(data[indeps[0]]) == dict):
      deps = []
      for x in indeps: 
        deps.append(self.processdata(data[x]))
    else:
      deps = [data[x] for x in indeps]
    return datavector(indeps,deps)  
 




      

    

    