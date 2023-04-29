import pyvisa
import time


address = 'TCPIP0::K-N6700C-13232.local::inst0::INSTR'#'USB0::0x2A8D::0x0002::MY56013232::0::INSTR'

def check_and_plugin():
    rm = pyvisa.ResourceManager()
    if not rm.list_resources().__contains__(address):
        raise Exception('未连接此设备(device not connected): N6700C')
    else:
        return rm.open_resource(address)

def poweron():
    inst = check_and_plugin()
    inst.write('output:state on,(@1)') 

def poweroff():
    inst = check_and_plugin()
    inst.write('output:state off,(@1)') 

def querystates():
    inst = check_and_plugin()
    state = inst.query('output:state? (@1)')
    if state == '1\n':
        return True
    else:
        return False
    
def queryerrors():
    inst = check_and_plugin()
    errors = inst.query('*ESR?')
    if errors == '+0\n':
        return False
    else:
        return True
    
def setPowercycle(cycle, voltage, uptime, downtime):
    inst = check_and_plugin()
    inst.write(':voltage '+str(voltage)+',(@1)' ) 
    for i in range(cycle):
        inst.write('output:state on,(@1);') 
        time.sleep(uptime)
        inst.write('output:state off,(@1)') 
        time.sleep(downtime)