from itertools import cycle

from matplotlib.widgets import SpanSelector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

if __name__=='__main__':
    t=np.arange(180)
    value=(20*np.sin((np.pi/2)*(t/22.0)) + 25 * np.random.random((len(t),))+50)
    fig=Figure()
    canvas=FigureCanvas(fig)
    ax=fig.add_subplot(111)
    ax.step(t,value)

    colors=cycle(list('rybmc'))

    def onselect(x0,x1):
        ax.axvspan(x0,x1, facecolor=next(colors), alpha=0.5)
        fig.canvas.draw_idle()

    ss=SpanSelector(ax,onselect,'horizontal')
    fig.canvas.draw()
    plt.show()
