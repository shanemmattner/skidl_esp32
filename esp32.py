from skidl import *

# Interface_USB.kicad_sym: CP2102N-Axx-xQFN24
cp2102 = Part('Interface_USB','CP2102N-Axx-xQFN24', footprint='Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm')
esp32 = Part('RF_Module','ESP32-WROOM-32', footprint='RF_Module:ESP32-WROOM-32')

generate_netlist()
