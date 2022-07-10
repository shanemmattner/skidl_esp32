from skidl import *


# standard logic level FET
def npn_LL(gate, drain, source, sch_lib='Transistor_FET', sch_name='DMN2041L', footprint='Package_TO_SOT_SMD:SOT-23'):
    npn = Part(sch_lib, sch_name, footprint=footprint)
    npn[1] += gate
    npn[2] += source
    npn[3] += drain
    
def r(value, p1, p2, footprint='digikey-footprints:0603'):
    r = Part('Device', 'R', value=value, footprint=footprint)
    r[1] += p1
    r[2] += p2
    
def c(value, p1, p2, footprint='digikey-footprints:0603'):
    c = Part('Device', 'C', value=value, footprint=footprint)
    c[1] += p1
    c[2] += p2
    
def serial_to_usb(MCU_EN, GPIO0, MCU_TX, MCU_RX, V3_3=Net('V3_3'), GND=Net('GND')):

    # Make parts
    cp2104 = Part('Interface_USB','CP2104', footprint='Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm')
    # Connect power pins
    cp2104[5,6,7] += V3_3
    cp2104[2,25] += GND
    
    usb_conn = Part('Connector', 'USB_B_Mini', footprint='USB_Mini-B_Lumberg_2486_01_Horizontal')
    usb_conn['VBUS'] += cp2104[8]
    usb_conn['D-'] += cp2104[4]
    usb_conn['D+'] += cp2104[3]
    # usb_conn['ID'] # not connected
    usb_conn['GND','Shield'] += GND
    
    
    # Decoupling/bulking capacitors
    c('100nF', V3_3, GND)
    c('10uF', V3_3, GND)
    
    # ROM programming cap
    c('4.7uF', cp2104['VPP'], GND)
    
    # Nets for programming 
    RTS = Net('RTS')
    DTR = Net('DTR')
    #programming transistors
    npn_LL(RTS, DTR, GPIO0)
    npn_LL(DTR, RTS, MCU_EN)
    
    # uart resistors
    r('470R', MCU_TX, cp2104[20])
    r('470R', MCU_RX, cp2104[21])

def esp32_circuit(V3_3=Net('V3_3'), GND=Net('GND')):
    # MCU
    esp32 = Part('RF_Module','ESP32-WROOM-32', footprint='RF_Module:ESP32-WROOM-32')

    esp32[1] += GND
    esp32[2] += V3_3
    
    # Decoupling/bulking capacitors
    c('100nF', V3_3, GND)
    c('10uF', V3_3, GND)
    
    # Enable Circuit
    r('10k', V3_3, esp32[3])
    c('10uF', esp32[3], GND)
    switch = Part('Switch','SW_DPST', footprint='digikey-footprints:Switch_Tactile_SMD_6x6mm_PTS645')
    switch[1,2] += esp32['EN']
    switch[3,4] += GND

    # serial/programming
    serial_to_usb(esp32['EN'], esp32['IO0'], esp32['TXD0/IO1'], esp32['RXD0/IO3'])


esp32_circuit()



generate_netlist(file_="/home/shanemattner/Desktop/esp32/skidl_esp32/esp32_kicad/esp32.net")
