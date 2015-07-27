from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import OrderedDict

class KeymapControl:
    def __init__(self, fig):
        self.fig=fig
        keypressid=self.fig.canvas.manager.key_press_handler_id
        self.fig.canvas.mpl_disconnect(keypressid)
        self._keymap=OrderedDict()
        self.connect_keymap()
        self._lastkey=None

    def connect_keymap(self):
        self._keycid=self.fig.canvas.mpl_connect('key_press_event', self.keypress)

    def disconnect_keymap(self):
        if self._keycid is not None:
            self.fig.canvas.mpl_disconnect(self._keycid)
            self._keycid=None

    def add_key_action(self, key, description, action_func):
        if not callable(action_func):
            raise ValueError('Invalid action. Key %s Description %s - action function is not a callable' % (key, description))

        if key in self._keymap:
            raise ValueError('%s is already in the keymap' % key)

        self._keymap[key]=(description, action_func)

    def keypress(self,event):
        action_tuple=self._keymap.get(event.key, None)
        if action_tuple:
            self._lastkey=event.key
            action_tuple[1]()

    def displayhelpmenu(self):
        print('Help Menu')
        print('Key      Action')
        print('================')
        for key, (description, _) in self._keymap.items():
            print('%11s %s' %(key,description))


class ControlSys(KeymapControl):
    def __init__(self, fig):
        # self.i=0
        self._hidekey=None
        self._hidecid=None
        KeymapControl.__init__(self, fig)

        self.add_key_action('left', 'Back a frame', lambda:self.change_frame(-1))
        self.add_key_action('right', 'Forward a frame', lambda:self.change_frame(1))
        self.add_key_action('h', 'Display help menu', lambda:self.displayhelpmenu)

    def change_frame(self,frame_delta):
        print ('HEYYYYYYYYY')
        # newi=self.i+frame_delta
        # if newi>=self.data.shape[0]:
        #     newi=self.data.shape[0]-1
        # if newi<0:
        #     newi=0
        # if newi!=self.i:
        #     self.polygons[self.i].set_visible(False)
        #     self.

data = [random.random() for i in range(10)]
t=np.arange(180)
value=(20*np.sin((np.pi/2)*(t/22.0)) + 25 * np.random.random((len(t),))+50)
fig,ax=plt.subplots(1,1)
ax.step(t,value)
cntrlsys=ControlSys(fig)
plt.show()
