EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title "Pump Remote Control Module"
Date "2020-11-20"
Rev "1.0"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 "Ashley Woods"
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 5F427FD1
P 3450 3200
F 0 "J1" H 3450 4681 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 3450 4590 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" H 3450 3200 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3450 3200 50  0001 C CNN
	1    3450 3200
	1    0    0    -1  
$EndComp
Text GLabel 2450 2300 0    50   Input ~ 0
TXD
Text GLabel 2450 2400 0    50   Input ~ 0
RXD
Wire Wire Line
	2450 2300 2650 2300
Wire Wire Line
	2450 2400 2650 2400
Wire Wire Line
	3050 4500 3050 4700
Wire Wire Line
	3150 4500 3150 4700
Wire Wire Line
	3150 4700 3050 4700
Wire Wire Line
	3250 4500 3250 4700
Wire Wire Line
	3250 4700 3150 4700
Connection ~ 3150 4700
Wire Wire Line
	3350 4500 3350 4700
Wire Wire Line
	3350 4700 3250 4700
Connection ~ 3250 4700
Connection ~ 3350 4700
Wire Wire Line
	3550 4500 3550 4700
Wire Wire Line
	3650 4500 3650 4700
Wire Wire Line
	3650 4700 3550 4700
Connection ~ 3550 4700
Wire Wire Line
	3750 4500 3750 4700
Wire Wire Line
	3750 4700 3650 4700
Connection ~ 3650 4700
Text GLabel 3050 1550 0    50   Input ~ 0
5V
Text GLabel 3050 1400 0    50   Input ~ 0
3v3
Wire Wire Line
	3350 1900 3350 1550
Wire Wire Line
	3050 1400 3550 1400
Wire Wire Line
	3550 1400 3550 1900
Text GLabel 13250 6700 0    50   Input ~ 0
3v3
Wire Wire Line
	13250 6700 13450 6700
Text GLabel 5150 2600 2    50   Input ~ 0
SDA
Text GLabel 5150 2700 2    50   Input ~ 0
SCL
Wire Wire Line
	4250 2600 4700 2600
Wire Wire Line
	4250 2700 5000 2700
Text GLabel 13250 7000 0    50   Input ~ 0
SDA
Text GLabel 13250 6900 0    50   Input ~ 0
SCL
Wire Wire Line
	13250 6900 13450 6900
Wire Wire Line
	13250 7000 13450 7000
$Comp
L power:GND #PWR015
U 1 1 5F449619
P 12900 6800
F 0 "#PWR015" H 12900 6550 50  0001 C CNN
F 1 "GND" H 12905 6627 50  0000 C CNN
F 2 "" H 12900 6800 50  0001 C CNN
F 3 "" H 12900 6800 50  0001 C CNN
	1    12900 6800
	1    0    0    -1  
$EndComp
Wire Wire Line
	12900 6800 13450 6800
$Comp
L power:GND #PWR05
U 1 1 5F44CF80
P 2850 4750
F 0 "#PWR05" H 2850 4500 50  0001 C CNN
F 1 "GND" H 2855 4577 50  0000 C CNN
F 2 "" H 2850 4750 50  0001 C CNN
F 3 "" H 2850 4750 50  0001 C CNN
	1    2850 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R7
U 1 1 5F46B4FF
P 4700 2300
F 0 "R7" H 4770 2346 50  0000 L CNN
F 1 "10K" H 4770 2255 50  0000 L CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 4630 2300 50  0001 C CNN
F 3 "~" H 4700 2300 50  0001 C CNN
	1    4700 2300
	1    0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 5F477B1D
P 5000 2300
F 0 "R8" H 5070 2346 50  0000 L CNN
F 1 "10K" H 5070 2255 50  0000 L CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 4930 2300 50  0001 C CNN
F 3 "~" H 5000 2300 50  0001 C CNN
	1    5000 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 2450 4700 2600
Connection ~ 4700 2600
Wire Wire Line
	4700 2600 5150 2600
Wire Wire Line
	5000 2450 5000 2700
Connection ~ 5000 2700
Wire Wire Line
	5000 2700 5150 2700
Text GLabel 5300 2150 2    50   Input ~ 0
3v3
Wire Wire Line
	4700 2150 5000 2150
Wire Wire Line
	5000 2150 5300 2150
Connection ~ 5000 2150
$Comp
L Device:LED D5
U 1 1 5F5FB393
P 13950 8700
F 0 "D5" H 13943 8445 50  0000 C CNN
F 1 "5V Present" H 13943 8536 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 13950 8700 50  0001 C CNN
F 3 "~" H 13950 8700 50  0001 C CNN
	1    13950 8700
	-1   0    0    1   
