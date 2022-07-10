from skidl import *

# standard logic level FET
def npn_LL(gate, drain, source):
    npn = Part('Transistor_FET', 'DMN2041L', footprint='Package_TO_SOT_SMD:SOT-23')
    npn[1] += gate
    npn[2] += source
    npn[3] += drain
    
def serial_to_usb():
    cp2102 = Part('Interface_USB','CP2102N-Axx-xQFN24', footprint='Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm')

def esp32_circuit(v3_3, gnd):
    
    # Nets
    mcu_en = Net('mcu_en')
    usb_rts = Net('usb_rts')
    mac_tx_ck = Net('mac_tx_ck')
    usb_dtr = Net('usb_dtr')
    
    # MCU
    esp32 = Part('RF_Module','ESP32-WROOM-32', footprint='RF_Module:ESP32-WROOM-32')
    
    #programming transistors
    npn_LL(usb_dtr, usb_rts, mcu_en)
    npn_LL(usb_rts, usb_dtr, mac_tx_ck)


v3_3 = Net('v3_3')
gnd = Net('gnd')

esp32_circuit(v3_3,gnd)
serial_to_usb()


generate_netlist(file_="/home/shanemattner/Desktop/esp32/skidl_esp32/esp32_kicad/esp32.net")
