EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Pycom Tank Sensor - Submersible"
Date "2020-02-21"
Rev "2"
Comp ""
Comment1 "Ashley Woods"
Comment2 ""
Comment3 "LoRaWAN water tank level sensor for submersible pressure sensor"
Comment4 "PyCom LoPy4 LoRaWAN module"
$EndDescr
Text GLabel 1250 1500 0    50   Input ~ 0
CONSOLE_TX
Wire Wire Line
	1250 1500 1500 1500
Text GLabel 1250 1650 0    50   Input ~ 0
CONSOLE_RX
Wire Wire Line
	1250 1650 1500 1650
$Comp
L power:GND #PWR0102
U 1 1 5BD542BF
P 3750 1050
F 0 "#PWR0102" H 3750 800 50  0001 C CNN
F 1 "GND" H 3755 877 50  0000 C CNN
F 2 "" H 3750 1050 50  0001 C CNN
F 3 "" H 3750 1050 50  0001 C CNN
	1    3750 1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 1050 3750 1050
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5BD54359
P 2350 3800
F 0 "J2" H 2430 3842 50  0000 L CNN
F 1 "Console" H 2430 3751 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 2350 3800 50  0001 C CNN
F 3 "~" H 2350 3800 50  0001 C CNN
	1    2350 3800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5BD54436
P 1400 3700
F 0 "#PWR0103" H 1400 3450 50  0001 C CNN
F 1 "GND" H 1405 3527 50  0000 C CNN
F 2 "" H 1400 3700 50  0001 C CNN
F 3 "" H 1400 3700 50  0001 C CNN
	1    1400 3700
	1    0    0    -1  
$EndComp
Text GLabel 2050 3800 0    50   Input ~ 0
CONSOLE_TX
Text GLabel 2050 3900 0    50   Input ~ 0
CONSOLE_RX
Wire Wire Line
	1400 3700 2150 3700
Wire Wire Line
	3150 1650 3450 1650
Wire Wire Line
	3150 900  3450 900 
Text GLabel 1200 2400 0    50   Input ~ 0
SDA
Wire Wire Line
	1200 2400 1500 2400
Text GLabel 1200 2550 0    50   Input ~ 0
SCL
Wire Wire Line
	1200 2550 1500 2550
Wire Wire Line
	3150 1800 3450 1800
Text GLabel 5350 6300 0    50   Input ~ 0
LDR_SENSE
Wire Wire Line
	2050 3800 2150 3800
Wire Wire Line
	2150 3900 2050 3900
NoConn ~ 1500 900 
NoConn ~ 1500 1050
NoConn ~ 1500 1200
NoConn ~ 1500 1350
NoConn ~ 1500 1800
NoConn ~ 1500 1950
NoConn ~ 1500 2100
NoConn ~ 1500 2250
NoConn ~ 1500 2850
NoConn ~ 3150 2850
NoConn ~ 3150 2700
NoConn ~ 3150 2250
NoConn ~ 3150 2100
NoConn ~ 3150 1950
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J1
U 1 1 5E5041DC
P 9950 950
F 0 "J1" H 9900 1100 50  0000 L CNN
F 1 "Solar Panel" H 9850 1050 50  0000 L CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 9950 950 50  0001 C CNN
F 3 "~" H 9950 950 50  0001 C CNN
	1    9950 950 
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J3
U 1 1 5E506B7D
P 9850 2400
F 0 "J3" H 9850 2550 50  0000 L CNN
F 1 "Battery Connector" H 9550 2500 50  0000 L CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 9850 2400 50  0001 C CNN
F 3 "~" H 9850 2400 50  0001 C CNN
	1    9850 2400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5E5084FD
P 10150 3750
F 0 "#PWR04" H 10150 3500 50  0001 C CNN
F 1 "GND" H 10155 3577 50  0000 C CNN
F 2 "" H 10150 3750 50  0001 C CNN
F 3 "" H 10150 3750 50  0001 C CNN
	1    10150 3750
	1    0    0    -1  
