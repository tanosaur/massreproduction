from collections import namedtuple
Isotope = namedtuple('Isotope', 'element number mass abundance')

ISOTOPES = [
    Isotope('Al', 27, 26.98, 100),
    Isotope('Cr', 50, 49.95, 4.3),
    Isotope('Cr', 52, 51.94, 83.8),
    Isotope('Cr', 53, 52.94, 9.5),
    Isotope('Cr', 54, 53.94, 2.4),
    Isotope('H', 1, 1.008, 99.985),
    Isotope('H', 2, 2.014, 0.015),
]

class Ion(namedtuple('Ion', 'isotope charge_state')):
    @property
    def mass_to_charge(self):
        return self.isotope.mass / self.charge_state

    @property
    def name(self):
        return '%s%s+%s' % (self.isotope.number, self.isotope.element, self.charge_state)

Range = namedtuple('Range', 'start end')
Method = namedtuple('Method', 'name function')
Analysis = namedtuple('Analysis', 'method range reason')

import json

analyses = {
Ion(Isotope('H', 2, 2.014, 0.015),1): Analysis(method=Method('FWHM',None), range=Range(1.5,2.5), reason='Just coz'),
Ion(Isotope('Cr', 53, 52.94, 9.5),2): Analysis(method=Method('FWTM',None), range=Range(25.5,26.5), reason='Felt like it')
}

analyses_list = []

for ion, analysis in analyses.items():
    analyses_list.append(ion.name)
    analyses_list.append({
    'Ion': [ion.isotope.element, ion.isotope.number, ion.isotope.mass, ion.isotope.abundance, ion.charge_state],
    'Method': analysis.method.name,
    'Range': [analysis.range.start, analysis.range.end],
    'Reason': analysis.reason})

with open('json.mr', mode='w', encoding='utf-8') as f:
    json.dump(analyses_list, f, indent=2)