$EndComp
$Comp
L Device:R R18
U 1 1 5F5FB3A7
P 13400 8700
F 0 "R18" V 13193 8700 50  0000 C CNN
F 1 "220R" V 13284 8700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 13330 8700 50  0001 C CNN
F 3 "~" H 13400 8700 50  0001 C CNN
	1    13400 8700
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR035
U 1 1 5F5FB3B1
P 14400 8750
F 0 "#PWR035" H 14400 8500 50  0001 C CNN
F 1 "GND" H 14405 8577 50  0000 C CNN
F 2 "" H 14400 8750 50  0001 C CNN
F 3 "" H 14400 8750 50  0001 C CNN
	1    14400 8750
	1    0    0    -1  
$EndComp
Text GLabel 13100 8700 0    50   Input ~ 0
5V
Text GLabel 2450 2700 0    50   Input ~ 0
Semiauto_Mode_Button
Text GLabel 2450 3500 0    50   Input ~ 0
Pump_Stop_Button
Wire Wire Line
	2650 2600 2450 2600
Wire Wire Line
	2450 2700 2650 2700
Wire Wire Line
	2650 2800 2450 2800
Text GLabel 2450 3000 0    50   Input ~ 0
Manual_Mode_Button_LED
Text Notes 2400 5100 0    50   ~ 0
Connection to Raspberry Pi Zero W 40 Pin Header
NoConn ~ 4250 2300
NoConn ~ 4250 2400
NoConn ~ 4250 3000
NoConn ~ 4250 3100
NoConn ~ 4250 3900
NoConn ~ 4250 4000
Text Notes 1750 1600 0    50   ~ 0
Pi is powered via this 5V line
Text Notes 13100 7250 0    50   ~ 0
SHT31 Temp Humidity Module\nI2C address 0x44
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5F450BB3
P 13700 3950
F 0 "J2" H 13780 3992 50  0000 L CNN
F 1 "Serial Console Connector" H 13780 3901 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 13700 3950 50  0001 C CNN
F 3 "~" H 13700 3950 50  0001 C CNN
	1    13700 3950
	1    0    0    -1  
$EndComp
Text GLabel 13200 3950 0    50   Input ~ 0
TXD
Text GLabel 13200 4050 0    50   Input ~ 0
RXD
Wire Wire Line
	13200 3950 13500 3950
Wire Wire Line
	13200 4050 13500 4050
$Comp
L power:GND #PWR011
U 1 1 5F44B884
P 12850 3850
F 0 "#PWR011" H 12850 3600 50  0001 C CNN
F 1 "GND" H 12855 3677 50  0000 C CNN
F 2 "" H 12850 3850 50  0001 C CNN
F 3 "" H 12850 3850 50  0001 C CNN
	1    12850 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	12850 3850 13500 3850
Wire Wire Line
	13100 8700 13250 8700
Wire Wire Line
	13550 8700 13800 8700
Wire Wire Line
	14100 8700 14400 8700
Wire Wire Line
	14400 8700 14400 8750
$Comp
L Connector:TestPoint TP1
U 1 1 5F7666D2
P 1750 6150
F 0 "TP1" H 1808 6268 50  0000 L CNN
F 1 "TP GND" H 1808 6177 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 1950 6150 50  0001 C CNN
F 3 "~" H 1950 6150 50  0001 C CNN
	1    1750 6150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR050
U 1 1 5F766B81
P 1750 6350
F 0 "#PWR050" H 1750 6100 50  0001 C CNN
F 1 "GND" H 1755 6177 50  0000 C CNN
F 2 "" H 1750 6350 50  0001 C CNN
F 3 "" H 1750 6350 50  0001 C CNN
	1    1750 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	1750 6150 1750 6350
Text GLabel 2450 2600 0    50   Input ~ 0
Manual_Mode_Button
Text GLabel 2450 2800 0    50   Input ~ 0
Auto_Mode_Button
Text GLabel 2450 3100 0    50   Input ~ 0
Semiauto_Mode_Button_LED
Text GLabel 2450 3200 0    50   Input ~ 0
Auto_Mode_Button_LED
Wire Wire Line
	2450 3000 2650 3000
Wire Wire Line
	2650 3100 2450 3100
Wire Wire Line
	2450 3200 2650 3200
Text GLabel 2450 3400 0    50   Input ~ 0
Pump_Start_Button
Text GLabel 2450 3700 0    50   Input ~ 0
Pump_Stop_Button_LED
Text GLabel 2450 3600 0    50   Input ~ 0
Pump_Start_Button_LED
Wire Wire Line
	2450 3400 2650 3400
Wire Wire Line
	2450 3500 2650 3500
Wire Wire Line
	2450 3600 2650 3600
Wire Wire Line
	2450 3700 2650 3700
NoConn ~ 4250 2900
Wire Wire Line
	4250 3300 4500 3300