$EndComp
Text GLabel 3450 900  2    50   Input ~ 0
VCC
Text GLabel 3450 1200 2    50   Input ~ 0
3v3
Wire Wire Line
	3150 1200 3450 1200
Text Notes 10450 6750 0    50   ~ 0
Notes:\n  VCC is 5 Volts
Wire Wire Line
	9750 950  9550 950 
$Comp
L power:GND #PWR03
U 1 1 5E50CFD0
P 9350 2400
F 0 "#PWR03" H 9350 2150 50  0001 C CNN
F 1 "GND" H 9355 2227 50  0000 C CNN
F 2 "" H 9350 2400 50  0001 C CNN
F 3 "" H 9350 2400 50  0001 C CNN
	1    9350 2400
	1    0    0    -1  
$EndComp
Text GLabel 10450 950  2    50   Input ~ 0
PANEL_POS
Text GLabel 10300 2500 2    50   Input ~ 0
BATTERY+12
Text GLabel 9550 950  0    50   Input ~ 0
PANEL_NEG
Wire Wire Line
	9450 3200 9750 3200
Text GLabel 9450 3200 0    50   Input ~ 0
BATTERY+12
Text GLabel 10850 3200 2    50   Input ~ 0
VCC
Wire Wire Line
	10150 3500 10150 3750
$Comp
L Regulator_Switching:TSR_1-2450 U6
U 1 1 5E5075B9
P 10150 3300
F 0 "U6" H 10150 3600 50  0000 C CNN
F 1 "TSR_1-2450" H 10150 3550 50  0000 C CNN
F 2 "Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT" H 10150 3150 50  0001 L CIN
F 3 "http://www.tracopower.com/products/tsr1.pdf" H 10150 3300 50  0001 C CNN
	1    10150 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3550 4350 3550 4450
Connection ~ 3550 4350
Wire Wire Line
	3250 4350 3550 4350
Text GLabel 3250 4350 0    50   Input ~ 0
LDR_SENSE
Wire Wire Line
	3550 3750 3550 3900
Wire Wire Line
	3300 3750 3550 3750
Text GLabel 3300 3750 0    50   Input ~ 0
3v3
Wire Wire Line
	3550 4750 3550 4900
$Comp
L power:GND #PWR0106
U 1 1 5BD713F3
P 3550 4900
F 0 "#PWR0106" H 3550 4650 50  0001 C CNN
F 1 "GND" H 3555 4727 50  0000 C CNN
F 2 "" H 3550 4900 50  0001 C CNN
F 3 "" H 3550 4900 50  0001 C CNN
	1    3550 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3550 4200 3550 4350
$Comp
L Device:R R3
U 1 1 5BD70B05
P 3550 4600
F 0 "R3" H 3620 4646 50  0000 L CNN
F 1 "1K" H 3620 4555 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 3480 4600 50  0001 C CNN
F 3 "" H 3550 4600 50  0001 C CNN
	1    3550 4600
	1    0    0    -1  
$EndComp
$Comp
L Sensor_Optical:A9060 R2
U 1 1 5BD70A16
P 3550 4050
F 0 "R2" H 3620 4096 50  0000 L CNN
F 1 "LDR" H 3620 4005 50  0000 L CNN
F 2 "OptoDevice:R_LDR_5.0x4.1mm_P3mm_Vertical" V 3725 4050 50  0001 C CNN
F 3 "http://cdn-reichelt.de/documents/datenblatt/A500/A90xxxx%23PE.pdf" H 3550 4000 50  0001 C CNN
	1    3550 4050
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J4
U 1 1 5E55D83E
P 7600 1000
F 0 "J4" H 7600 1150 50  0000 L CNN
F 1 "Pressure Sensor" H 7450 1100 50  0000 L CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 7600 1000 50  0001 C CNN
F 3 "~" H 7600 1000 50  0001 C CNN
	1    7600 1000
	1    0    0    -1  
