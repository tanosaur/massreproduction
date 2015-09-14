def required_inputs():
    return ['suggested_m2c']

def manual(suggested_m2c):
    start = suggested_m2c - 0.25
    end = suggested_m2c + 0.25
    return (start, end)
