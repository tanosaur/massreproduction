# MassRep
## A reproducible workflow mass spectrum analysis GUI for atom probe tomography

- Requires PyQt4, matplotlib and Python 3.
- Run mainwindow.py to load GUI.
- See 'manual.pdf’ in ‘docs’ folder for GUI shortcuts.

## Features

- single-ion 'suggest' function
- manual range application
- export to .rng file
- export to .json file
- loads data from .pos
- loads saved analyses from .json
- .json files can be applied to new datasets
- 'history' view to toggle between previous steps
- bin size control
- interactive plot controls via matplotlib (http://matplotlib.org/users/navigation_toolbar.html)

![alt tag](https://github.com/sojung21/massreproduction/blob/master/docs/wiki%20images/GUI_suggest.png)
![alt tag](https://github.com/sojung21/massreproduction/blob/master/docs/wiki%20images/GUI_auto.png)

## Build
- 'lookups.py' - RGB colors and isotope data
- 'models.py' -> 'viewmodels.py' -> 'mainwindow.py', 'plots.py' -> 'commands.py' ( -> 'models.py')
- 'ui_ ... .py' - UI setup files
- See ‘docs’ folder for further info.

## Licensing

GNU GPL v3.