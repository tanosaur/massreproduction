
def eposreaderMKII(file_name):
# Outputs: detectX, detectY, x, y, z, m, tof, voltageDC, voltage_pulse, nulls, nat_pulse
# - detectX and detectY are the detector coordinates
# - x, y, z and m are the coordinates /w mass/charge ratio
# - tof is the time of flight
# - voltageDC and voltage_pulse, DC and pulse voltage, respectively
# - nulls -  is the time between each pulse
# - nat_pulse is the number of atoms detected in an event
# - file_name is the name of the file, must be in same directory
#2015
# Author: Tong GAO

## Open the file
    fileID = open(file_name,"rb")
    print(fileID)
    import os
    size=os.path.getsize(file_name)
    print ('Opened file...')

    m=[]
    import struct
    fileID.seek(12)
    i=0
    while i <(size/44):
        a=fileID.read(4)
        d,=struct.unpack('>f',a)
        m.append(d)

        fileID.read(40)
        i+=1
## Close file
    fileID.close()
    return m

m=eposreaderMKII('R14_14153-v01.epos')
print(m)