Text GLabel 4500 3300 2    50   Input ~ 0
SHUTDOWN
NoConn ~ 4250 3400
NoConn ~ 4250 3500
NoConn ~ 4250 3600
NoConn ~ 4250 3700
Text GLabel 2450 3800 0    50   Input ~ 0
Alarm_Button
Text GLabel 2450 3900 0    50   Input ~ 0
Alarm_Button_LED
Wire Wire Line
	2450 3800 2650 3800
Wire Wire Line
	2450 3900 2650 3900
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 5FC530DE
P 14700 1150
F 0 "J3" H 14780 1192 50  0000 L CNN
F 1 "Power Input Connector" H 14780 1101 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 14700 1150 50  0001 C CNN
F 3 "~" H 14700 1150 50  0001 C CNN
	1    14700 1150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5FC55527
P 13950 1150
F 0 "#PWR0101" H 13950 900 50  0001 C CNN
F 1 "GND" H 13955 977 50  0000 C CNN
F 2 "" H 13950 1150 50  0001 C CNN
F 3 "" H 13950 1150 50  0001 C CNN
	1    13950 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	14500 1050 13950 1050
Wire Wire Line
	13950 1050 13950 1150
Text Notes 13450 950  0    50   ~ 0
This comes direct from the external plug pack.\nVoltage input 8-20 VDC.
Text GLabel 12800 5400 0    50   Input ~ 0
SHUTDOWN
$Comp
L power:GND #PWR0102
U 1 1 5FC5A578
P 13850 5400
F 0 "#PWR0102" H 13850 5150 50  0001 C CNN
F 1 "GND" H 13855 5227 50  0000 C CNN
F 2 "" H 13850 5400 50  0001 C CNN
F 3 "" H 13850 5400 50  0001 C CNN
	1    13850 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	12800 5400 12950 5400
Wire Wire Line
	13150 5000 12950 5000
Wire Wire Line
	12950 5000 12950 5400
Connection ~ 12950 5400
Wire Wire Line
	12950 5400 13150 5400
Wire Wire Line
	13550 5000 13750 5000
Wire Wire Line
	13750 5000 13750 5400
Wire Wire Line
	13550 5400 13750 5400
Connection ~ 13750 5400
Wire Wire Line
	13750 5400 13850 5400
$Comp
L Mechanical:MountingHole H1
U 1 1 5FC6495A
P 1850 7650
F 0 "H1" H 1950 7699 50  0000 L CNN
F 1 "Mount" H 1950 7608 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 1850 7650 50  0001 C CNN
F 3 "~" H 1850 7650 50  0001 C CNN
	1    1850 7650
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 5FC64F22
P 1850 8400
F 0 "H2" H 1950 8449 50  0000 L CNN
F 1 "Mount" H 1950 8358 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 1850 8400 50  0001 C CNN
F 3 "~" H 1850 8400 50  0001 C CNN
	1    1850 8400
	1    0    0    -1  
$EndComp
$Comp
L Connector:TestPoint TP2
U 1 1 5FC6F0E8
P 2300 6150
F 0 "TP2" H 2358 6268 50  0000 L CNN
F 1 "TP +5V" H 2358 6177 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 2500 6150 50  0001 C CNN
F 3 "~" H 2500 6150 50  0001 C CNN
	1    2300 6150
	1    0    0    -1  
$EndComp
Text GLabel 2250 6450 0    50   Input ~ 0
5V
Wire Wire Line
	2300 6150 2300 6450
Wire Wire Line
	2300 6450 2250 6450
Wire Wire Line
	8750 1000 9000 1000
Text GLabel 9000 1000 2    50   Input ~ 0
Pump_Start_Button
Wire Wire Line
	8050 1000 8350 1000
Text GLabel 7400 1400 0    50   Input ~ 0
Pump_Start_Button_LED
$Comp
L Device:R R2
U 1 1 5FB9B26E
P 7700 1400
F 0 "R2" V 7493 1400 50  0000 C CNN
F 1 "4k3" V 7584 1400 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 7630 1400 50  0001 C CNN
F 3 "~" H 7700 1400 50  0001 C CNN
	1    7700 1400
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q1
U 1 1 5FB9A51A
P 8150 1400
F 0 "Q1" H 8341 1446 50  0000 L CNN
F 1 "P2N2222A" H 8341 1355 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 8350 1325 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8150 1400 50  0001 L CNN
	1    8150 1400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5FB857FB
P 9050 1300
F 0 "R1" V 9150 1300 50  0000 C CNN
F 1 "220R" V 9050 1300 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8980 1300 50  0001 C CNN
F 3 "~" H 9050 1300 50  0001 C CNN
	1    9050 1300
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 600  11450 600 
Wire Notes Line
	11450 600  11450 9300
