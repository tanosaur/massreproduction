def required_inputs():
    return ['bin_size', 'abundance', 'suggested_m2c']

def voodoo(bin_size, abundance, suggested_m2c):
    convolution = suggested_m2c/(bin_size*abundance)
    start = suggested_m2c - convolution
    end = suggested_m2c + convolution
    return (start, end)