$EndComp
Text Notes 4500 5700 0    50   ~ 0
24V supply and sensing for submersible pressure sensor
$Comp
L Switch:SW_SPST SW1
U 1 1 5E59822C
P 2150 5800
F 0 "SW1" H 2150 6035 50  0000 C CNN
F 1 "OFFLINE" H 2150 5944 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 2150 5800 50  0001 C CNN
F 3 "~" H 2150 5800 50  0001 C CNN
	1    2150 5800
	1    0    0    -1  
$EndComp
Text GLabel 3450 1800 2    50   Input ~ 0
OFFLINE_MODE
Text GLabel 1800 5800 0    50   Input ~ 0
OFFLINE_MODE
$Comp
L power:GND #PWR012
U 1 1 5E598D3F
P 2550 5800
F 0 "#PWR012" H 2550 5550 50  0001 C CNN
F 1 "GND" H 2555 5627 50  0000 C CNN
F 2 "" H 2550 5800 50  0001 C CNN
F 3 "" H 2550 5800 50  0001 C CNN
	1    2550 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 5800 1950 5800
Wire Wire Line
	2350 5800 2550 5800
$Comp
L power:GND #PWR07
U 1 1 5E5A2A26
P 5800 3550
F 0 "#PWR07" H 5800 3300 50  0001 C CNN
F 1 "GND" H 5805 3377 50  0000 C CNN
F 2 "" H 5800 3550 50  0001 C CNN
F 3 "" H 5800 3550 50  0001 C CNN
	1    5800 3550
	1    0    0    -1  
$EndComp
Text GLabel 5650 4300 0    50   Input ~ 0
BOOST24POS
$Comp
L Transistor_FET:BS170 Q1
U 1 1 5E5F9A13
P 5700 3100
F 0 "Q1" H 5904 3146 50  0000 L CNN
F 1 "BS170" H 5904 3055 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline_Wide" H 5900 3025 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/BS/BS170.pdf" H 5700 3100 50  0001 L CNN
	1    5700 3100
	1    0    0    -1  
$EndComp
Text GLabel 3450 1650 2    50   Input ~ 0
BOOST_ENABLE
Text GLabel 5350 3100 0    50   Input ~ 0
BOOST_ENABLE
Wire Wire Line
	5350 3100 5450 3100
Wire Wire Line
	5800 3300 5800 3550
Wire Wire Line
	5800 2750 5800 2900
Text Notes 4650 3400 0    50   ~ 0
Power control for \n24V boost converter \npower supply
Text GLabel 2200 7050 2    50   Input ~ 0
BOOST24POS
Text GLabel 2200 7250 2    50   Input ~ 0
LDR_SENSE
Wire Wire Line
	2000 6950 2200 6950
Wire Wire Line
	2000 7050 2200 7050
Text GLabel 2200 7150 2    50   Input ~ 0
PRESS_SENSE
Wire Wire Line
	2000 6850 2200 6850
NoConn ~ 3150 1350
$Comp
L power:GND #PWR09
U 1 1 5E62D6DE
P 2850 6750
F 0 "#PWR09" H 2850 6500 50  0001 C CNN
F 1 "GND" H 2855 6577 50  0000 C CNN
F 2 "" H 2850 6750 50  0001 C CNN
F 3 "" H 2850 6750 50  0001 C CNN
	1    2850 6750
	1    0    0    -1  
$EndComp
Text Notes 1000 7500 0    50   ~ 0
Test Points
Wire Wire Line
	2000 6750 2850 6750
Text GLabel 2200 6950 2    50   Input ~ 0
BATTERY+12
Wire Wire Line
	2000 7150 2200 7150
Text GLabel 2200 6850 2    50   Input ~ 0
VCC
Wire Wire Line
	2000 7250 2200 7250
