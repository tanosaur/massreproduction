import json
import os
import aptread.aptload

from PyQt4.QtGui import QUndoCommand, QUndoView
from models import Ion, Range, Analysis
from lookups import ISOTOPES

class LoadPOS(QUndoCommand):
    def __init__(self, posfile, m2c_model, metadata_model):
        super(LoadPOS, self).__init__('Load (%s)' %posfile)

        self._posfile =  posfile
        self._m2c_model = m2c_model
        self._metadata_model = metadata_model

        self._old_m2cs = None
        self._old_experiment_ID = None

    def redo(self):
        new_m2cs = self._read_posfile(self._posfile)
        self._old_m2cs = self._m2c_model.replace(new_m2cs)

        new_experiment_ID = self._create_experiment_ID(self._posfile)
        self._old_experiment_ID = self._metadata_model.replace_experiment_ID(new_experiment_ID)

    def undo(self):
        self._m2c_model.replace(self._old_m2cs)

    def _read_posfile(self, posfile):
        return tuple(aptread.aptload.POSData(posfile).pos.mc.tolist())

    def _create_experiment_ID(self, posfile):
        _ , tail = os.path.split(posfile)
        experiment_ID = os.path.splitext(tail)[0]
        return experiment_ID

class LoadEPOS(QUndoCommand):
    def __init__(self, posfile, model):
        super(LoadPOS, self).__init__('Load (%s)' %posfile)

        self._posfile =  posfile
        self._model = model

        self._old_m2cs = None

    def redo(self):
        new_m2cs = self._read_posfile(self._posfile)
        self._old_m2cs = self._model.replace(new_m2cs)

    def undo(self):
        self._model.replace(self._old_m2cs)

    def _read_posfile(self, posfile):
        return tuple(aptread.aptload.POSData(posfile).pos.mc.tolist())

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
        new_suggested_ions = self._suggest(self._known_elements, self._max_charge_state)
        self._old_suggested_ions = self._model.replace(new_suggested_ions)

    def undo(self):
        self._model.replace(self._old_suggested_ions)

    def _suggest(self, known_elements, max_charge_state):
        known_elements=known_elements.split(',')
        working_suggested_ions=[]

        for element in known_elements:
            for isotope in ISOTOPES:
                if element == isotope.element:
                    for charge_state in range(1,max_charge_state+1):
                        working_suggested_ions.append(Ion(isotope, charge_state))

        suggested_ions=tuple(working_suggested_ions)

        return suggested_ions

class AddIonsToTable(QUndoCommand):
    def __init__(self, ions, model):
        super(AddIonsToTable, self).__init__('Add {0}'.format(', '.join(ion.name for ion in ions)))

        self._model=model
        self._ions=ions
        self._old_analyses=None

    def redo(self):
        new_analyses = self._model.analyses_from_suggest(self._ions)
        self._old_analyses = self._model.append(new_analyses)

    def undo(self):
        self._model.replace(self._old_analyses)

class SelectMethod(QUndoCommand):
    def __init__(self, ion, method, analyses_model, methods_view_model):
        super(SelectMethod, self).__init__('{0} Method: {1}'.format(ion.name, method))

        self._analyses_model = analyses_model
        self._methods_view_model = methods_view_model

        self._ion = ion
        self._method = method
        self._new_range = None

        self._old_ion = None
        self._old_method = None
        self._old_range = None

    def redo(self):
        self._new_range = self._methods_view_model.run_method_for_ion(self._ion, self._method)
        self._old_ion, self._old_method, self._old_range = self._analyses_model.update_method_for_ion(self._ion, self._method, self._new_range)

    def undo(self):
        self._analyses_model.update_method_for_ion(self._old_ion, self._old_method, self._old_range)

class ExportAsJSON(QUndoCommand):
    def __init__(self, filename, model):
        super(ExportAsJSON, self).__init__('Export as {0}'.format(filename))

        self._model = model
        self._filename = filename

    def redo(self):
        self._model.export_analyses_to_mrfile(self._filename)

    def undo(self):
        pass

