import unittest
import numpy as np
import aptread.aptload

from PyQt4.QtGui import QUndoCommand, QUndoView

class LoadM2C(QUndoCommand):
    def __init__(self, posfile, loaded_m2c_model):
        super(LoadM2C, self).__init__('Load (%s)' %posfile)

        self._posfile =  posfile
        self._loaded_m2c_model = loaded_m2c_model

        self._old_m2cs = None

    def redo(self):
        new_m2cs = self._read_posfile(self._posfile)
        self._old_m2cs = self._loaded_m2c_model.replace(new_m2cs)

    def undo(self):
        self._loaded_m2c_model.replace(self._old_m2cs)

    def _read_posfile(self, posfile):
        return tuple(aptread.aptload.APData(posfile).pos.mc.tolist())

class BinSizeValueChange(QUndoCommand):

    def __init__(self, value, model):
        super(BinSizeValueChange, self).__init__('Bin Size (%s)' % value)

        self._new_value=value
        self._model=model

        self._old_value = None

    def redo(self):
        self._old_value = self._model.replace_value(self._new_value)

    def undo(self):
        self._model.replace_value(self._old_value)


class SuggestChange(QUndoCommand):

    def __init__(self, known_elements, max_charge_state, model):
        super(SuggestChange, self).__init__('Suggest {0} ({1})'.format(known_elements,max_charge_state))

        self._model=model

        self._new_known_elements=known_elements
        self._new_max_charge_state=max_charge_state

        self._old_known_elements=None
        self._old_max_charge_state=None

    def redo(self):
        self._old_known_elements, self._old_max_charge_state = self.model.replace(self._new_known_elements, self._new_max_charge_state)

    def undo(self):
        self.model.replace(self._old_known_elements,self._old_max_charge_state)

class CommandAddIonsToTable(QUndoCommand):
    def __init__(self,ion_names, range_table_model):

        super(CommandAddIonsToTable, self).__init__('Add {0}'.format(','.join(ion_names)))

        self.range_table_model=range_table_model

        self.ion_names=ion_names
        self.old_ion_names=None

    def redo(self):
        self._old_ions_names = self.range_table_model.update_ions(self.ion_names)

    def undo(self):
        self.range_table_model.update_ions(self.old_ion_names)

class CommandRemoveIonsFromTree(QUndoCommand):
    pass