Wire Notes Line
	11450 9300 6150 9300
Text Notes 6250 9250 0    50   ~ 0
Push buttons and associated LEDs
$Comp
L AW_Misc_Library:PCB_Switch_RS479-1413 SW7
U 1 1 5FC86A4D
P 13850 5800
F 0 "SW7" H 13638 6446 50  0000 L CNN
F 1 "Shutdown" H 13638 6355 50  0000 L CNN
F 2 "Aw_footprints:PCB Switch RS 479-1413" H 13850 6000 50  0001 C CNN
F 3 "~" H 13850 6000 50  0001 C CNN
	1    13850 5800
	1    0    0    -1  
$EndComp
$Comp
L AW_Misc_Library:GY_SHT31-Breakout-pycom U1
U 1 1 5FC876CA
P 13500 7150
F 0 "U1" H 13828 7521 50  0000 L CNN
F 1 "GY_SHT31-Breakout-pycom" H 13828 7430 50  0000 L CNN
F 2 "Aw_footprints:GY_SHT31_Breakout" H 13550 7000 50  0001 C CNN
F 3 "" H 13550 7000 50  0001 C CNN
	1    13500 7150
	1    0    0    -1  
$EndComp
NoConn ~ 14500 1150
Wire Wire Line
	3350 4700 3450 4700
Wire Wire Line
	3450 4500 3450 4700
Connection ~ 3450 4700
Wire Wire Line
	3450 4700 3550 4700
Wire Wire Line
	3050 1550 3250 1550
Wire Wire Line
	3250 1900 3250 1550
Connection ~ 3250 1550
Wire Wire Line
	3250 1550 3350 1550
Wire Wire Line
	3650 1900 3650 1400
Wire Wire Line
	3650 1400 3550 1400
Connection ~ 3550 1400
Wire Wire Line
	2850 4750 2850 4700
Wire Wire Line
	2850 4700 3050 4700
Connection ~ 3050 4700
$Comp
L Switch:SW_Push_LED SW1
U 1 1 5FCB6E73
P 8550 1100
F 0 "SW1" H 8550 1485 50  0000 C CNN
F 1 "Pump Start Button" H 8550 1394 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 8550 1400 50  0001 C CNN
F 3 "~" H 8550 1400 50  0001 C CNN
	1    8550 1100
	1    0    0    -1  
$EndComp
Text GLabel 9350 1300 2    50   Input ~ 0
5V
$Comp
L power:GND #PWR01
U 1 1 5FCFC127
P 8250 1700
F 0 "#PWR01" H 8250 1450 50  0001 C CNN
F 1 "GND" H 8255 1527 50  0000 C CNN
F 2 "" H 8250 1700 50  0001 C CNN
F 3 "" H 8250 1700 50  0001 C CNN
	1    8250 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 1600 8250 1700
Wire Wire Line
	8350 1100 8250 1100
Wire Wire Line
	8250 1100 8250 1200
Wire Wire Line
	7400 1400 7550 1400
Wire Wire Line
	7850 1400 7950 1400
Wire Wire Line
	9200 1300 9350 1300
Wire Wire Line
	8900 1300 8800 1300
Wire Wire Line
	8800 1300 8800 1100
Wire Wire Line
	8800 1100 8750 1100
Wire Wire Line
	9550 2500 9800 2500
Text GLabel 9800 2500 2    50   Input ~ 0
Pump_Stop_Button
Wire Wire Line
	8850 2500 9150 2500
Text GLabel 8200 2900 0    50   Input ~ 0
Pump_Stop_Button_LED
$Comp
L Device:R R3
U 1 1 5FD4C81F
P 8500 2900
F 0 "R3" V 8293 2900 50  0000 C CNN
F 1 "4k3" V 8384 2900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8430 2900 50  0001 C CNN
F 3 "~" H 8500 2900 50  0001 C CNN
	1    8500 2900
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q2
U 1 1 5FD4C829
P 8950 2900
F 0 "Q2" H 9141 2946 50  0000 L CNN
F 1 "P2N2222A" H 9141 2855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 9150 2825 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8950 2900 50  0001 L CNN
	1    8950 2900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R10
U 1 1 5FD4C833
P 9850 2800
F 0 "R10" V 9950 2800 50  0000 C CNN
F 1 "220R" V 9850 2800 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 9780 2800 50  0001 C CNN
F 3 "~" H 9850 2800 50  0001 C CNN
	1    9850 2800
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 2050 11450 2050
$Comp
L Switch:SW_Push_LED SW2
U 1 1 5FD4C83E
P 9350 2600
F 0 "SW2" H 9350 2985 50  0000 C CNN
F 1 "Pump Stop Button" H 9350 2894 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 9350 2900 50  0001 C CNN
F 3 "~" H 9350 2900 50  0001 C CNN
	1    9350 2600
	1    0    0    -1  