$Comp
L Device:LED D2
U 1 1 5E6621A9
P 5850 4450
F 0 "D2" V 5889 4332 50  0000 R CNN
F 1 "+24 LED" V 5798 4332 50  0000 R CNN
F 2 "LED_THT:LED_D5.0mm" H 5850 4450 50  0001 C CNN
F 3 "~" H 5850 4450 50  0001 C CNN
	1    5850 4450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R4
U 1 1 5E6629B3
P 5850 4800
F 0 "R4" H 5920 4846 50  0000 L CNN
F 1 "1.5K" H 5920 4755 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 5780 4800 50  0001 C CNN
F 3 "" H 5850 4800 50  0001 C CNN
	1    5850 4800
	1    0    0    -1  
$EndComp
Text Notes 5300 4450 0    50   ~ 0
24V Present
$Comp
L Device:R R5
U 1 1 5E56FA45
P 10500 4550
F 0 "R5" H 10570 4596 50  0000 L CNN
F 1 "15K" H 10570 4505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 10430 4550 50  0001 C CNN
F 3 "" H 10500 4550 50  0001 C CNN
	1    10500 4550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 5E570253
P 10500 5300
F 0 "#PWR08" H 10500 5050 50  0001 C CNN
F 1 "GND" H 10505 5127 50  0000 C CNN
F 2 "" H 10500 5300 50  0001 C CNN
F 3 "" H 10500 5300 50  0001 C CNN
	1    10500 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	10500 5150 10500 5300
Wire Wire Line
	10500 4700 10500 4800
Wire Wire Line
	10500 4250 10500 4400
Text GLabel 10300 4250 0    50   Input ~ 0
BATTERY+12
Text GLabel 10350 4800 0    50   Input ~ 0
BATTLEVEL_SENSE
Wire Wire Line
	10350 4800 10500 4800
Connection ~ 10500 4800
Wire Wire Line
	10500 4800 10500 4850
Text Notes 9400 4550 0    50   ~ 0
Battery voltage sensing \nfor 12V battery
$Comp
L Device:R R6
U 1 1 5E56FE95
P 10500 5000
F 0 "R6" H 10570 5046 50  0000 L CNN
F 1 "4.7K" H 10570 4955 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 10430 5000 50  0001 C CNN
F 3 "" H 10500 5000 50  0001 C CNN
	1    10500 5000
	1    0    0    -1  
$EndComp
NoConn ~ 1500 2700
Wire Wire Line
	10300 4250 10500 4250
NoConn ~ 3150 1500
Wire Wire Line
	5650 4300 5850 4300
Wire Wire Line
	5850 4600 5850 4650
$Comp
L power:GND #PWR010
U 1 1 5E63CC30
P 5850 5000
F 0 "#PWR010" H 5850 4750 50  0001 C CNN
F 1 "GND" H 5855 4827 50  0000 C CNN
F 2 "" H 5850 5000 50  0001 C CNN
F 3 "" H 5850 5000 50  0001 C CNN
	1    5850 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 4950 5850 5000
$Comp
L AW_Misc_Library:SDLA12TA_SLA_Charge_Module U4
U 1 1 602501B7
P 10050 1650
F 0 "U4" H 10050 1750 50  0000 C CNN
F 1 "SDLA12TA_SLA_Charge_Module" H 10050 1700 50  0000 C CNN
F 2 "Aw_footprints:SDLA12TA_Module" H 10050 1850 50  0001 C CNN
F 3 "" H 10050 1850 50  0001 C CNN
	1    10050 1650
	1    0    0    -1  
$EndComp
Text GLabel 9500 1850 0    50   Input ~ 0
PANEL_NEG
Text GLabel 9500 1750 0    50   Input ~ 0
PANEL_POS
Wire Wire Line
	9500 1750 9650 1750
Wire Wire Line
	9500 1850 9650 1850
