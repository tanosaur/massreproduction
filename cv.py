import fileinput
import re

ISOTOPE_REGEXP = re.compile("[0-9]+ [0-9.]+ [0-9.]")

for l in fileinput.input():
  l = l.strip()
  if ISOTOPE_REGEXP.match(l):
    params = ', '.join(l.split(' '))
    print("Isotope('%s', %s)" % (last_isotope_name, params))
  elif len(l) > 0:
    last_isotope_name = l
