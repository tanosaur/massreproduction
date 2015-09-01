import unittest
import numpy as np
import json
import aptread.aptload

from PyQt4.QtGui import QUndoCommand, QUndoView

class LoadM2C(QUndoCommand):
    def __init__(self, posfile, model):
        super(LoadM2C, self).__init__('Load (%s)' %posfile)

        self._posfile =  posfile
        self._model = model

        self._old_m2cs = None

    def redo(self):
        new_m2cs = self._read_posfile(self._posfile)
        self._old_m2cs = self._model.replace(new_m2cs)

    def undo(self):
        self._model.replace(self._old_m2cs)

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


class SuggestIons(QUndoCommand):

    def __init__(self, known_elements, max_charge_state, model):
        super(SuggestIons, self).__init__('Suggest {0} ({1})'.format(known_elements,max_charge_state))

        self._model=model

        self._known_elements=known_elements
        self._max_charge_state=max_charge_state

        self._old_suggested_ions=None

    def redo(self):
        new_suggested_ions = self._model.suggest(self._known_elements, self._max_charge_state)
        self._old_suggested_ions = self._model.replace(new_suggested_ions)

    def undo(self):
        self._model.replace(self._old_suggested_ions)

class AddIonsToTable(QUndoCommand):
    def __init__(self, ions, model):
        super(AddIonsToTable, self).__init__('Add {0}'.format(', '.join(ion.name for ion in ions)))

        self._model=model
        self._ions=ions
        self._old_analyses=None

    def redo(self):
        self._old_analyses = self._model.add_analyses(self._ions)

    def undo(self):
        self._model.replace(self._old_analyses)

class AddMethods(QUndoCommand):
    def __init__(self, methods, model):
        super(AddMethods, self).__init__('Add {0}'.format(', '.join(method.name for method in methods)))

        self._model=model
        self._methods=methods

        self._old_methods=None

    def redo(self):
        self._old_methods = self._model.replace(self._methods)

    def undo(self):
        self._model.replace(self._old_methods)

class ExportAnalyses(QUndoCommand):
    def __init__(self, model):
        super(ExportAnalyses, self).__init__('Export analyses')

        self._model=model

    def redo(self):
        self._model.export_analyses()

class LoadAnalyses(QUndoCommand):
    def __init__(self, filename, model):
        super(LoadAnalyses, self).__init__('Load (%s)' %filename)

        self._filename=filename
        self._model=model

        self._old_analyses=None

    def redo(self):
        new_analyses = self._read_mrfile(self._filename)
        self._old_analyses = self._model.replace(new_analyses)

    def undo(self):
        self._model.replace(self._old_analyses)

    def _read_mrfile(self, mrfile):
        with open(mrfile, 'r', encoding='utf-8') as f:
            saved_analyses = json.loads(f)

        return saved_analyses
