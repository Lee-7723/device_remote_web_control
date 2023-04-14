import pyvisa

def poweron():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x2A8D::0x0002::MY56013232::0::INSTR')
    inst.write('output:state on,(@1)') 

def poweroff():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x2A8D::0x0002::MY56013232::0::INSTR')
    inst.write('output:state off,(@1)') 