Text GLabel 10600 1750 2    50   Input ~ 0
BATTERY+12
$Comp
L power:GND #PWR011
U 1 1 60257BB5
P 10600 1850
F 0 "#PWR011" H 10600 1600 50  0001 C CNN
F 1 "GND" H 10605 1677 50  0000 C CNN
F 2 "" H 10600 1850 50  0001 C CNN
F 3 "" H 10600 1850 50  0001 C CNN
	1    10600 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	10450 1750 10600 1750
Wire Wire Line
	10450 1850 10600 1850
Wire Wire Line
	10550 3200 10850 3200
NoConn ~ 3150 2400
Wire Notes Line
	8650 500  11150 500 
Wire Notes Line
	11150 500  11150 5700
Wire Notes Line
	11150 5700 8650 5700
Wire Notes Line
	8650 5700 8650 500 
Text Notes 8650 5700 0    50   ~ 0
Power Supply 
Wire Notes Line
	8500 500  8500 5700
Wire Notes Line
	8500 5700 4500 5700
Wire Notes Line
	4500 5700 4500 500 
Wire Notes Line
	4500 500  8500 500 
$Comp
L Pycom-Tank-Sensor-Submersible-rescue:LoPy4-pycom U1
U 1 1 5BD53A8A
P 1500 700
F 0 "U1" H 2325 787 60  0000 C CNN
F 1 "LoPy4" H 2325 681 60  0000 C CNN
F 2 "Aw_footprints:LoPy_with_headers" H 1500 700 60  0001 C CNN
F 3 "" H 1500 700 60  0001 C CNN
	1    1500 700 
	1    0    0    -1  
$EndComp
$Comp
L AW_Misc_Library:Adafruit_ADS1115_Module U2
U 1 1 6025370D
P 5750 6100
F 0 "U2" H 5700 6150 50  0000 L CNN
F 1 "Adafruit_ADS1115_Module" V 5950 5100 50  0000 L CNN
F 2 "Aw_footprints:Adafruit_ADS1115_Module" H 5750 6100 50  0001 C CNN
F 3 "" H 5750 6100 50  0001 C CNN
	1    5750 6100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR01
U 1 1 602555ED
P 4900 7050
F 0 "#PWR01" H 4900 6800 50  0001 C CNN
F 1 "GND" H 4905 6877 50  0000 C CNN
F 2 "" H 4900 7050 50  0001 C CNN
F 3 "" H 4900 7050 50  0001 C CNN
	1    4900 7050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 7000 4900 7000
Wire Wire Line
	4900 7000 4900 7050
Text GLabel 5350 7100 0    50   Input ~ 0
3v3
Wire Wire Line
	5350 7100 5500 7100
Text GLabel 5350 6800 0    50   Input ~ 0
SDA
Wire Wire Line
	5350 6800 5500 6800
Text GLabel 5350 6900 0    50   Input ~ 0
SCL
Wire Wire Line
	5350 6900 5500 6900
NoConn ~ 5500 6700
NoConn ~ 5500 6600
Wire Wire Line
	5350 6300 5500 6300
NoConn ~ 5500 6200
Text GLabel 5350 6500 0    50   Input ~ 0
BATTLEVEL_SENSE
Wire Wire Line
	5350 6500 5500 6500
$Comp
L AW_Misc_Library:XL6009E1_DC-DC_Stepup_Converter U3
U 1 1 602630BD
P 7650 1500
F 0 "U3" H 7600 1550 50  0000 L CNN
F 1 "XL6009E1_DC-DC_Stepup_Converter" H 7000 950 50  0000 L CNN
F 2 "Aw_footprints:XL6009E1_DC-DC_Converter" H 7650 1500 50  0001 C CNN
F 3 "" H 7650 1500 50  0001 C CNN
	1    7650 1500
	1    0    0    -1  
$EndComp
Text GLabel 7150 1800 0    50   Input ~ 0
BOOST24POS
Wire Wire Line
	7150 1800 7400 1800
