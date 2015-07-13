from itertools import cycle
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np

if __name__=='__main__':
    t=np.arange(180)
    value=(20*np.sin((np.pi/2)*(t/22.0)) + 25 * np.random.random((len(t),))+50)
    fig,ax=plt.subplots(1,1,figsize=(10,5))
    ax.step(t,value)
    ax.set_ylabel('Stock Price (USD)')
    ax.set_xlabel('Time (days)')
    colors=cycle(list('rybmc'))

    def onselect(x0,x1):
        ax.axvspan(x0,x1, facecolor=next(colors), alpha=0.5)
        fig.canvas.draw_idle()

    ss=SpanSelector(ax,onselect,'horizontal')
    plt.show()