$EndComp
Text GLabel 10150 2800 2    50   Input ~ 0
5V
$Comp
L power:GND #PWR03
U 1 1 5FD4C849
P 9050 3200
F 0 "#PWR03" H 9050 2950 50  0001 C CNN
F 1 "GND" H 9055 3027 50  0000 C CNN
F 2 "" H 9050 3200 50  0001 C CNN
F 3 "" H 9050 3200 50  0001 C CNN
	1    9050 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 3100 9050 3200
Wire Wire Line
	9150 2600 9050 2600
Wire Wire Line
	9050 2600 9050 2700
Wire Wire Line
	8200 2900 8350 2900
Wire Wire Line
	8650 2900 8750 2900
Wire Wire Line
	10000 2800 10150 2800
Wire Wire Line
	9700 2800 9600 2800
Wire Wire Line
	9600 2800 9600 2600
Wire Wire Line
	9600 2600 9550 2600
Wire Notes Line
	6150 9300 6150 600 
Wire Wire Line
	9550 3950 9850 3950
Text GLabel 9850 3950 2    50   Input ~ 0
Manual_Mode_Button
Wire Wire Line
	8850 3950 9150 3950
Text GLabel 8200 4350 0    50   Input ~ 0
Manual_Mode_Button_LED
$Comp
L Device:R R4
U 1 1 5FD61EF8
P 8500 4350
F 0 "R4" V 8293 4350 50  0000 C CNN
F 1 "4k3" V 8384 4350 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8430 4350 50  0001 C CNN
F 3 "~" H 8500 4350 50  0001 C CNN
	1    8500 4350
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q3
U 1 1 5FD61F02
P 8950 4350
F 0 "Q3" H 9141 4396 50  0000 L CNN
F 1 "P2N2222A" H 9141 4305 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 9150 4275 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8950 4350 50  0001 L CNN
	1    8950 4350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R11
U 1 1 5FD61F0C
P 9850 4250
F 0 "R11" V 9950 4250 50  0000 C CNN
F 1 "220R" V 9850 4250 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 9780 4250 50  0001 C CNN
F 3 "~" H 9850 4250 50  0001 C CNN
	1    9850 4250
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 3500 11450 3500
$Comp
L Switch:SW_Push_LED SW3
U 1 1 5FD61F17
P 9350 4050
F 0 "SW3" H 9350 4435 50  0000 C CNN
F 1 "Manual Mode Button" H 9350 4344 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 9350 4350 50  0001 C CNN
F 3 "~" H 9350 4350 50  0001 C CNN
	1    9350 4050
	1    0    0    -1  
$EndComp
Text GLabel 10150 4250 2    50   Input ~ 0
5V
Wire Wire Line
	9050 4550 9050 4650
Wire Wire Line
	9150 4050 9050 4050
Wire Wire Line
	9050 4050 9050 4150
Wire Wire Line
	8200 4350 8350 4350
Wire Wire Line
	8650 4350 8750 4350
Wire Wire Line
	10000 4250 10150 4250
Wire Wire Line
	9700 4250 9600 4250
Wire Wire Line
	9600 4250 9600 4050
Wire Wire Line
	9600 4050 9550 4050
$Comp
L power:GND #PWR06
U 1 1 5FD71FD5
P 9050 4650
F 0 "#PWR06" H 9050 4400 50  0001 C CNN
F 1 "GND" H 9055 4477 50  0000 C CNN
F 2 "" H 9050 4650 50  0001 C CNN
F 3 "" H 9050 4650 50  0001 C CNN
	1    9050 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	9550 5400 9850 5400
Text GLabel 9850 5400 2    50   Input ~ 0
Semiauto_Mode_Button
Wire Wire Line
	8850 5400 9150 5400
Text GLabel 8200 5800 0    50   Input ~ 0
Semiauto_Mode_Button_LED
$Comp
L Device:R R5
U 1 1 5FD71FED
P 8500 5800
F 0 "R5" V 8293 5800 50  0000 C CNN
F 1 "4k3" V 8384 5800 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8430 5800 50  0001 C CNN
F 3 "~" H 8500 5800 50  0001 C CNN
	1    8500 5800
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q4
U 1 1 5FD71FF7
P 8950 5800
F 0 "Q4" H 9141 5846 50  0000 L CNN
F 1 "P2N2222A" H 9141 5755 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 9150 5725 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8950 5800 50  0001 L CNN
	1    8950 5800
	1    0    0    -1  
