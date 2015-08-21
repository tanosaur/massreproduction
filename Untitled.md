1.295 make plot
2.283 load
0.375    0.002 axis.py:1959(_get_tick)
 0.709    0.236 artist.py:57(draw_wrapper)
0.256    0.032 _base.py:817(cla)
0.707    0.236 _base.py:1989(draw)
0.416    0.208 _axes.py:5376(hist)
0.000    0.041    0.007 axis.py:1294(get_major_ticks)
0.710    0.237 backend_qt5agg.py:140(draw)
        8    0.001    0.000    0.063    0.008 backend_qt5agg.py:73(paintEvent)
        6    0.000    0.000    0.289    0.048 axis.py:1317(get_minor_ticks)
Statistical analysis
Click trails is what we are doing (this is the first analysis resource, user tracing)
Get someone in analytics
Analytics is more interesting

ipython notebook


- create a function for controller to instantiate models

# Code improvement

MVC
Undo/redos
Each data in own model class
Factored code, explicit data flow (easier to understand, less buggy, easier to change)
- passing variables instead of accessing directly
- instantiating where needed only
- easier for one signal to action many view changes and see how it works
- general functions do many things (work well for many cases)


# Build/testing

1. Scientific - scientific testing
2. User - usability testing 