$Comp
L power:GND #PWR06
U 1 1 60267C29
P 6750 1900
F 0 "#PWR06" H 6750 1650 50  0001 C CNN
F 1 "GND" H 6755 1727 50  0000 C CNN
F 2 "" H 6750 1900 50  0001 C CNN
F 3 "" H 6750 1900 50  0001 C CNN
	1    6750 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 1900 7400 1900
$Comp
L Relay:EC2-12NU K1
U 1 1 60269BAC
P 7300 3750
F 0 "K1" V 6533 3750 50  0000 C CNN
F 1 "EC2-12NU" V 6624 3750 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_Kemet_EC2" H 7300 3750 50  0001 C CNN
F 3 "https://content.kemet.com/datasheets/KEM_R7002_EC2_EE2.pdf" H 7300 3750 50  0001 C CNN
	1    7300 3750
	0    1    1    0   
$EndComp
Text GLabel 7850 3350 2    50   Input ~ 0
BATTERY+12
Wire Wire Line
	7600 3350 7700 3350
Text GLabel 7850 3850 2    50   Input ~ 0
BATTERY+12
Wire Wire Line
	7600 3850 7700 3850
Text GLabel 7150 1600 0    50   Input ~ 0
BOOST_SUPPLY
Wire Wire Line
	7150 1600 7400 1600
Text GLabel 6800 3750 0    50   Input ~ 0
BOOST_SUPPLY
Wire Wire Line
	6800 3750 6900 3750
NoConn ~ 7600 3650
NoConn ~ 7600 4050
Text GLabel 7150 1100 0    50   Input ~ 0
BOOST24POS
Wire Wire Line
	7150 1100 7400 1100
$Comp
L power:GND #PWR05
U 1 1 6029DF18
P 6400 1900
F 0 "#PWR05" H 6400 1650 50  0001 C CNN
F 1 "GND" H 6405 1727 50  0000 C CNN
F 2 "" H 6400 1900 50  0001 C CNN
F 3 "" H 6400 1900 50  0001 C CNN
	1    6400 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 1700 6400 1700
Wire Wire Line
	6400 1700 6400 1900
$Comp
L power:GND #PWR02
U 1 1 602A17A4
P 5900 1100
F 0 "#PWR02" H 5900 850 50  0001 C CNN
F 1 "GND" H 5905 927 50  0000 C CNN
F 2 "" H 5900 1100 50  0001 C CNN
F 3 "" H 5900 1100 50  0001 C CNN
	1    5900 1100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 602AD746
P 6300 1000
F 0 "R1" V 6200 950 50  0000 L CNN
F 1 "100R" V 6400 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 6230 1000 50  0001 C CNN
F 3 "" H 6300 1000 50  0001 C CNN
	1    6300 1000
	0    1    1    0   
$EndComp
Text GLabel 7150 850  0    50   Input ~ 0
PRESS_SENSE
Wire Wire Line
	6150 1000 5900 1000
Wire Wire Line
	5900 1000 5900 1100
Wire Wire Line
	6450 1000 7250 1000
Wire Wire Line
	7150 850  7250 850 
Wire Wire Line
	7250 850  7250 1000
Connection ~ 7250 1000
Wire Wire Line
	7250 1000 7400 1000
Text GLabel 6800 3350 0    50   Input ~ 0
BOOST_SWITCH
Text Notes 5300 4600 0    20   ~ 0
This is intended as a green LED\n with 2V drop and 15mA.
Text GLabel 5350 6400 0    50   Input ~ 0
PRESS_SENSE
Wire Wire Line
	5350 6400 5500 6400
Wire Notes Line
	1000 6500 3000 6500
Wire Notes Line
	3000 6500 3000 7500
Wire Notes Line
	3000 7500 1000 7500
Wire Notes Line
	1000 7500 1000 6500
Wire Notes Line
	4500 5850 6350 5850
Wire Notes Line
	6350 5850 6350 7600
Wire Notes Line
	6350 7600 4500 7600
Wire Notes Line
	4500 7600 4500 5850