$EndComp
$Comp
L Device:R R12
U 1 1 5FD72001
P 9850 5700
F 0 "R12" V 9950 5700 50  0000 C CNN
F 1 "220R" V 9850 5700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 9780 5700 50  0001 C CNN
F 3 "~" H 9850 5700 50  0001 C CNN
	1    9850 5700
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 4950 11450 4950
$Comp
L Switch:SW_Push_LED SW4
U 1 1 5FD7200C
P 9350 5500
F 0 "SW4" H 9350 5885 50  0000 C CNN
F 1 "Semiauto Mode Button" H 9350 5794 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 9350 5800 50  0001 C CNN
F 3 "~" H 9350 5800 50  0001 C CNN
	1    9350 5500
	1    0    0    -1  
$EndComp
Text GLabel 10150 5700 2    50   Input ~ 0
5V
$Comp
L power:GND #PWR07
U 1 1 5FD72017
P 9050 6100
F 0 "#PWR07" H 9050 5850 50  0001 C CNN
F 1 "GND" H 9055 5927 50  0000 C CNN
F 2 "" H 9050 6100 50  0001 C CNN
F 3 "" H 9050 6100 50  0001 C CNN
	1    9050 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 6000 9050 6100
Wire Wire Line
	9150 5500 9050 5500
Wire Wire Line
	9050 5500 9050 5600
Wire Wire Line
	8200 5800 8350 5800
Wire Wire Line
	8650 5800 8750 5800
Wire Wire Line
	10000 5700 10150 5700
Wire Wire Line
	9700 5700 9600 5700
Wire Wire Line
	9600 5700 9600 5500
Wire Wire Line
	9600 5500 9550 5500
$Comp
L power:GND #PWR08
U 1 1 5FD7B7E2
P 9050 6100
F 0 "#PWR08" H 9050 5850 50  0001 C CNN
F 1 "GND" H 9055 5927 50  0000 C CNN
F 2 "" H 9050 6100 50  0001 C CNN
F 3 "" H 9050 6100 50  0001 C CNN
	1    9050 6100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR09
U 1 1 5FD7B7EC
P 9050 6100
F 0 "#PWR09" H 9050 5850 50  0001 C CNN
F 1 "GND" H 9055 5927 50  0000 C CNN
F 2 "" H 9050 6100 50  0001 C CNN
F 3 "" H 9050 6100 50  0001 C CNN
	1    9050 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9550 6850 9850 6850
Text GLabel 9850 6850 2    50   Input ~ 0
Auto_Mode_Button
Wire Wire Line
	8850 6850 9150 6850
Text GLabel 8200 7250 0    50   Input ~ 0
Auto_Mode_Button_LED
$Comp
L Device:R R6
U 1 1 5FD7B804
P 8500 7250
F 0 "R6" V 8293 7250 50  0000 C CNN
F 1 "4k3" V 8384 7250 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8430 7250 50  0001 C CNN
F 3 "~" H 8500 7250 50  0001 C CNN
	1    8500 7250
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q5
U 1 1 5FD7B80E
P 8950 7250
F 0 "Q5" H 9141 7296 50  0000 L CNN
F 1 "P2N2222A" H 9141 7205 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 9150 7175 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8950 7250 50  0001 L CNN
	1    8950 7250
	1    0    0    -1  
$EndComp
$Comp
L Device:R R13
U 1 1 5FD7B818
P 9850 7150
F 0 "R13" V 9950 7150 50  0000 C CNN
F 1 "220R" V 9850 7150 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 9780 7150 50  0001 C CNN
F 3 "~" H 9850 7150 50  0001 C CNN
	1    9850 7150
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 6400 11450 6400
$Comp
L Switch:SW_Push_LED SW5
U 1 1 5FD7B823
P 9350 6950
F 0 "SW5" H 9350 7335 50  0000 C CNN
F 1 "Auto Mode Button" H 9350 7244 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 9350 7250 50  0001 C CNN
F 3 "~" H 9350 7250 50  0001 C CNN
	1    9350 6950
	1    0    0    -1  
$EndComp
Text GLabel 10150 7150 2    50   Input ~ 0
5V
$Comp
L power:GND #PWR010
U 1 1 5FD7B82E
P 9050 7550
F 0 "#PWR010" H 9050 7300 50  0001 C CNN
F 1 "GND" H 9055 7377 50  0000 C CNN
F 2 "" H 9050 7550 50  0001 C CNN
F 3 "" H 9050 7550 50  0001 C CNN
	1    9050 7550
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 7450 9050 7550
Wire Wire Line
	9150 6950 9050 6950
Wire Wire Line
	9050 6950 9050 7050
Wire Wire Line
	8200 7250 8350 7250
Wire Wire Line
	8650 7250 8750 7250
Wire Wire Line
	10000 7150 10150 7150
Wire Wire Line
	9700 7150 9600 7150
