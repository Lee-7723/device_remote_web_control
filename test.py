import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('TCPIP0::K-N6700C-13232.local::inst0::INSTR')
#inst.write('*RST')

    
print ("What is the Voltage you want to output?")
vout = input()

print(vout)
string = ':VOLTage '+str(vout)+',(@1);:CURrent 1.5,(@1)'
print(string)
inst.write(string)

#inst.write (':VOLTage 8,(@1);:CURrent 1.5,(@1)')