Text Notes 4500 7600 0    50   ~ 0
Analogue to Digital Conversion
Text Notes 7050 2150 0    50   ~ 0
Set this output voltage to 24VDC
Wire Wire Line
	10150 2500 10300 2500
Wire Wire Line
	9350 2400 9650 2400
NoConn ~ 10150 2400
NoConn ~ 9650 2500
NoConn ~ 7900 1000
NoConn ~ 7900 1100
Wire Wire Line
	10250 950  10450 950 
NoConn ~ 10250 1050
NoConn ~ 9750 1050
$Comp
L AW_Misc_Library:Pimoroni_BME280_Module U5
U 1 1 6036729E
P 2050 4450
F 0 "U5" H 1800 4500 50  0000 L CNN
F 1 "Pimoroni_BME280_Module" H 1400 4450 50  0000 L CNN
F 2 "Aw_footprints:Pimoroni BME280 Module" H 2050 4450 50  0001 C CNN
F 3 "" H 2050 4450 50  0001 C CNN
	1    2050 4450
	1    0    0    -1  
$EndComp
Text GLabel 1450 4700 0    50   Input ~ 0
SDA
Text GLabel 1450 4800 0    50   Input ~ 0
SCL
Wire Wire Line
	1450 4700 1650 4700
Wire Wire Line
	1450 4800 1650 4800
Text GLabel 1450 4600 0    50   Input ~ 0
3v3
Wire Wire Line
	1450 4600 1650 4600
$Comp
L power:GND #PWR013
U 1 1 6036ED96
P 1400 5000
F 0 "#PWR013" H 1400 4750 50  0001 C CNN
F 1 "GND" H 1405 4827 50  0000 C CNN
F 2 "" H 1400 5000 50  0001 C CNN
F 3 "" H 1400 5000 50  0001 C CNN
	1    1400 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 5000 1650 5000
Text Notes 1800 6000 0    20   ~ 0
Close this jumper for offline operation.\nThis suppresses LoRaWAN connectivity.
Wire Notes Line
	1000 3500 3850 3500
Wire Notes Line
	3850 3500 3850 6200
Wire Notes Line
	3850 6200 1000 6200
Wire Notes Line
	1000 6200 1000 3500
Text Notes 1000 6200 0    50   ~ 0
Environment Monitor and Control
Text Notes 2950 5300 0    50   ~ 0
LDR used to monitor \nenclosure integrity
NoConn ~ 3150 2550
Text GLabel 5350 2750 0    50   Input ~ 0
BOOST_SWITCH
Wire Wire Line
	5350 2750 5800 2750
Wire Wire Line
	6800 3350 6900 3350
$Comp
L Connector_Generic:Conn_01x01 J5
U 1 1 602AF7A6
P 1800 6750
F 0 "J5" H 2400 6750 50  0000 C CNN
F 1 "TP_GND" H 2100 6750 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 6750 50  0001 C CNN
F 3 "~" H 1800 6750 50  0001 C CNN
	1    1800 6750
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J6
U 1 1 602B694C
P 1800 6850
F 0 "J6" H 2400 6850 50  0000 C CNN
F 1 "TP_5V" H 2100 6850 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 6850 50  0001 C CNN
F 3 "~" H 1800 6850 50  0001 C CNN
	1    1800 6850
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J7
U 1 1 602B6AC9
P 1800 6950
F 0 "J7" H 2400 6950 50  0000 C CNN
F 1 "TP_12V" H 2100 6950 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 6950 50  0001 C CNN
F 3 "~" H 1800 6950 50  0001 C CNN
	1    1800 6950
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J8
U 1 1 602B6C1C
P 1800 7050
F 0 "J8" H 2400 7050 50  0000 C CNN
F 1 "TP_24V" H 2100 7050 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 7050 50  0001 C CNN
F 3 "~" H 1800 7050 50  0001 C CNN
	1    1800 7050
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J9
U 1 1 602B6E06
P 1800 7150
F 0 "J9" H 2400 7150 50  0000 C CNN
F 1 "TP_PRESS" H 2100 7150 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 7150 50  0001 C CNN
F 3 "~" H 1800 7150 50  0001 C CNN
	1    1800 7150
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J10
U 1 1 602B7052
P 1800 7250
F 0 "J10" H 2400 7250 50  0000 C CNN
F 1 "TP_LDR" H 2100 7250 50  0000 C CNN
F 2 "TestPoint:TestPoint_Loop_D2.60mm_Drill0.9mm_Beaded" H 1800 7250 50  0001 C CNN
F 3 "~" H 1800 7250 50  0001 C CNN
	1    1800 7250
	-1   0    0    1   