Wire Wire Line
	9600 7150 9600 6950
Wire Wire Line
	9600 6950 9550 6950
Connection ~ 9050 6100
Wire Wire Line
	9550 8300 9850 8300
Text GLabel 9850 8300 2    50   Input ~ 0
Alarm_Button
Wire Wire Line
	8850 8300 9150 8300
Text GLabel 8200 8700 0    50   Input ~ 0
Alarm_Button_LED
$Comp
L Device:R R9
U 1 1 5FD858A7
P 8500 8700
F 0 "R9" V 8293 8700 50  0000 C CNN
F 1 "4k3" V 8384 8700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8430 8700 50  0001 C CNN
F 3 "~" H 8500 8700 50  0001 C CNN
	1    8500 8700
	0    1    1    0   
$EndComp
$Comp
L AW_Misc_Library:2N2222A Q6
U 1 1 5FD858B1
P 8950 8700
F 0 "Q6" H 9141 8746 50  0000 L CNN
F 1 "P2N2222A" H 9141 8655 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92L_Inline" H 9150 8625 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 8950 8700 50  0001 L CNN
	1    8950 8700
	1    0    0    -1  
$EndComp
$Comp
L Device:R R14
U 1 1 5FD858BB
P 9850 8600
F 0 "R14" V 9950 8600 50  0000 C CNN
F 1 "220R" V 9850 8600 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 9780 8600 50  0001 C CNN
F 3 "~" H 9850 8600 50  0001 C CNN
	1    9850 8600
	0    1    1    0   
$EndComp
Wire Notes Line
	6150 7850 11450 7850
$Comp
L Switch:SW_Push_LED SW6
U 1 1 5FD858C6
P 9350 8400
F 0 "SW6" H 9350 8785 50  0000 C CNN
F 1 "Alarm Button" H 9350 8694 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 9350 8700 50  0001 C CNN
F 3 "~" H 9350 8700 50  0001 C CNN
	1    9350 8400
	1    0    0    -1  
$EndComp
Text GLabel 10150 8600 2    50   Input ~ 0
5V
$Comp
L power:GND #PWR012
U 1 1 5FD858D1
P 9050 9000
F 0 "#PWR012" H 9050 8750 50  0001 C CNN
F 1 "GND" H 9055 8827 50  0000 C CNN
F 2 "" H 9050 9000 50  0001 C CNN
F 3 "" H 9050 9000 50  0001 C CNN
	1    9050 9000
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 8900 9050 9000
Wire Wire Line
	9150 8400 9050 8400
Wire Wire Line
	9050 8400 9050 8500
Wire Wire Line
	8200 8700 8350 8700
Wire Wire Line
	8650 8700 8750 8700
Wire Wire Line
	10000 8600 10150 8600
Wire Wire Line
	9700 8600 9600 8600
Wire Wire Line
	9600 8600 9600 8400
Wire Wire Line
	9600 8400 9550 8400
Text GLabel 14550 2750 2    50   Input ~ 0
5V
$Comp
L Regulator_Switching:TSR_1-2450 U2
U 1 1 5FB9637C
P 13950 2850
F 0 "U2" H 13950 3217 50  0000 C CNN
F 1 "TSR_1-2450" H 13950 3126 50  0000 C CNN
F 2 "Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT" H 13950 2700 50  0001 L CIN
F 3 "http://www.tracopower.com/products/tsr1.pdf" H 13950 2850 50  0001 C CNN
	1    13950 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	13050 1700 13050 2750
Wire Wire Line
	13050 2750 13550 2750
Wire Wire Line
	14350 2750 14550 2750
$Comp
L power:GND #PWR019
U 1 1 5FBB9989
P 13950 3200
F 0 "#PWR019" H 13950 2950 50  0001 C CNN
F 1 "GND" H 13955 3027 50  0000 C CNN
F 2 "" H 13950 3200 50  0001 C CNN
F 3 "" H 13950 3200 50  0001 C CNN
	1    13950 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	13950 3050 13950 3200
$Comp
L Device:D D1
U 1 1 5FBC7942
P 13250 1700
F 0 "D1" H 13250 1917 50  0000 C CNN
F 1 "D" H 13250 1826 50  0000 C CNN
F 2 "Diode_THT:D_5W_P12.70mm_Horizontal" H 13250 1700 50  0001 C CNN
F 3 "~" H 13250 1700 50  0001 C CNN
	1    13250 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	13100 1700 13050 1700
