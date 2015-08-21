import unittest
import numpy as np
import aptread.aptload

from PyQt4.QtGui import QUndoCommand, QUndoView

class CommandLoadData(QUndoCommand):

    def __init__(self, posfile, m2c_model):
        super(CommandLoadData, self).__init__('Load (%s)' %posfile)

        self.posfile = posfile
        self.m2c_model = m2c_model

        self._old_m2cs = None

    def redo(self):
        new_m2cs = self._read_posfile(self.posfile)
        self._old_m2cs = self.m2c_model.replace_m2cs(new_m2cs)

    def undo(self):
        self.m2c_model.replace_m2cs(self._old_m2cs)

    def _read_posfile(self, posfile):
        return aptread.aptload.APData(posfile).pos.mc.tolist() # Convert numpy array of mass-to-charges to list

class CommandBinSizeChange(QUndoCommand):

    def __init__(self, bin_size, bin_size_model, m2c_model):
        super(CommandBinSizeChange, self).__init__('Bin size (%s)' %bin_size)

        self.bin_size=bin_size
        self.bin_size_model=bin_size_model

        self._old_bin_size = None

    def redo(self):
        self._old_bin_size = self.bin_size_model.replace_bin_size(self.bin_size)

    def undo(self):
        self.bin_size_model.replace_bin_size(self._old_bin_size)


class CommandSuggest(QUndoCommand):

    def __init__(self, known_elements, max_charge_state, suggest_model):
        super(CommandSuggest, self).__init__('Suggest {0} ({1})'.format(known_elements,max_charge_state))

        self.suggest_model=suggest_model

        self.known_elements=known_elements # String
        self.max_charge_state=max_charge_state # Int

        self._old_known_elements=None
        self._old_max_charge_state=None

    def redo(self):
        self._old_known_elements, self._old_max_charge_state = self.suggest_model.replace(self.known_elements, self.max_charge_state)

    def undo(self):
        self.suggest_model.replace(self._old_known_elements,self._old_max_charge_state)

class CommandAddIonsToTable(QUndoCommand):
    def __init__(self,ion_names,suggest_model):

        super(CommandAddIonsToTable, self).__init__('Add {0}'.format(','.join(ion_names)))

        self.ion_names=ion_names
        self.suggest_model=suggest_model

    def redo(self):
        self._old_ions_in_table=list(self.suggest_model.ionsintable)
        self.suggest_model.set_ionsintable(self.ion_names)
        self.suggest_model.range_table_updated.emit(self.suggest_model.ionsintable)

    def undo(self):
        self.suggest_model.ionsintable=self._old_ions_in_table
        self.suggest_model.range_table_updated.emit(self.suggest_model.ionsintable)


class CommandRemoveIonsFromTree(QUndoCommand):
    pass