class ImportJSON(QUndoCommand):
    def __init__(self, filename, mr_view_model, analyses_model, metadata_model):
        _ , tail = os.path.split(filename)
        super(ImportJSON, self).__init__('Load %s' %tail)

        self._mr_view_model= mr_view_model
        self._analyses_model = analyses_model
        self._metadata_model = metadata_model

        self._filename=filename

        self._old_analyses=None
        self._old_metadata=None

    def redo(self):
        imported_analyses, imported_metadata = self._mr_view_model.import_analyses_from_mrfile(self._filename)
        self._old_analyses = self._analyses_model.append(imported_analyses)
        self._old_metadata = self._metadata_model.replace(imported_metadata)

    def undo(self):
        self._analyses_model.replace(self._old_analyses)
        self._metadata_model.replace(self._old_metadata)

class ExportAsRNG(QUndoCommand):
    def __init__(self, filename, model):
        super(ExportAsRNG, self).__init__('Export as {0}'.format(filename))

        self._model = model
        self._filename = filename

    def redo(self):
        self._model.export_analyses_to_rngfile(self._filename)

    def undo(self):
        pass

class UpdateExperimentID(QUndoCommand):
    def __init__(self, experiment_ID, model):
        super(UpdateExperimentID, self).__init__('Experiment ID: (%s)' %experiment_ID)

        self._model = model
        self._experiment_ID = experiment_ID

        self._old_experiment_ID = None

    def redo(self):
        print(self._experiment_ID)
        self._old_experiment_ID = self._model.replace_experiment_ID(self._experiment_ID)

    def undo(self):
        self._model.replace_experiment_ID(self._old_experiment_ID)

class UpdateExperimentDescription(QUndoCommand):
    def __init__(self, experiment_description, model):
        super(UpdateExperimentDescription, self).__init__('Description: (%s)' %experiment_description)

        self._model = model
        self._experiment_description = experiment_description

        self._old_experiment_description = None

    def redo(self):
        self._old_experiment_description = self._model.replace_experiment_description(self._experiment_description)

    def undo(self):
        self._model.replace_experiment_description(self._old_experiment_description)

class UpdateManualRange(QUndoCommand):
    def __init__(self, ion, start, end, model):

        if str(start):
            start = float(start)
        if str(end):
            end = float(end)

        super(UpdateManualRange, self).__init__('{0} Range: {1} - {2}'.format(ion.name, round(start,2), round(end,2)))

        self._model = model
        self._new_ion = ion
        self._new_range = Range(start, end)

        self._old_ion = None
        self._old_range = None

    def redo(self):
        self._old_ion, self._old_range = self._model.update_manual_range_for_ion(self._new_ion, self._new_range)

    def undo(self):
        self._model.update_manual_range_for_ion(self._old_ion, self._old_range)

class UpdateReason(QUndoCommand):
    def __init__(self, ion, reason, model):
        super(UpdateReason, self).__init__('{0} Reason: {1}'.format(ion.name, reason))

        self._model = model
        self._new_ion = ion
        self._new_reason = reason

        self._old_ion = None
        self._old_reason = None

    def redo(self):
        self._old_ion, self._old_reason = self._model.update_reason_for_ion(self._new_ion, self._new_reason)

    def undo(self):
        self._model.update_reason_for_ion(self._old_ion, self._old_reason)

class DeleteIon(QUndoCommand):
    def __init__(self, selected_ions, model):
        super(DeleteIon, self).__init__('Delete {0}'.format(', '.join(ion.name for ion in selected_ions)))

        self._model = model
        self._ions_to_delete = selected_ions

        self._old_analyses = None

    def redo(self):
        self._old_analyses = self._model.delete_analyses(self._ions_to_delete)

    def undo(self):
        self._model.replace(self._old_analyses)
