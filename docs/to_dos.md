# Suggested implementation

_Completed_

- Manual range selection
- Auto range selection
- Add ions from a suggest function
- A suggest function
- Load/export analysis from/to a workflow file
- Load spectrum from .pos file
- Bin size adjustment (laggy but OK for 1.0 release)
- A range of plot controls via matplotlib http://matplotlib.org/users/navigation_toolbar.html

_In progress_
- Export to .rng file - fix or redo
- Plot bug - must fix issue where plot is resizing to default frame at every update

_Not started_
- Load from .rng file
- Load from .epos file
- Showing multiple hits on plot from .epos file
- Add plot control of double click to zoom out as in IVAS (popular request from users)
- ‘Clear all’ button (at the moment users must restart program to easily clear program state)
- Allow fix of ‘Tools’ dialog box on to the main window (includes suggest and action history tabs) (good request from a user)
- Packaging - https://wiki.python.org/moin/PyQt/Deploying_PyQt_Applications https://www.smallsurething.com/a-really-simple-guide-to-packaging-your-pyqt-application-with-cx_freeze/