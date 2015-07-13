from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.path import Path

class DataContainer(object):
  def __init__(self,xs,ys):
    self.xs=xs
    self.ys=ys
  def select_from_bbox(self,x1,y1,x2,y2):
    bbox=Path([(x1,y1), (x1,y2), (x2,y2), (x2,y1)], closed=True)
    return bbox.contains_points(zip(self.xs, self.ys))

if __name__=='__main__':
    xs,ys=np.random.random((2,25))
    fig,ax=plt.subplots(1,1)
    ax.scatter(xs, ys)

    def howmanyselected(evnt_clik, evnt_release):
        print(evnt_clik.xdata, evnt_clik.ydata)
        print(evnt_release.xdata, evnt_release.ydata)
        where=howmanyselected.dc.select_from_bbox(evnt_clik.xdata, evnt_clik.ydata,evnt_release.xdata, evnt_release.ydata)
        # print('%d out of %d' % (np.sum(where), len(where)))

    howmanyselected.dc=DataContainer(xs,ys)

    rs=RectangleSelector(ax, howmanyselected)
    plt.show()