$Comp
L Mechanical:MountingHole H5
U 1 1 5FBCA80F
P 3050 8350
F 0 "H5" H 3150 8396 50  0000 L CNN
F 1 "Mount" H 3150 8305 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 3050 8350 50  0001 C CNN
F 3 "~" H 3050 8350 50  0001 C CNN
	1    3050 8350
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 5FBD4C52
P 1850 9100
F 0 "H3" H 1950 9146 50  0000 L CNN
F 1 "Mount" H 1950 9055 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 1850 9100 50  0001 C CNN
F 3 "~" H 1850 9100 50  0001 C CNN
	1    1850 9100
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 5FBD570D
P 1850 9750
F 0 "H4" H 1950 9796 50  0000 L CNN
F 1 "Mount" H 1950 9705 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 1850 9750 50  0001 C CNN
F 3 "~" H 1850 9750 50  0001 C CNN
	1    1850 9750
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H6
U 1 1 5FBD6094
P 3050 9100
F 0 "H6" H 3150 9146 50  0000 L CNN
F 1 "Mount" H 3150 9055 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5_Pad_Via" H 3050 9100 50  0001 C CNN
F 3 "~" H 3050 9100 50  0001 C CNN
	1    3050 9100
	1    0    0    -1  
$EndComp
Wire Wire Line
	15050 2350 13550 2350
Wire Wire Line
	13550 2350 13550 1700
Wire Wire Line
	13550 1700 13400 1700
Wire Wire Line
	14150 1250 14150 1750
Wire Wire Line
	14150 1750 14250 1750
Wire Wire Line
	14150 1250 14500 1250
$Comp
L AW_Misc_Library:SW_DPDT SW8
U 1 1 5FBAE622
P 14450 1750
F 0 "SW8" H 14450 2035 50  0000 C CNN
F 1 "SW_DPDT" H 14450 1944 50  0000 C CNN
F 2 "Aw_footprints:Switch DPDT Jaycar ST0365" H 14450 1750 50  0001 C CNN
F 3 "~" H 14450 1750 50  0001 C CNN
	1    14450 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	14150 1750 14150 2100
Wire Wire Line
	14150 2100 14250 2100
Connection ~ 14150 1750
Wire Wire Line
	14650 1650 15050 1650
Wire Wire Line
	15050 1650 15050 2000
Wire Wire Line
	14650 2000 15050 2000
Connection ~ 15050 2000
Wire Wire Line
	15050 2000 15050 2350
$Comp
L power:GND #PWR0103
U 1 1 5FBF9593
P 8050 1000
F 0 "#PWR0103" H 8050 750 50  0001 C CNN
F 1 "GND" H 8055 827 50  0000 C CNN
F 2 "" H 8050 1000 50  0001 C CNN
F 3 "" H 8050 1000 50  0001 C CNN
	1    8050 1000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5FC03997
P 8850 2500
F 0 "#PWR0104" H 8850 2250 50  0001 C CNN
F 1 "GND" H 8855 2327 50  0000 C CNN
F 2 "" H 8850 2500 50  0001 C CNN
F 3 "" H 8850 2500 50  0001 C CNN
	1    8850 2500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5FC297F8
P 8850 3950
F 0 "#PWR0105" H 8850 3700 50  0001 C CNN
F 1 "GND" H 8855 3777 50  0000 C CNN
F 2 "" H 8850 3950 50  0001 C CNN
F 3 "" H 8850 3950 50  0001 C CNN
	1    8850 3950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5FC29C2D
P 8850 5400
F 0 "#PWR0106" H 8850 5150 50  0001 C CNN
F 1 "GND" H 8855 5227 50  0000 C CNN
F 2 "" H 8850 5400 50  0001 C CNN
F 3 "" H 8850 5400 50  0001 C CNN
	1    8850 5400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5FC2A31E
P 8850 6850
F 0 "#PWR0107" H 8850 6600 50  0001 C CNN
F 1 "GND" H 8855 6677 50  0000 C CNN
F 2 "" H 8850 6850 50  0001 C CNN
F 3 "" H 8850 6850 50  0001 C CNN
	1    8850 6850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5FC2A6A4
P 8850 8300
F 0 "#PWR0108" H 8850 8050 50  0001 C CNN
F 1 "GND" H 8855 8127 50  0000 C CNN
F 2 "" H 8850 8300 50  0001 C CNN
F 3 "" H 8850 8300 50  0001 C CNN
	1    8850 8300
	1    0    0    -1  
$EndComp
NoConn ~ 14650 2200
NoConn ~ 14650 1850
NoConn ~ 17650 1150
$Comp
L Connector_Generic:Conn_01x04 J?
U 1 1 5FC1AD80
P 10650 1100
F 0 "J?" H 10730 1092 50  0000 L CNN
F 1 "Conn_01x04" H 10730 1001 50  0000 L CNN
F 2 "" H 10650 1100 50  0001 C CNN
F 3 "~" H 10650 1100 50  0001 C CNN
	1    10650 1100
	1    0    0    -1  
$EndComp
$EndSCHEMATC
