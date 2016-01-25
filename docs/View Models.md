# View Models

## Reference Data (Static)

Element = string (ex: ‘Al, ‘H’)

Isotope = {
  element: Element
  name: int (ex: 26, 1)
  mass: float (ex: 25.9, 1.1)
  abundance: float (ex: 100.0, 12.4)
}

Ion = {
  isotope: Isotope
  charge_state: int (ex: 1, 2, 3)
}

## Reified types

Range = {
	start: float (ex: 25.5)
	end: float (ex: 26.5)
}

## Notation

CamelCase words are reified types; abstract concepts to which we have given definite names.

<some name> is a value that another part of the system is responsible for

_<some name> is a value that this part of the system is responsible for

## Working Plot
### To display the mass to charge information
m2c = [float, …]
binsize = int

### To display suggestions
suggestions = [Ion, …]

### To display ranges
ranges = {
	Ion: Range
}

## Suggested Ion List
ions = [Ion, …]

## Analyses Table
analyses = [
	Ion: {
		method: string (ex: ‘FWHM’, ‘Manual’)
		range: Range
		reason: string
	}
]

## Final Plot
### To display mass to charge information
m2c = [float, …]
binsize = int

### To display ranges
ranges = {
	Ion: Range
}

## Undo Stack
commands = [Command, …]