$EndComp
$Comp
L Device:D D1
U 1 1 6025E50A
P 7300 2850
F 0 "D1" H 7300 2633 50  0000 C CNN
F 1 "D" H 7300 2724 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P12.70mm_Horizontal" H 7300 2850 50  0001 C CNN
F 3 "~" H 7300 2850 50  0001 C CNN
	1    7300 2850
	-1   0    0    1   
$EndComp
Wire Wire Line
	7450 2850 7700 2850
Wire Wire Line
	7700 2850 7700 3350
Connection ~ 7700 3350
Wire Wire Line
	7700 3350 7850 3350
Wire Wire Line
	7150 2850 6900 2850
Wire Wire Line
	6900 2850 6900 3350
Connection ~ 6900 3350
Wire Wire Line
	6900 3350 7000 3350
$Comp
L Mechanical:MountingHole H2
U 1 1 6028142F
P 7050 6050
F 0 "H2" H 7150 6096 50  0000 L CNN
F 1 "MountingHole" H 7150 6005 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 7050 6050 50  0001 C CNN
F 3 "~" H 7050 6050 50  0001 C CNN
	1    7050 6050
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 60281FB9
P 7050 6200
F 0 "H3" H 7150 6246 50  0000 L CNN
F 1 "MountingHole" H 7150 6155 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 7050 6200 50  0001 C CNN
F 3 "~" H 7050 6200 50  0001 C CNN
	1    7050 6200
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H1
U 1 1 602823D0
P 7050 5900
F 0 "H1" H 7150 5946 50  0000 L CNN
F 1 "MountingHole" H 7150 5855 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 7050 5900 50  0001 C CNN
F 3 "~" H 7050 5900 50  0001 C CNN
	1    7050 5900
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 602829DF
P 7050 6350
F 0 "H4" H 7150 6396 50  0000 L CNN
F 1 "MountingHole" H 7150 6305 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 7050 6350 50  0001 C CNN
F 3 "~" H 7050 6350 50  0001 C CNN
	1    7050 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7600 4250 7700 4250
Wire Wire Line
	7700 4250 7700 3850
Connection ~ 7700 3850
Wire Wire Line
	7700 3850 7850 3850
Wire Wire Line
	7000 4150 6900 4150
Wire Wire Line
	6900 4150 6900 3750
Connection ~ 6900 3750
Wire Wire Line
	6900 3750 7000 3750
$Comp
L Device:R R7
U 1 1 6027C440
P 5450 3350
F 0 "R7" H 5520 3396 50  0000 L CNN
F 1 "10K" H 5520 3305 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 5380 3350 50  0001 C CNN
F 3 "" H 5450 3350 50  0001 C CNN
	1    5450 3350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR014
U 1 1 6027CCC6
P 5450 3550
F 0 "#PWR014" H 5450 3300 50  0001 C CNN
F 1 "GND" H 5455 3377 50  0000 C CNN
F 2 "" H 5450 3550 50  0001 C CNN
F 3 "" H 5450 3550 50  0001 C CNN
	1    5450 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 3200 5450 3100
Connection ~ 5450 3100
Wire Wire Line
	5450 3100 5500 3100
Wire Wire Line
	5450 3550 5450 3500
$EndSCHEMATC
