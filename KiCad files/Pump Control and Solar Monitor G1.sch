EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title "Pump Control and Solar Interface Module"
Date "2020-08-22"
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
Connection ~ 3050 4700
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
Wire Wire Line
	3450 4500 3450 4700
Wire Wire Line
	3450 4700 3350 4700
Connection ~ 3350 4700
Wire Wire Line
	3550 4500 3550 4700
Wire Wire Line
	3550 4700 3450 4700
Connection ~ 3450 4700
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
$Comp
L AW_Misc_Library:GY_SHT31-Breakout-pycom U6
U 1 1 5F432531
P 5900 1450
F 0 "U6" H 6228 1821 50  0000 L CNN
F 1 "GY_SHT31 Module" H 6228 1730 50  0000 L CNN
F 2 "Aw_footprints:GY_SHT31_Breakout" H 5950 1300 50  0001 C CNN
F 3 "" H 5950 1300 50  0001 C CNN
	1    5900 1450
	1    0    0    -1  
$EndComp
Text GLabel 3050 1550 0    50   Input ~ 0
5V
Text GLabel 3050 1400 0    50   Input ~ 0
3v3
Wire Wire Line
	3050 1550 3250 1550
Wire Wire Line
	3250 1550 3250 1900
Wire Wire Line
	3350 1900 3350 1550
Wire Wire Line
	3350 1550 3250 1550
Connection ~ 3250 1550
Wire Wire Line
	3050 1400 3550 1400
Wire Wire Line
	3550 1400 3550 1900
Wire Wire Line
	3650 1900 3650 1400
Wire Wire Line
	3650 1400 3550 1400
Connection ~ 3550 1400
Text GLabel 5650 1000 0    50   Input ~ 0
3v3
Wire Wire Line
	5650 1000 5850 1000
Text GLabel 5150 2600 2    50   Input ~ 0
SDA
Text GLabel 5150 2700 2    50   Input ~ 0
SCL
Wire Wire Line
	4250 2600 4700 2600
Wire Wire Line
	4250 2700 5000 2700
Text GLabel 5650 1300 0    50   Input ~ 0
SDA
Text GLabel 5650 1200 0    50   Input ~ 0
SCL
Wire Wire Line
	5650 1200 5850 1200
Wire Wire Line
	5650 1300 5850 1300
Text GLabel 4500 3300 2    50   Input ~ 0
SHUTDOWN
Text GLabel 13500 6650 0    50   Input ~ 0
SHUTDOWN
Wire Wire Line
	13500 6650 13600 6650
$Comp
L Connector_Generic:Conn_02x06_Odd_Even J3
U 1 1 5F43C9B9
P 14700 1100
F 0 "J3" H 14750 1517 50  0000 C CNN
F 1 "Switch Module Connector" H 14750 1426 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical" H 14700 1100 50  0001 C CNN
F 3 "~" H 14700 1100 50  0001 C CNN
	1    14700 1100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR029
U 1 1 5F43D5B1
P 14150 600
F 0 "#PWR029" H 14150 350 50  0001 C CNN
F 1 "GND" H 14155 427 50  0000 C CNN
F 2 "" H 14150 600 50  0001 C CNN
F 3 "" H 14150 600 50  0001 C CNN
	1    14150 600 
	1    0    0    -1  
$EndComp
Text GLabel 15150 1000 2    50   Input ~ 0
AC_Phase2_Present
NoConn ~ 14500 1400
NoConn ~ 15000 1300
Wire Wire Line
	14150 600  14300 600 
Wire Wire Line
	14300 600  14300 900 
Wire Wire Line
	14300 900  14500 900 
Wire Wire Line
	14200 1000 14500 1000
Wire Wire Line
	14200 1100 14500 1100
Wire Wire Line
	15000 1000 15150 1000
$Comp
L power:GND #PWR037
U 1 1 5F447C4B
P 15300 1400
F 0 "#PWR037" H 15300 1150 50  0001 C CNN
F 1 "GND" H 15305 1227 50  0000 C CNN
F 2 "" H 15300 1400 50  0001 C CNN
F 3 "" H 15300 1400 50  0001 C CNN
	1    15300 1400
	1    0    0    -1  
$EndComp
Wire Wire Line
	15000 1400 15300 1400
$Comp
L power:GND #PWR025
U 1 1 5F4488B8
P 14500 6650
F 0 "#PWR025" H 14500 6400 50  0001 C CNN
F 1 "GND" H 14505 6477 50  0000 C CNN
F 2 "" H 14500 6650 50  0001 C CNN
F 3 "" H 14500 6650 50  0001 C CNN
	1    14500 6650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR015
U 1 1 5F449619
P 5300 1100
F 0 "#PWR015" H 5300 850 50  0001 C CNN
F 1 "GND" H 5305 927 50  0000 C CNN
F 2 "" H 5300 1100 50  0001 C CNN
F 3 "" H 5300 1100 50  0001 C CNN
	1    5300 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 1100 5850 1100
$Comp
L power:GND #PWR05
U 1 1 5F44CF80
P 2650 4700
F 0 "#PWR05" H 2650 4450 50  0001 C CNN
F 1 "GND" H 2655 4527 50  0000 C CNN
F 2 "" H 2650 4700 50  0001 C CNN
F 3 "" H 2650 4700 50  0001 C CNN
	1    2650 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2650 4700 3050 4700
Text GLabel 14200 1300 0    50   Input ~ 0
PUMP_FAULT
Text GLabel 15150 1100 2    50   Input ~ 0
PUMP_RUNNING
Text GLabel 15150 1200 2    50   Input ~ 0
PUMP_STOP_RELAY
Wire Wire Line
	14200 1200 14500 1200
Wire Wire Line
	14200 1300 14500 1300
Wire Wire Line
	15000 1100 15150 1100
Wire Wire Line
	15000 1200 15150 1200
$Comp
L AW_Misc_Library:SDLA12TA_SLA_Charge_Module U4
U 1 1 5F45DED1
P 2250 8150
F 0 "U4" H 2250 8315 50  0000 C CNN
F 1 "SDLA12TA_SLA_Charge_Module" H 2250 8224 50  0000 C CNN
F 2 "Aw_footprints:SDLA12TA_Module" H 2250 8350 50  0001 C CNN
F 3 "" H 2250 8350 50  0001 C CNN
	1    2250 8150
	1    0    0    -1  
$EndComp
$Comp
L power:+15V #PWR01
U 1 1 5F45E5CB
P 1400 8150
F 0 "#PWR01" H 1400 8000 50  0001 C CNN
F 1 "+15V" H 1415 8323 50  0000 C CNN
F 2 "" H 1400 8150 50  0001 C CNN
F 3 "" H 1400 8150 50  0001 C CNN
	1    1400 8150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 5F45EA6E
P 1400 8400
F 0 "#PWR02" H 1400 8150 50  0001 C CNN
F 1 "GND" H 1405 8227 50  0000 C CNN
F 2 "" H 1400 8400 50  0001 C CNN
F 3 "" H 1400 8400 50  0001 C CNN
	1    1400 8400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 5F45F0B6
P 3000 8450
F 0 "#PWR06" H 3000 8200 50  0001 C CNN
F 1 "GND" H 3005 8277 50  0000 C CNN
F 2 "" H 3000 8450 50  0001 C CNN
F 3 "" H 3000 8450 50  0001 C CNN
	1    3000 8450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 8150 1400 8250
Wire Wire Line
	1400 8250 1850 8250
Wire Wire Line
	1400 8400 1400 8350
Wire Wire Line
	1400 8350 1850 8350
Wire Wire Line
	2650 8350 3000 8350
Wire Wire Line
	3000 8350 3000 8450
$Comp
L AW_Misc_Library:Polulu_D36V28F5_5V_Regulator U8
U 1 1 5F46807A
P 9750 10100
F 0 "U8" H 9750 10265 50  0000 C CNN
F 1 "Polulu D36V28F5 5V Regulator" H 9750 10174 50  0000 C CNN
F 2 "Aw_footprints:Polulu_D36V28F5_Regulator" H 9750 10100 50  0001 C CNN
F 3 "" H 9750 10100 50  0001 C CNN
	1    9750 10100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR016
U 1 1 5F4682BD
P 8750 10500
F 0 "#PWR016" H 8750 10250 50  0001 C CNN
F 1 "GND" H 8755 10327 50  0000 C CNN
F 2 "" H 8750 10500 50  0001 C CNN
F 3 "" H 8750 10500 50  0001 C CNN
	1    8750 10500
	1    0    0    -1  
$EndComp
Wire Wire Line
	8750 10200 8800 10200
Text GLabel 7950 10850 0    50   Input ~ 0
5V
$Comp
L Device:R_Small R1
U 1 1 5F41D3B5
P 3100 8250
F 0 "R1" V 2904 8250 50  0000 C CNN
F 1 "0.1R" V 2995 8250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" H 3100 8250 50  0001 C CNN
F 3 "~" H 3100 8250 50  0001 C CNN
	1    3100 8250
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R3
U 1 1 5F41F0F8
P 8650 10200
F 0 "R3" V 8454 10200 50  0000 C CNN
F 1 "0.1R" V 8545 10200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" H 8650 10200 50  0001 C CNN
F 3 "~" H 8650 10200 50  0001 C CNN
	1    8650 10200
	0    1    1    0   
$EndComp
Text GLabel 1650 10750 0    50   Input ~ 0
BATTERY+
$Comp
L Device:R_Small R12
U 1 1 5F42FD40
P 9400 9400
F 0 "R12" H 9341 9354 50  0000 R CNN
F 1 "10K" H 9341 9445 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 9400 9400 50  0001 C CNN
F 3 "~" H 9400 9400 50  0001 C CNN
	1    9400 9400
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Small R14
U 1 1 5F430034
P 9800 9400
F 0 "R14" H 9741 9354 50  0000 R CNN
F 1 "10K" H 9741 9445 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 9800 9400 50  0001 C CNN
F 3 "~" H 9800 9400 50  0001 C CNN
	1    9800 9400
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 9150 9400 9150
$Comp
L power:GND #PWR018
U 1 1 5F43BA8A
P 9400 9600
F 0 "#PWR018" H 9400 9350 50  0001 C CNN
F 1 "GND" H 9405 9427 50  0000 C CNN
F 2 "" H 9400 9600 50  0001 C CNN
F 3 "" H 9400 9600 50  0001 C CNN
	1    9400 9600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR020
U 1 1 5F43BEED
P 9800 9600
F 0 "#PWR020" H 9800 9350 50  0001 C CNN
F 1 "GND" H 9805 9427 50  0000 C CNN
F 2 "" H 9800 9600 50  0001 C CNN
F 3 "" H 9800 9600 50  0001 C CNN
	1    9800 9600
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 9500 9400 9600
Wire Wire Line
	9800 9500 9800 9600
Text GLabel 7400 9600 0    50   Input ~ 0
3v3
$Comp
L power:GND #PWR013
U 1 1 5F4442FC
P 7300 9250
F 0 "#PWR013" H 7300 9000 50  0001 C CNN
F 1 "GND" H 7305 9077 50  0000 C CNN
F 2 "" H 7300 9250 50  0001 C CNN
F 3 "" H 7300 9250 50  0001 C CNN
	1    7300 9250
	1    0    0    -1  
$EndComp
$Comp
L AW_Misc_Library:INA219AIDCNR U3
U 1 1 5F44A0B9
P 8400 8950
F 0 "U3" H 8400 9115 50  0000 C CNN
F 1 "INA219AIDCNR" H 8400 9024 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-8_Handsoldering" H 8400 8950 50  0001 C CNN
F 3 "" H 8400 8950 50  0001 C CNN
	1    8400 8950
	1    0    0    -1  
$EndComp
Wire Wire Line
	8700 9050 9800 9050
Wire Wire Line
	9400 9150 9400 9300
Wire Wire Line
	9800 9050 9800 9300
Connection ~ 9800 9050
Text GLabel 9700 8550 0    50   Input ~ 0
3v3
Text GLabel 8900 9350 2    50   Input ~ 0
SCL
Text GLabel 8900 9250 2    50   Input ~ 0
SDA
Wire Wire Line
	8700 9250 8900 9250
Wire Wire Line
	8700 9350 8900 9350
Wire Wire Line
	7300 9250 7550 9250
Wire Wire Line
	8100 9150 7950 9150
Wire Wire Line
	7950 9150 7950 9700
Wire Wire Line
	7950 9700 8800 9700
Wire Wire Line
	8800 9700 8800 10200
Wire Wire Line
	8100 9050 7900 9050
Wire Wire Line
	7900 9050 7900 9750
Wire Wire Line
	7900 9750 8450 9750
Wire Wire Line
	8450 9750 8450 10200
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
Wire Wire Line
	2650 8250 2900 8250
Wire Wire Line
	3200 8250 3250 8250
$Comp
L Device:R_Small R11
U 1 1 5F497A47
P 3850 7450
F 0 "R11" H 3791 7404 50  0000 R CNN
F 1 "10K" H 3791 7495 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 3850 7450 50  0001 C CNN
F 3 "~" H 3850 7450 50  0001 C CNN
	1    3850 7450
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Small R5
U 1 1 5F497A4D
P 4250 7450
F 0 "R5" H 4191 7404 50  0000 R CNN
F 1 "10K" H 4191 7495 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 4250 7450 50  0001 C CNN
F 3 "~" H 4250 7450 50  0001 C CNN
	1    4250 7450
	-1   0    0    1   
$EndComp
Wire Wire Line
	3150 7200 3850 7200
$Comp
L power:GND #PWR07
U 1 1 5F497A54
P 3850 7650
F 0 "#PWR07" H 3850 7400 50  0001 C CNN
F 1 "GND" H 3855 7477 50  0000 C CNN
F 2 "" H 3850 7650 50  0001 C CNN
F 3 "" H 3850 7650 50  0001 C CNN
	1    3850 7650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR09
U 1 1 5F497A5A
P 4250 7650
F 0 "#PWR09" H 4250 7400 50  0001 C CNN
F 1 "GND" H 4255 7477 50  0000 C CNN
F 2 "" H 4250 7650 50  0001 C CNN
F 3 "" H 4250 7650 50  0001 C CNN
	1    4250 7650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 7550 3850 7650
Wire Wire Line
	4250 7550 4250 7650
$Comp
L AW_Misc_Library:INA219AIDCNR U1
U 1 1 5F497A6A
P 2850 7000
F 0 "U1" H 2850 7165 50  0000 C CNN
F 1 "INA219AIDCNR" H 2850 7074 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-8_Handsoldering" H 2850 7000 50  0001 C CNN
F 3 "" H 2850 7000 50  0001 C CNN
	1    2850 7000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 7100 4250 7100
Wire Wire Line
	3850 7200 3850 7350
Wire Wire Line
	4250 7100 4250 7350
Text GLabel 3350 7400 2    50   Input ~ 0
SCL
Text GLabel 3350 7300 2    50   Input ~ 0
SDA
Wire Wire Line
	3150 7300 3350 7300
Wire Wire Line
	3150 7400 3350 7400
Wire Wire Line
	2550 7200 2400 7200
Wire Wire Line
	2400 7200 2400 7750
Wire Wire Line
	2400 7750 3250 7750
Wire Wire Line
	3250 7750 3250 8250
Wire Wire Line
	2550 7100 2350 7100
Wire Wire Line
	2350 7100 2350 7800
Wire Wire Line
	2350 7800 2900 7800
Wire Wire Line
	2900 7800 2900 8250
Connection ~ 2900 8250
Wire Wire Line
	2900 8250 3000 8250
Wire Wire Line
	8450 10200 8550 10200
Connection ~ 8800 10200
Wire Wire Line
	8800 10200 8800 10400
$Comp
L Device:R_Small R2
U 1 1 5F4D77AC
P 3050 10750
F 0 "R2" V 2854 10750 50  0000 C CNN
F 1 "0.1R" V 2945 10750 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" H 3050 10750 50  0001 C CNN
F 3 "~" H 3050 10750 50  0001 C CNN
	1    3050 10750
	0    1    1    0   
$EndComp
Wire Wire Line
	1650 10750 2900 10750
Wire Wire Line
	3150 10750 3250 10750
Wire Wire Line
	9700 8550 9800 8550
$Comp
L Device:C_Small C3
U 1 1 5F4FE5CB
P 7550 9400
F 0 "C3" H 7642 9446 50  0000 L CNN
F 1 "0.1uF" H 7642 9355 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 7550 9400 50  0001 C CNN
F 3 "~" H 7550 9400 50  0001 C CNN
	1    7550 9400
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 9600 7550 9600
Wire Wire Line
	8100 9600 8100 9350
Wire Wire Line
	7550 9500 7550 9600
Connection ~ 7550 9600
Wire Wire Line
	7550 9600 8100 9600
Wire Wire Line
	7550 9300 7550 9250
Connection ~ 7550 9250
Wire Wire Line
	7550 9250 8100 9250
Text GLabel 1850 7650 0    50   Input ~ 0
3v3
$Comp
L power:GND #PWR03
U 1 1 5F51E875
P 1750 7300
F 0 "#PWR03" H 1750 7050 50  0001 C CNN
F 1 "GND" H 1755 7127 50  0000 C CNN
F 2 "" H 1750 7300 50  0001 C CNN
F 3 "" H 1750 7300 50  0001 C CNN
	1    1750 7300
	1    0    0    -1  
$EndComp
Wire Wire Line
	1750 7300 2000 7300
$Comp
L Device:C_Small C1
U 1 1 5F51E87C
P 2000 7450
F 0 "C1" H 2092 7496 50  0000 L CNN
F 1 "0.1uF" H 2092 7405 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 2000 7450 50  0001 C CNN
F 3 "~" H 2000 7450 50  0001 C CNN
	1    2000 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 7650 2000 7650
Wire Wire Line
	2000 7550 2000 7650
Connection ~ 2000 7650
Wire Wire Line
	2000 7650 2550 7650
Wire Wire Line
	2000 7350 2000 7300
Connection ~ 2000 7300
Wire Wire Line
	2000 7300 2550 7300
Wire Wire Line
	2550 7400 2550 7650
$Comp
L Device:R_Small R4
U 1 1 5F560B1C
P 3850 9950
F 0 "R4" H 3791 9904 50  0000 R CNN
F 1 "10K" H 3791 9995 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 3850 9950 50  0001 C CNN
F 3 "~" H 3850 9950 50  0001 C CNN
	1    3850 9950
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Small R6
U 1 1 5F560B22
P 4250 9950
F 0 "R6" H 4191 9904 50  0000 R CNN
F 1 "10K" H 4191 9995 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 4250 9950 50  0001 C CNN
F 3 "~" H 4250 9950 50  0001 C CNN
	1    4250 9950
	-1   0    0    1   
$EndComp
Wire Wire Line
	3150 9700 3850 9700
$Comp
L power:GND #PWR08
U 1 1 5F560B29
P 3850 10150
F 0 "#PWR08" H 3850 9900 50  0001 C CNN
F 1 "GND" H 3855 9977 50  0000 C CNN
F 2 "" H 3850 10150 50  0001 C CNN
F 3 "" H 3850 10150 50  0001 C CNN
	1    3850 10150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR010
U 1 1 5F560B2F
P 4250 10150
F 0 "#PWR010" H 4250 9900 50  0001 C CNN
F 1 "GND" H 4255 9977 50  0000 C CNN
F 2 "" H 4250 10150 50  0001 C CNN
F 3 "" H 4250 10150 50  0001 C CNN
	1    4250 10150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 10050 3850 10150
Wire Wire Line
	4250 10050 4250 10150
Text GLabel 1850 10150 0    50   Input ~ 0
3v3
$Comp
L power:GND #PWR04
U 1 1 5F560B38
P 1750 9800
F 0 "#PWR04" H 1750 9550 50  0001 C CNN
F 1 "GND" H 1755 9627 50  0000 C CNN
F 2 "" H 1750 9800 50  0001 C CNN
F 3 "" H 1750 9800 50  0001 C CNN
	1    1750 9800
	1    0    0    -1  
$EndComp
$Comp
L AW_Misc_Library:INA219AIDCNR U2
U 1 1 5F560B3E
P 2850 9500
F 0 "U2" H 2850 9665 50  0000 C CNN
F 1 "INA219AIDCNR" H 2850 9574 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-8_Handsoldering" H 2850 9500 50  0001 C CNN
F 3 "" H 2850 9500 50  0001 C CNN
	1    2850 9500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 9600 4250 9600
Wire Wire Line
	3850 9700 3850 9850
Wire Wire Line
	4250 9600 4250 9850
Connection ~ 3850 9700
Text GLabel 3750 9100 0    50   Input ~ 0
3v3
Wire Wire Line
	3750 9100 3850 9100
Text GLabel 3350 9900 2    50   Input ~ 0
SCL
Text GLabel 3350 9800 2    50   Input ~ 0
SDA
Wire Wire Line
	3150 9800 3350 9800
Wire Wire Line
	3150 9900 3350 9900
Wire Wire Line
	1750 9800 2000 9800
Wire Wire Line
	2550 9700 2400 9700
Wire Wire Line
	2400 9700 2400 10250
Wire Wire Line
	2400 10250 3250 10250
Wire Wire Line
	3250 10250 3250 10750
Wire Wire Line
	2550 9600 2350 9600
Wire Wire Line
	2350 9600 2350 10300
Wire Wire Line
	2350 10300 2900 10300
Wire Wire Line
	2900 10300 2900 10750
$Comp
L Device:C_Small C2
U 1 1 5F560B6A
P 2000 9950
F 0 "C2" H 2092 9996 50  0000 L CNN
F 1 "0.1uF" H 2092 9905 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 2000 9950 50  0001 C CNN
F 3 "~" H 2000 9950 50  0001 C CNN
	1    2000 9950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 10150 2000 10150
Wire Wire Line
	2550 10150 2550 9900
Wire Wire Line
	2000 10050 2000 10150
Connection ~ 2000 10150
Wire Wire Line
	2000 10150 2550 10150
Wire Wire Line
	2000 9850 2000 9800
Connection ~ 2000 9800
Wire Wire Line
	2000 9800 2550 9800
Connection ~ 2900 10750
Wire Wire Line
	2900 10750 2950 10750
Connection ~ 3250 10750
Text Notes 2650 7650 0    50   ~ 0
Supply current monitor \nAddress 0x40
Text Notes 2650 10150 0    50   ~ 0
Battery Charge monitor \nAddress 0x41
Text Notes 8200 9600 0    50   ~ 0
Load current monitor\nAddress 0x44\nPin 7&8 solder bridged to set address 0x45
$Comp
L Device:LED D4
U 1 1 5F59F8A5
P 14400 7800
F 0 "D4" H 14393 7545 50  0000 C CNN
F 1 "15V Present" H 14393 7636 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 14400 7800 50  0001 C CNN
F 3 "~" H 14400 7800 50  0001 C CNN
	1    14400 7800
	-1   0    0    1   
$EndComp
$Comp
L power:+15V #PWR027
U 1 1 5F5C71FB
P 13400 7750
F 0 "#PWR027" H 13400 7600 50  0001 C CNN
F 1 "+15V" H 13415 7923 50  0000 C CNN
F 2 "" H 13400 7750 50  0001 C CNN
F 3 "" H 13400 7750 50  0001 C CNN
	1    13400 7750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R17
U 1 1 5F5C7B2C
P 13850 7800
F 0 "R17" V 13643 7800 50  0000 C CNN
F 1 "1K" V 13734 7800 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 13780 7800 50  0001 C CNN
F 3 "~" H 13850 7800 50  0001 C CNN
	1    13850 7800
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR034
U 1 1 5F5DC43F
P 14850 7850
F 0 "#PWR034" H 14850 7600 50  0001 C CNN
F 1 "GND" H 14855 7677 50  0000 C CNN
F 2 "" H 14850 7850 50  0001 C CNN
F 3 "" H 14850 7850 50  0001 C CNN
	1    14850 7850
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D5
U 1 1 5F5FB393
P 14400 8350
F 0 "D5" H 14393 8095 50  0000 C CNN
F 1 "5V Present" H 14393 8186 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 14400 8350 50  0001 C CNN
F 3 "~" H 14400 8350 50  0001 C CNN
	1    14400 8350
	-1   0    0    1   
$EndComp
$Comp
L Device:R R18
U 1 1 5F5FB3A7
P 13850 8350
F 0 "R18" V 13643 8350 50  0000 C CNN
F 1 "220R" V 13734 8350 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 13780 8350 50  0001 C CNN
F 3 "~" H 13850 8350 50  0001 C CNN
	1    13850 8350
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR035
U 1 1 5F5FB3B1
P 14850 8400
F 0 "#PWR035" H 14850 8150 50  0001 C CNN
F 1 "GND" H 14855 8227 50  0000 C CNN
F 2 "" H 14850 8400 50  0001 C CNN
F 3 "" H 14850 8400 50  0001 C CNN
	1    14850 8400
	1    0    0    -1  
$EndComp
Text GLabel 13550 8350 0    50   Input ~ 0
5V
Wire Wire Line
	3250 8250 5050 8250
Wire Wire Line
	3250 10750 5050 10750
Connection ~ 3250 8250
Text GLabel 5850 9150 2    50   Input ~ 0
BATTERY_SUPPLY
Text GLabel 7750 10200 0    50   Input ~ 0
BATTERY_SUPPLY
Wire Wire Line
	7750 10200 8450 10200
Connection ~ 8450 10200
Text GLabel 13550 9000 0    50   Input ~ 0
BATTERY_SUPPLY
$Comp
L Device:LED D6
U 1 1 5F67C7DF
P 14400 9000
F 0 "D6" H 14393 8745 50  0000 C CNN
F 1 "BATTERY Present" H 14393 8836 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 14400 9000 50  0001 C CNN
F 3 "~" H 14400 9000 50  0001 C CNN
	1    14400 9000
	-1   0    0    1   
$EndComp
$Comp
L Device:R R19
U 1 1 5F67C7E9
P 13850 9000
F 0 "R19" V 13643 9000 50  0000 C CNN
F 1 "820R" V 13734 9000 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 13780 9000 50  0001 C CNN
F 3 "~" H 13850 9000 50  0001 C CNN
	1    13850 9000
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR036
U 1 1 5F67C7F3
P 14850 9050
F 0 "#PWR036" H 14850 8800 50  0001 C CNN
F 1 "GND" H 14855 8877 50  0000 C CNN
F 2 "" H 14850 9050 50  0001 C CNN
F 3 "" H 14850 9050 50  0001 C CNN
	1    14850 9050
	1    0    0    -1  
$EndComp
Wire Wire Line
	14850 9000 14850 9050
Wire Wire Line
	3850 9100 3850 9700
Wire Wire Line
	9800 8550 9800 9050
$Comp
L Connector_Generic:Conn_01x04 J6
U 1 1 5F6CA540
P 14800 2800
F 0 "J6" H 14880 2792 50  0000 L CNN
F 1 "LED Module Connector" H 14880 2701 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 14800 2800 50  0001 C CNN
F 3 "~" H 14800 2800 50  0001 C CNN
	1    14800 2800
	1    0    0    -1  
$EndComp
Text Notes 14350 3200 0    50   ~ 0
I2C Connection to External \nI2C LED Status Bar
$Comp
L power:GND #PWR032
U 1 1 5F6D441A
P 14350 2550
F 0 "#PWR032" H 14350 2300 50  0001 C CNN
F 1 "GND" H 14355 2377 50  0000 C CNN
F 2 "" H 14350 2550 50  0001 C CNN
F 3 "" H 14350 2550 50  0001 C CNN
	1    14350 2550
	1    0    0    -1  
$EndComp
Text GLabel 14150 2800 0    50   Input ~ 0
SCL
Text GLabel 14150 2900 0    50   Input ~ 0
SDA
$Comp
L Regulator_Switching:TSR_1-2433 U7
U 1 1 5F6D547E
P 2800 5950
F 0 "U7" H 2800 6317 50  0000 C CNN
F 1 "TSR_1-2433" H 2800 6226 50  0000 C CNN
F 2 "Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT" H 2800 5800 50  0001 L CIN
F 3 "http://www.tracopower.com/products/tsr1.pdf" H 2800 5950 50  0001 C CNN
	1    2800 5950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR017
U 1 1 5F6D59DC
P 2800 6300
F 0 "#PWR017" H 2800 6050 50  0001 C CNN
F 1 "GND" H 2805 6127 50  0000 C CNN
F 2 "" H 2800 6300 50  0001 C CNN
F 3 "" H 2800 6300 50  0001 C CNN
	1    2800 6300
	1    0    0    -1  
$EndComp
Text GLabel 2150 5850 0    50   Input ~ 0
BATTERY_SUPPLY
$Comp
L power:+3.3VA #PWR021
U 1 1 5F6D6209
P 3850 5600
F 0 "#PWR021" H 3850 5450 50  0001 C CNN
F 1 "+3.3VA" H 3865 5773 50  0000 C CNN
F 2 "" H 3850 5600 50  0001 C CNN
F 3 "" H 3850 5600 50  0001 C CNN
	1    3850 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 6150 2800 6300
Wire Wire Line
	2150 5850 2400 5850
Text Notes 2400 6150 0    50   ~ 0
Auxiliary 3.3V supply
$Comp
L power:+3.3VA #PWR028
U 1 1 5F6F4B17
P 14050 3200
F 0 "#PWR028" H 14050 3050 50  0001 C CNN
F 1 "+3.3VA" H 14065 3373 50  0000 C CNN
F 2 "" H 14050 3200 50  0001 C CNN
F 3 "" H 14050 3200 50  0001 C CNN
	1    14050 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	14600 2800 14150 2800
Wire Wire Line
	14150 2900 14600 2900
Wire Wire Line
	14050 3200 14050 3300
Wire Wire Line
	14400 3300 14400 3000
Wire Wire Line
	14400 3000 14600 3000
Wire Wire Line
	14050 3300 14400 3300
Text GLabel 14450 5450 0    50   Input ~ 0
FRONIUS_GND
Text GLabel 14450 5650 0    50   Input ~ 0
FRONIUS_RAW_1
Text Notes 14300 6100 0    50   ~ 0
Froinuis Digital IO
Text GLabel 4500 3400 2    50   Input ~ 0
FRONIUS_1
Text GLabel 2450 2600 0    50   Input ~ 0
AC_Phase1_Present
Text GLabel 2450 2800 0    50   Input ~ 0
AC_Phase3_Present
Text GLabel 2450 2700 0    50   Input ~ 0
AC_Phase2_Present
Text GLabel 2450 3400 0    50   Input ~ 0
PUMP_START_PULSE
Text GLabel 2450 3700 0    50   Input ~ 0
PUMP_FAULT
Text GLabel 2450 3500 0    50   Input ~ 0
PUMP_STOP_PULSE
Text GLabel 2450 3600 0    50   Input ~ 0
PUMP_RUNNING
Wire Wire Line
	2650 2600 2450 2600
Wire Wire Line
	2450 2700 2650 2700
Wire Wire Line
	2650 2800 2450 2800
Wire Wire Line
	2450 3400 2650 3400
Wire Wire Line
	2450 3700 2650 3700
$Comp
L Connector_Generic:Conn_01x03 J8
U 1 1 5F60522F
P 14950 4100
F 0 "J8" H 15030 4142 50  0000 L CNN
F 1 "Tamper Switch Connector" H 15030 4051 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 14950 4100 50  0001 C CNN
F 3 "~" H 14950 4100 50  0001 C CNN
	1    14950 4100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR033
U 1 1 5F605AA7
P 14600 3750
F 0 "#PWR033" H 14600 3500 50  0001 C CNN
F 1 "GND" H 14605 3577 50  0000 C CNN
F 2 "" H 14600 3750 50  0001 C CNN
F 3 "" H 14600 3750 50  0001 C CNN
	1    14600 3750
	1    0    0    -1  
$EndComp
Text GLabel 4500 2900 2    50   Input ~ 0
TAMPER
Wire Wire Line
	4250 2900 4500 2900
Wire Wire Line
	14600 3750 14700 3750
Wire Wire Line
	14700 3750 14700 4000
Wire Wire Line
	14700 4000 14750 4000
Wire Wire Line
	4250 3300 4500 3300
Wire Wire Line
	4250 3400 4500 3400
Wire Wire Line
	2450 3500 2650 3500
Wire Wire Line
	2650 3600 2450 3600
$Comp
L Transistor_FET:BS170 Q1
U 1 1 5F7B275A
P 7200 6900
F 0 "Q1" H 7404 6946 50  0000 L CNN
F 1 "BS170" H 7404 6855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 7400 6825 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/BS/BS170.pdf" H 7200 6900 50  0001 L CNN
	1    7200 6900
	1    0    0    -1  
$EndComp
Text GLabel 6800 6900 0    50   Input ~ 0
PUMP_START_PULSE
$Comp
L power:GND #PWR012
U 1 1 5F7C35A4
P 6900 7450
F 0 "#PWR012" H 6900 7200 50  0001 C CNN
F 1 "GND" H 6905 7277 50  0000 C CNN
F 2 "" H 6900 7450 50  0001 C CNN
F 3 "" H 6900 7450 50  0001 C CNN
	1    6900 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 6900 6900 6900
Wire Wire Line
	6900 7000 6900 6900
Connection ~ 6900 6900
Wire Wire Line
	6900 6900 7000 6900
Wire Wire Line
	6900 7300 6900 7450
$Comp
L power:GND #PWR014
U 1 1 5F7F01B8
P 7300 7450
F 0 "#PWR014" H 7300 7200 50  0001 C CNN
F 1 "GND" H 7305 7277 50  0000 C CNN
F 2 "" H 7300 7450 50  0001 C CNN
F 3 "" H 7300 7450 50  0001 C CNN
	1    7300 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	7300 7100 7300 7450
Text GLabel 7900 6400 2    50   Input ~ 0
PUMP_START_RELAY
Wire Wire Line
	7300 6700 7300 6400
Wire Wire Line
	7300 6400 7600 6400
Wire Wire Line
	7600 6450 7600 6400
Connection ~ 7600 6400
Wire Wire Line
	7600 6400 7900 6400
$Comp
L Device:Fuse F1
U 1 1 5F8F7CD4
P 5450 9150
F 0 "F1" V 5253 9150 50  0000 C CNN
F 1 "Fuse 5 AMP" V 5344 9150 50  0000 C CNN
F 2 "Aw_footprints:Wuth Electronik PCB TTH Fuse Holder" V 5380 9150 50  0001 C CNN
F 3 "~" H 5450 9150 50  0001 C CNN
	1    5450 9150
	0    1    1    0   
$EndComp
Wire Wire Line
	5600 9150 5850 9150
Wire Wire Line
	5300 9150 5050 9150
Wire Wire Line
	5050 8250 5050 9150
Connection ~ 5050 9150
Wire Wire Line
	5050 9150 5050 10750
$Comp
L Device:D D1
U 1 1 5F82C9A0
P 7600 6600
F 0 "D1" V 7550 6500 50  0000 C CNN
F 1 "FLYBACK DIODE" V 7650 6250 50  0000 C CNN
F 2 "Diode_THT:D_5W_P12.70mm_Horizontal" H 7600 6600 50  0001 C CNN
F 3 "~" H 7600 6600 50  0001 C CNN
	1    7600 6600
	0    -1   -1   0   
$EndComp
$Comp
L Transistor_FET:BS170 Q2
U 1 1 5F92BDEC
P 10300 6900
F 0 "Q2" H 10504 6946 50  0000 L CNN
F 1 "BS170" H 10504 6855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 10500 6825 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/BS/BS170.pdf" H 10300 6900 50  0001 L CNN
	1    10300 6900
	1    0    0    -1  
$EndComp
Text GLabel 9900 6900 0    50   Input ~ 0
PUMP_STOP_PULSE
$Comp
L Device:R R15
U 1 1 5F92BDF7
P 10000 7200
F 0 "R15" H 10150 7250 50  0000 C CNN
F 1 "10K" H 10150 7150 50  0000 C CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 9930 7200 50  0001 C CNN
F 3 "~" H 10000 7200 50  0001 C CNN
	1    10000 7200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR022
U 1 1 5F92BE01
P 10000 7450
F 0 "#PWR022" H 10000 7200 50  0001 C CNN
F 1 "GND" H 10005 7277 50  0000 C CNN
F 2 "" H 10000 7450 50  0001 C CNN
F 3 "" H 10000 7450 50  0001 C CNN
	1    10000 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	9900 6900 10000 6900
Wire Wire Line
	10000 7050 10000 6900
Connection ~ 10000 6900
Wire Wire Line
	10000 6900 10100 6900
Wire Wire Line
	10000 7350 10000 7450
$Comp
L power:GND #PWR024
U 1 1 5F92BE10
P 10400 7450
F 0 "#PWR024" H 10400 7200 50  0001 C CNN
F 1 "GND" H 10405 7277 50  0000 C CNN
F 2 "" H 10400 7450 50  0001 C CNN
F 3 "" H 10400 7450 50  0001 C CNN
	1    10400 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	10400 7100 10400 7450
Text GLabel 11000 6400 2    50   Input ~ 0
PUMP_STOP_RELAY
Wire Wire Line
	10400 6700 10400 6400
Wire Wire Line
	10400 6400 10700 6400
Wire Wire Line
	10700 6450 10700 6400
Connection ~ 10700 6400
Wire Wire Line
	10700 6400 11000 6400
$Comp
L Device:D D2
U 1 1 5F92BE23
P 10700 6600
F 0 "D2" V 10650 6500 50  0000 C CNN
F 1 "FLYBACK DIODE" V 10750 6250 50  0000 C CNN
F 2 "Diode_THT:D_5W_P12.70mm_Horizontal" H 10700 6600 50  0001 C CNN
F 3 "~" H 10700 6600 50  0001 C CNN
	1    10700 6600
	0    -1   -1   0   
$EndComp
Text Notes 13550 7200 0    50   ~ 0
System Shutdown PB
Text Notes 2400 5100 0    50   ~ 0
Connection to Raspberry Pi 40 Pin Header
NoConn ~ 4250 2300
NoConn ~ 4250 2400
NoConn ~ 4250 3000
NoConn ~ 4250 3100
NoConn ~ 4250 3900
NoConn ~ 4250 4000
NoConn ~ 2650 3900
NoConn ~ 2650 3800
NoConn ~ 2650 3200
NoConn ~ 2650 3100
NoConn ~ 2650 3000
NoConn ~ 14750 4200
Text Notes 1750 1600 0    50   ~ 0
Pi is powered via this 5V line
Text Notes 5500 1550 0    50   ~ 0
SHT31 Temp Humidity Module\nI2C address 0x44
Text Notes 5950 7950 0    79   ~ 0
Relay control MOSFETS
Text GLabel 4500 3500 2    50   Input ~ 0
FRONIUS_2
Text GLabel 4500 3600 2    50   Input ~ 0
FRONIUS_3
Text GLabel 4500 3700 2    50   Input ~ 0
FRONIUS_4
Wire Wire Line
	4250 3500 4500 3500
Wire Wire Line
	4500 3600 4250 3600
Wire Wire Line
	4250 3700 4500 3700
$Comp
L Device:LED D7
U 1 1 5F691742
P 4600 5850
F 0 "D7" H 4593 5595 50  0000 C CNN
F 1 "3v3AUX Present" H 4593 5686 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 4600 5850 50  0001 C CNN
F 3 "~" H 4600 5850 50  0001 C CNN
	1    4600 5850
	-1   0    0    1   
$EndComp
$Comp
L Device:R R20
U 1 1 5F691756
P 4100 5850
F 0 "R20" V 3893 5850 50  0000 C CNN
F 1 "1K" V 3984 5850 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4030 5850 50  0001 C CNN
F 3 "~" H 4100 5850 50  0001 C CNN
	1    4100 5850
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR038
U 1 1 5F691760
P 4850 5950
F 0 "#PWR038" H 4850 5700 50  0001 C CNN
F 1 "GND" H 4855 5777 50  0000 C CNN
F 2 "" H 4850 5950 50  0001 C CNN
F 3 "" H 4850 5950 50  0001 C CNN
	1    4850 5950
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 5600 3850 5850
Text GLabel 14450 5750 0    50   Input ~ 0
FRONIUS_RAW_2
Text GLabel 14450 5850 0    50   Input ~ 0
FRONIUS_RAW_3
Text GLabel 14450 5950 0    50   Input ~ 0
FRONIUS_RAW_4
Wire Wire Line
	14350 2450 14350 2550
Wire Wire Line
	14600 2450 14350 2450
Wire Wire Line
	14600 2700 14600 2450
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5F450BB3
P 14800 2000
F 0 "J2" H 14880 2042 50  0000 L CNN
F 1 "Serial Console Connector" H 14880 1951 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 14800 2000 50  0001 C CNN
F 3 "~" H 14800 2000 50  0001 C CNN
	1    14800 2000
	1    0    0    -1  
$EndComp
Text GLabel 14300 2000 0    50   Input ~ 0
TXD
Text GLabel 14300 2100 0    50   Input ~ 0
RXD
Wire Wire Line
	14300 2000 14600 2000
Wire Wire Line
	14300 2100 14600 2100
$Comp
L power:GND #PWR011
U 1 1 5F44B884
P 13950 1900
F 0 "#PWR011" H 13950 1650 50  0001 C CNN
F 1 "GND" H 13955 1727 50  0000 C CNN
F 2 "" H 13950 1900 50  0001 C CNN
F 3 "" H 13950 1900 50  0001 C CNN
	1    13950 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	13950 1900 14600 1900
Wire Wire Line
	14150 4100 14750 4100
Connection ~ 14150 4100
Wire Wire Line
	14150 4050 14150 4100
Wire Wire Line
	13850 4100 14150 4100
Wire Wire Line
	14150 3700 14150 3750
Wire Wire Line
	13950 3700 14150 3700
Text GLabel 13950 3700 0    50   Input ~ 0
3v3
Text GLabel 13850 4100 0    50   Input ~ 0
TAMPER
Text Notes 14100 4550 0    50   ~ 0
Tamper switch is normally closed\n1=NC\n2=Common\n3=NO
Wire Notes Line
	13300 650  11000 650 
Wire Notes Line
	13300 5600 13300 650 
Wire Notes Line
	11000 5600 13300 5600
Wire Notes Line
	11000 650  11000 5600
Wire Wire Line
	11150 1950 11150 1900
Wire Wire Line
	11400 1950 11150 1950
Wire Wire Line
	12250 1950 11850 1950
$Comp
L Device:D D3
U 1 1 5F7350D0
P 11550 1950
F 0 "D3" H 11550 2167 50  0000 C CNN
F 1 "Polarity Protection" H 11550 2076 50  0000 C CNN
F 2 "Diode_THT:D_5W_P12.70mm_Horizontal" H 11550 1950 50  0001 C CNN
F 3 "~" H 11550 1950 50  0001 C CNN
	1    11550 1950
	1    0    0    -1  
$EndComp
Text Notes 11550 2200 0    50   ~ 0
Connection to External 15VDC Power Supply \nwith Polarity Protection
$Comp
L power:+15V #PWR026
U 1 1 5F457F85
P 11150 1900
F 0 "#PWR026" H 11150 1750 50  0001 C CNN
F 1 "+15V" H 11165 2073 50  0000 C CNN
F 2 "" H 11150 1900 50  0001 C CNN
F 3 "" H 11150 1900 50  0001 C CNN
	1    11150 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	12000 1850 12250 1850
Wire Wire Line
	12000 1500 12000 1850
Wire Wire Line
	12150 1500 12000 1500
$Comp
L power:GND #PWR031
U 1 1 5F456BF8
P 12150 1500
F 0 "#PWR031" H 12150 1250 50  0001 C CNN
F 1 "GND" H 12155 1327 50  0000 C CNN
F 2 "" H 12150 1500 50  0001 C CNN
F 3 "" H 12150 1500 50  0001 C CNN
	1    12150 1500
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J5
U 1 1 5F456797
P 12450 1850
F 0 "J5" H 12350 2100 50  0000 L CNN
F 1 "DC Power Supply Conector" H 12250 2000 50  0000 L CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 12450 1850 50  0001 C CNN
F 3 "~" H 12450 1850 50  0001 C CNN
	1    12450 1850
	1    0    0    -1  
$EndComp
NoConn ~ 12750 1850
NoConn ~ 12750 1950
NoConn ~ 12200 3900
NoConn ~ 11700 3900
NoConn ~ 11700 2950
NoConn ~ 12200 2850
Wire Wire Line
	12200 2950 12550 2950
Wire Wire Line
	11700 3800 11450 3800
Text Notes 11500 4100 0    50   ~ 0
Power supply to Netgear Switch
$Comp
L power:GND #PWR0101
U 1 1 5F526A6F
P 11450 3800
F 0 "#PWR0101" H 11450 3550 50  0001 C CNN
F 1 "GND" H 11455 3627 50  0000 C CNN
F 2 "" H 11450 3800 50  0001 C CNN
F 3 "" H 11450 3800 50  0001 C CNN
	1    11450 3800
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J9
U 1 1 5F52656D
P 11900 3800
F 0 "J9" H 11957 4125 50  0000 C CNN
F 1 "Netgear Power" H 11957 4034 50  0000 C CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 11950 3760 50  0001 C CNN
F 3 "~" H 11950 3760 50  0001 C CNN
	1    11900 3800
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J4
U 1 1 5F45363F
P 11900 2850
F 0 "J4" H 11850 3100 50  0000 L CNN
F 1 "Battery Connector" H 11750 3000 50  0000 L CNN
F 2 "Connector_Molex:Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical" H 11900 2850 50  0001 C CNN
F 3 "~" H 11900 2850 50  0001 C CNN
	1    11900 2850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR030
U 1 1 5F454149
P 11500 2650
F 0 "#PWR030" H 11500 2400 50  0001 C CNN
F 1 "GND" H 11505 2477 50  0000 C CNN
F 2 "" H 11500 2650 50  0001 C CNN
F 3 "" H 11500 2650 50  0001 C CNN
	1    11500 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	11500 2650 11650 2650
Wire Wire Line
	11650 2650 11650 2850
Wire Wire Line
	11650 2850 11700 2850
Text GLabel 12700 2950 2    50   Input ~ 0
BATTERY+
Text Notes 11600 3200 0    50   ~ 0
Connection to External \n12V SLA Battery
Connection ~ 8450 2700
Wire Wire Line
	8650 2700 8650 2600
Wire Wire Line
	8450 2700 8650 2700
Connection ~ 8500 4000
Wire Wire Line
	8700 4000 8700 3900
Wire Wire Line
	8500 4000 8700 4000
Connection ~ 8500 5100
Wire Wire Line
	8700 5100 8700 5000
Wire Wire Line
	8500 5100 8700 5100
Wire Wire Line
	8500 4800 8700 4800
Connection ~ 8500 4800
$Comp
L Device:LED D11
U 1 1 5F81CC16
P 8500 4950
F 0 "D11" V 8539 5030 50  0000 L CNN
F 1 "Fron4" V 8448 5030 50  0000 L CNN
F 2 "LED_THT:LED_D5.0mm" H 8500 4950 50  0001 C CNN
F 3 "~" H 8500 4950 50  0001 C CNN
	1    8500 4950
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8500 3700 8700 3700
Connection ~ 8500 3700
$Comp
L Device:LED D10
U 1 1 5F81C58F
P 8500 3850
F 0 "D10" V 8539 3930 50  0000 L CNN
F 1 "Fron3" V 8448 3930 50  0000 L CNN
F 2 "LED_THT:LED_D5.0mm" H 8500 3850 50  0001 C CNN
F 3 "~" H 8500 3850 50  0001 C CNN
	1    8500 3850
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8450 2400 8650 2400
Connection ~ 8450 2400
$Comp
L Device:LED D9
U 1 1 5F81A5EC
P 8450 2550
F 0 "D9" V 8489 2630 50  0000 L CNN
F 1 "Fron2" V 8398 2630 50  0000 L CNN
F 2 "LED_THT:LED_D5.0mm" H 8450 2550 50  0001 C CNN
F 3 "~" H 8450 2550 50  0001 C CNN
	1    8450 2550
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED D8
U 1 1 5F63316B
P 8450 1450
F 0 "D8" V 8489 1530 50  0000 L CNN
F 1 "Fron1" V 8398 1530 50  0000 L CNN
F 2 "LED_THT:LED_D5.0mm" H 8450 1450 50  0001 C CNN
F 3 "~" H 8450 1450 50  0001 C CNN
	1    8450 1450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8300 1300 8450 1300
Wire Wire Line
	8450 1300 8650 1300
Wire Wire Line
	8450 1600 7950 1600
Wire Wire Line
	8450 1600 8650 1600
Connection ~ 8450 1300
Connection ~ 8450 1600
Wire Wire Line
	8650 1600 8650 1500
Wire Notes Line
	10750 650  7200 650 
Wire Notes Line
	10750 5600 10750 650 
Wire Notes Line
	7200 5600 10750 5600
Wire Notes Line
	7200 650  7200 5600
Wire Wire Line
	9600 4300 9600 4400
Wire Wire Line
	9450 4300 9600 4300
Text GLabel 9450 4300 0    50   Input ~ 0
3v3
Wire Wire Line
	9600 5000 9600 5050
Wire Wire Line
	9300 5000 9600 5000
Connection ~ 9600 4800
Wire Wire Line
	9600 4800 10000 4800
Wire Wire Line
	9600 4800 9600 4700
Wire Wire Line
	9300 4800 9600 4800
Text GLabel 10000 4800 2    50   Input ~ 0
FRONIUS_4
$Comp
L power:GND #PWR041
U 1 1 5F634988
P 9600 5050
F 0 "#PWR041" H 9600 4800 50  0001 C CNN
F 1 "GND" H 9605 4877 50  0000 C CNN
F 2 "" H 9600 5050 50  0001 C CNN
F 3 "" H 9600 5050 50  0001 C CNN
	1    9600 5050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R26
U 1 1 5F63497E
P 9600 4550
F 0 "R26" H 9530 4504 50  0000 R CNN
F 1 "10K" H 9530 4595 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 9530 4550 50  0001 C CNN
F 3 "~" H 9600 4550 50  0001 C CNN
	1    9600 4550
	-1   0    0    1   
$EndComp
Text Notes 7250 5550 0    79   ~ 0
Opto Isolator for Fronuis Digital IO
Wire Wire Line
	8500 5100 8000 5100
Wire Wire Line
	8350 4800 8500 4800
Wire Wire Line
	8000 4800 8050 4800
$Comp
L Device:R R23
U 1 1 5F634970
P 8200 4800
F 0 "R23" V 7993 4800 50  0000 C CNN
F 1 "540R" V 8084 4800 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8130 4800 50  0001 C CNN
F 3 "~" H 8200 4800 50  0001 C CNN
	1    8200 4800
	0    1    1    0   
$EndComp
Text GLabel 8000 4800 0    50   Input ~ 0
FRONIUS_RAW_4
Text GLabel 8000 5100 0    50   Input ~ 0
FRONIUS_GND
$Comp
L Isolator:PC817 U11
U 1 1 5F634964
P 9000 4900
F 0 "U11" H 9000 5225 50  0000 C CNN
F 1 "PC817" H 9000 5134 50  0000 C CNN
F 2 "Package_DIP:DIP-4_W7.62mm" H 8800 4700 50  0001 L CIN
F 3 "http://www.soselectronic.cz/a_info/resource/d/pc817.pdf" H 9000 4900 50  0001 L CNN
	1    9000 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	9600 3200 9600 3300
Wire Wire Line
	9450 3200 9600 3200
Text GLabel 9450 3200 0    50   Input ~ 0
3v3
Wire Wire Line
	9600 3900 9600 3950
Wire Wire Line
	9300 3900 9600 3900
Connection ~ 9600 3700
Wire Wire Line
	9600 3700 10000 3700
Wire Wire Line
	9600 3700 9600 3600
Wire Wire Line
	9300 3700 9600 3700
Text GLabel 10000 3700 2    50   Input ~ 0
FRONIUS_3
$Comp
L power:GND #PWR040
U 1 1 5F634950
P 9600 3950
F 0 "#PWR040" H 9600 3700 50  0001 C CNN
F 1 "GND" H 9605 3777 50  0000 C CNN
F 2 "" H 9600 3950 50  0001 C CNN
F 3 "" H 9600 3950 50  0001 C CNN
	1    9600 3950
	1    0    0    -1  
$EndComp
$Comp
L Device:R R25
U 1 1 5F634946
P 9600 3450
F 0 "R25" H 9530 3404 50  0000 R CNN
F 1 "10K" H 9530 3495 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 9530 3450 50  0001 C CNN
F 3 "~" H 9600 3450 50  0001 C CNN
	1    9600 3450
	-1   0    0    1   
$EndComp
Wire Wire Line
	8500 4000 8000 4000
Wire Wire Line
	8350 3700 8500 3700
Wire Wire Line
	8000 3700 8050 3700
$Comp
L Device:R R22
U 1 1 5F634938
P 8200 3700
F 0 "R22" V 7993 3700 50  0000 C CNN
F 1 "540R" V 8084 3700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8130 3700 50  0001 C CNN
F 3 "~" H 8200 3700 50  0001 C CNN
	1    8200 3700
	0    1    1    0   
$EndComp
Text GLabel 8000 3700 0    50   Input ~ 0
FRONIUS_RAW_3
Text GLabel 8000 4000 0    50   Input ~ 0
FRONIUS_GND
$Comp
L Isolator:PC817 U10
U 1 1 5F63492C
P 9000 3800
F 0 "U10" H 9000 4125 50  0000 C CNN
F 1 "PC817" H 9000 4034 50  0000 C CNN
F 2 "Package_DIP:DIP-4_W7.62mm" H 8800 3600 50  0001 L CIN
F 3 "http://www.soselectronic.cz/a_info/resource/d/pc817.pdf" H 9000 3800 50  0001 L CNN
	1    9000 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	9550 1900 9550 2000
Wire Wire Line
	9500 1900 9550 1900
Text GLabel 9500 1900 0    50   Input ~ 0
3v3
Wire Wire Line
	9550 2600 9550 2650
Wire Wire Line
	9250 2600 9550 2600
Connection ~ 9550 2400
Wire Wire Line
	9550 2400 9950 2400
Wire Wire Line
	9550 2400 9550 2300
Wire Wire Line
	9250 2400 9550 2400
Text GLabel 9950 2400 2    50   Input ~ 0
FRONIUS_2
$Comp
L power:GND #PWR039
U 1 1 5F526032
P 9550 2650
F 0 "#PWR039" H 9550 2400 50  0001 C CNN
F 1 "GND" H 9555 2477 50  0000 C CNN
F 2 "" H 9550 2650 50  0001 C CNN
F 3 "" H 9550 2650 50  0001 C CNN
	1    9550 2650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R24
U 1 1 5F526028
P 9550 2150
F 0 "R24" H 9480 2104 50  0000 R CNN
F 1 "10K" H 9480 2195 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 9480 2150 50  0001 C CNN
F 3 "~" H 9550 2150 50  0001 C CNN
	1    9550 2150
	-1   0    0    1   
$EndComp
Wire Wire Line
	8450 2700 7950 2700
Wire Wire Line
	8300 2400 8450 2400
Wire Wire Line
	7950 2400 8000 2400
$Comp
L Device:R R21
U 1 1 5F52601A
P 8150 2400
F 0 "R21" V 7943 2400 50  0000 C CNN
F 1 "540R" V 8034 2400 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8080 2400 50  0001 C CNN
F 3 "~" H 8150 2400 50  0001 C CNN
	1    8150 2400
	0    1    1    0   
$EndComp
Text GLabel 7950 2400 0    50   Input ~ 0
FRONIUS_RAW_2
Text GLabel 7950 2700 0    50   Input ~ 0
FRONIUS_GND
$Comp
L Isolator:PC817 U9
U 1 1 5F52600E
P 8950 2500
F 0 "U9" H 8950 2825 50  0000 C CNN
F 1 "PC817" H 8950 2734 50  0000 C CNN
F 2 "Package_DIP:DIP-4_W7.62mm" H 8750 2300 50  0001 L CIN
F 3 "http://www.soselectronic.cz/a_info/resource/d/pc817.pdf" H 8950 2500 50  0001 L CNN
	1    8950 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	9550 800  9550 900 
Wire Wire Line
	9400 800  9550 800 
Text GLabel 9400 800  0    50   Input ~ 0
3v3
Wire Wire Line
	9550 1500 9550 1550
Wire Wire Line
	9250 1500 9550 1500
Connection ~ 9550 1300
Wire Wire Line
	9550 1300 9950 1300
Wire Wire Line
	9550 1300 9550 1200
Wire Wire Line
	9250 1300 9550 1300
Text GLabel 9950 1300 2    50   Input ~ 0
FRONIUS_1
$Comp
L power:GND #PWR019
U 1 1 5F4C37E6
P 9550 1550
F 0 "#PWR019" H 9550 1300 50  0001 C CNN
F 1 "GND" H 9555 1377 50  0000 C CNN
F 2 "" H 9550 1550 50  0001 C CNN
F 3 "" H 9550 1550 50  0001 C CNN
	1    9550 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R13
U 1 1 5F4C3395
P 9550 1050
F 0 "R13" H 9480 1004 50  0000 R CNN
F 1 "10K" H 9480 1095 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 9480 1050 50  0001 C CNN
F 3 "~" H 9550 1050 50  0001 C CNN
	1    9550 1050
	-1   0    0    1   
$EndComp
Wire Wire Line
	7950 1300 8000 1300
$Comp
L Device:R R10
U 1 1 5F474E89
P 8150 1300
F 0 "R10" V 7943 1300 50  0000 C CNN
F 1 "540R" V 8034 1300 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8080 1300 50  0001 C CNN
F 3 "~" H 8150 1300 50  0001 C CNN
	1    8150 1300
	0    1    1    0   
$EndComp
Text GLabel 7950 1300 0    50   Input ~ 0
FRONIUS_RAW_1
Text GLabel 7950 1600 0    50   Input ~ 0
FRONIUS_GND
$Comp
L Isolator:PC817 U5
U 1 1 5F445B21
P 8950 1400
F 0 "U5" H 8950 1725 50  0000 C CNN
F 1 "PC817" H 8950 1634 50  0000 C CNN
F 2 "Package_DIP:DIP-4_W7.62mm" H 8750 1200 50  0001 L CIN
F 3 "http://www.soselectronic.cz/a_info/resource/d/pc817.pdf" H 8950 1400 50  0001 L CNN
	1    8950 1400
	1    0    0    -1  
$EndComp
Text GLabel 14200 1200 0    50   Input ~ 0
PUMP_START_RELAY
Text GLabel 14200 1100 0    50   Input ~ 0
AC_Phase3_Present
Text GLabel 14200 1000 0    50   Input ~ 0
AC_Phase1_Present
Text Notes 11050 1150 0    50   ~ 0
Note:\nAll DC power connectors use the same plug.\nPin 1 - Always GND\nPin 2 - used by 15VDV Supply \nPin 3 - used by Battery\nPin 4 - Used by Netgear switch
Text Notes 11050 5550 0    79   ~ 0
DC Supply
$Comp
L AW_Misc_Library:Polulu_S18V20F12_Voltage_Regulator U12
U 1 1 5F57DCBF
P 12200 4450
F 0 "U12" H 12300 4415 50  0000 C CNN
F 1 "Polulu_S18V20F12_Voltage_Regulator" H 12300 4324 50  0000 C CNN
F 2 "Aw_footprints:Polulu_S18V20x_Regulators" H 12200 4450 50  0001 C CNN
F 3 "" H 12200 4450 50  0001 C CNN
	1    12200 4450
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR042
U 1 1 5F57ECAC
P 11500 4800
F 0 "#PWR042" H 11500 4550 50  0001 C CNN
F 1 "GND" H 11505 4627 50  0000 C CNN
F 2 "" H 11500 4800 50  0001 C CNN
F 3 "" H 11500 4800 50  0001 C CNN
	1    11500 4800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR044
U 1 1 5F57F0A4
P 13100 4800
F 0 "#PWR044" H 13100 4550 50  0001 C CNN
F 1 "GND" H 13105 4627 50  0000 C CNN
F 2 "" H 13100 4800 50  0001 C CNN
F 3 "" H 13100 4800 50  0001 C CNN
	1    13100 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	11900 4750 11500 4750
Wire Wire Line
	12700 4750 13100 4750
Wire Wire Line
	13100 4750 13100 4800
Wire Wire Line
	11500 4800 11500 4750
$Comp
L power:+12VA #PWR048
U 1 1 5F5FDF8E
P 15450 800
F 0 "#PWR048" H 15450 650 50  0001 C CNN
F 1 "+12VA" H 15465 973 50  0000 C CNN
F 2 "" H 15450 800 50  0001 C CNN
F 3 "" H 15450 800 50  0001 C CNN
	1    15450 800 
	1    0    0    -1  
$EndComp
$Comp
L power:+12VA #PWR043
U 1 1 5F5FECB7
P 12500 3750
F 0 "#PWR043" H 12500 3600 50  0001 C CNN
F 1 "+12VA" H 12515 3923 50  0000 C CNN
F 2 "" H 12500 3750 50  0001 C CNN
F 3 "" H 12500 3750 50  0001 C CNN
	1    12500 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	12500 3800 12500 3750
Wire Wire Line
	12200 3800 12500 3800
Wire Wire Line
	15450 900  15450 800 
Wire Wire Line
	15000 900  15450 900 
$Comp
L power:+12VA #PWR045
U 1 1 5F64C9B2
P 13100 5350
F 0 "#PWR045" H 13100 5200 50  0001 C CNN
F 1 "+12VA" H 13115 5523 50  0000 C CNN
F 2 "" H 13100 5350 50  0001 C CNN
F 3 "" H 13100 5350 50  0001 C CNN
	1    13100 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	12700 4950 12800 4950
Wire Wire Line
	12800 4950 12800 5450
Wire Wire Line
	12800 5450 13100 5450
Wire Wire Line
	13100 5450 13100 5350
Text GLabel 11750 5150 0    50   Input ~ 0
BATTERY_SUPPLY
Wire Wire Line
	11800 4950 11900 4950
Wire Wire Line
	11800 4950 11800 5150
Wire Wire Line
	11800 5150 11750 5150
$Comp
L power:GND #PWR047
U 1 1 5F93278C
P 14850 9600
F 0 "#PWR047" H 14850 9350 50  0001 C CNN
F 1 "GND" H 14855 9427 50  0000 C CNN
F 2 "" H 14850 9600 50  0001 C CNN
F 3 "" H 14850 9600 50  0001 C CNN
	1    14850 9600
	1    0    0    -1  
$EndComp
Wire Wire Line
	14850 9550 14850 9600
$Comp
L power:+12VA #PWR046
U 1 1 5F94E82B
P 13400 9550
F 0 "#PWR046" H 13400 9400 50  0001 C CNN
F 1 "+12VA" H 13415 9723 50  0000 C CNN
F 2 "" H 13400 9550 50  0001 C CNN
F 3 "" H 13400 9550 50  0001 C CNN
	1    13400 9550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R16
U 1 1 5F6245C1
P 14150 3900
F 0 "R16" V 13943 3900 50  0000 C CNN
F 1 "10K" V 14034 3900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14080 3900 50  0001 C CNN
F 3 "~" H 14150 3900 50  0001 C CNN
	1    14150 3900
	-1   0    0    1   
$EndComp
Wire Wire Line
	11900 4850 11900 4750
Connection ~ 11900 4750
Wire Wire Line
	11900 5050 11900 4950
Connection ~ 11900 4950
Wire Wire Line
	12700 4850 12700 4750
Connection ~ 12700 4750
Wire Wire Line
	12700 5050 12700 4950
Connection ~ 12700 4950
Wire Wire Line
	8750 10500 9150 10500
Wire Wire Line
	9250 10600 9150 10600
Wire Wire Line
	9150 10600 9150 10500
Connection ~ 9150 10500
Wire Wire Line
	9150 10500 9250 10500
Wire Wire Line
	8800 10400 9250 10400
NoConn ~ 9250 10200
NoConn ~ 9250 10300
NoConn ~ 11900 5150
$Comp
L Device:R R9
U 1 1 5F5D2641
P 6900 7150
F 0 "R9" H 6841 7104 50  0000 R CNN
F 1 "10K" H 6841 7195 50  0000 R CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" H 6900 7150 50  0001 C CNN
F 3 "~" H 6900 7150 50  0001 C CNN
	1    6900 7150
	-1   0    0    1   
$EndComp
Wire Notes Line
	12250 5900 5900 5900
Wire Notes Line
	5900 5900 5900 8000
Wire Notes Line
	5900 8000 12250 8000
Wire Notes Line
	12250 8000 12250 5900
$Comp
L Device:LED D12
U 1 1 5F932778
P 14400 9550
F 0 "D12" H 14393 9295 50  0000 C CNN
F 1 "12VA Supply" H 14393 9386 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 14400 9550 50  0001 C CNN
F 3 "~" H 14400 9550 50  0001 C CNN
	1    14400 9550
	-1   0    0    1   
$EndComp
Wire Wire Line
	13400 9550 13700 9550
$Comp
L Device:R R27
U 1 1 5F932782
P 13850 9550
F 0 "R27" V 13643 9550 50  0000 C CNN
F 1 "820R" V 13734 9550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 13780 9550 50  0001 C CNN
F 3 "~" H 13850 9550 50  0001 C CNN
	1    13850 9550
	0    1    1    0   
$EndComp
Wire Wire Line
	14550 9550 14850 9550
Wire Wire Line
	14000 9550 14250 9550
Wire Wire Line
	13550 9000 13700 9000
Wire Wire Line
	14000 9000 14250 9000
Wire Wire Line
	14550 9000 14850 9000
Wire Wire Line
	13550 8350 13700 8350
Wire Wire Line
	14000 8350 14250 8350
Wire Wire Line
	14550 8350 14850 8350
Wire Wire Line
	14850 8350 14850 8400
Wire Wire Line
	13400 7750 13400 7800
Wire Wire Line
	13400 7800 13700 7800
Wire Wire Line
	14000 7800 14250 7800
Wire Wire Line
	14550 7800 14850 7800
Wire Wire Line
	14850 7800 14850 7850
Wire Wire Line
	3950 5850 3850 5850
Wire Wire Line
	4250 5850 4450 5850
Wire Wire Line
	4750 5850 4850 5850
Wire Wire Line
	4850 5850 4850 5950
$Comp
L power:+12VA #PWR023
U 1 1 5F887C49
P 8100 6900
F 0 "#PWR023" H 8100 6750 50  0001 C CNN
F 1 "+12VA" H 8115 7073 50  0000 C CNN
F 2 "" H 8100 6900 50  0001 C CNN
F 3 "" H 8100 6900 50  0001 C CNN
	1    8100 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7600 6750 7600 6900
Wire Wire Line
	7600 6900 8100 6900
$Comp
L power:+12VA #PWR049
U 1 1 5F8BF1C9
P 11200 6900
F 0 "#PWR049" H 11200 6750 50  0001 C CNN
F 1 "+12VA" H 11215 7073 50  0000 C CNN
F 2 "" H 11200 6900 50  0001 C CNN
F 3 "" H 11200 6900 50  0001 C CNN
	1    11200 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	10700 6750 10700 6900
Wire Wire Line
	10700 6900 11200 6900
$Comp
L Connector:TestPoint TP3
U 1 1 5F5B264C
P 12550 2800
F 0 "TP3" H 12608 2918 50  0000 L CNN
F 1 "TP Battery" H 12608 2827 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 12750 2800 50  0001 C CNN
F 3 "~" H 12750 2800 50  0001 C CNN
	1    12550 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	12550 2800 12550 2950
Connection ~ 12550 2950
Wire Wire Line
	12550 2950 12700 2950
$Comp
L Connector:TestPoint TP2
U 1 1 5F606DDC
P 11850 1400
F 0 "TP2" H 11908 1518 50  0000 L CNN
F 1 "TP 15V" H 11908 1427 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 12050 1400 50  0001 C CNN
F 3 "~" H 12050 1400 50  0001 C CNN
	1    11850 1400
	1    0    0    -1  
$EndComp
Wire Wire Line
	11850 1400 11850 1950
Connection ~ 11850 1950
Wire Wire Line
	11850 1950 11700 1950
$Comp
L Connector:TestPoint TP6
U 1 1 5F65DBD3
P 3350 5550
F 0 "TP6" H 3408 5668 50  0000 L CNN
F 1 "TP 3v3A" H 3408 5577 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3550 5550 50  0001 C CNN
F 3 "~" H 3550 5550 50  0001 C CNN
	1    3350 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 5850 3350 5850
Connection ~ 3850 5850
Wire Wire Line
	3350 5550 3350 5850
Connection ~ 3350 5850
Wire Wire Line
	3350 5850 3850 5850
$Comp
L Connector:TestPoint TP4
U 1 1 5F6B4A02
P 12800 4400
F 0 "TP4" H 12858 4518 50  0000 L CNN
F 1 "TP 12VA" H 12858 4427 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 13000 4400 50  0001 C CNN
F 3 "~" H 13000 4400 50  0001 C CNN
	1    12800 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	12800 4400 12800 4950
Connection ~ 12800 4950
$Comp
L Connector:TestPoint TP5
U 1 1 5F6D2F65
P 8200 10650
F 0 "TP5" H 8258 10768 50  0000 L CNN
F 1 "TP 5V" H 8258 10677 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 8400 10650 50  0001 C CNN
F 3 "~" H 8400 10650 50  0001 C CNN
	1    8200 10650
	1    0    0    -1  
$EndComp
Wire Wire Line
	7950 10850 8200 10850
Wire Wire Line
	9050 10700 9250 10700
Wire Wire Line
	8200 10650 8200 10850
$Comp
L Connector:TestPoint TP1
U 1 1 5F7666D2
P 5600 4700
F 0 "TP1" H 5658 4818 50  0000 L CNN
F 1 "TP GND" H 5658 4727 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 5800 4700 50  0001 C CNN
F 3 "~" H 5800 4700 50  0001 C CNN
	1    5600 4700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR050
U 1 1 5F766B81
P 5600 4900
F 0 "#PWR050" H 5600 4650 50  0001 C CNN
F 1 "GND" H 5605 4727 50  0000 C CNN
F 2 "" H 5600 4900 50  0001 C CNN
F 3 "" H 5600 4900 50  0001 C CNN
	1    5600 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4700 5600 4900
$Comp
L Connector:Screw_Terminal_01x06 J7
U 1 1 5F447505
P 14850 5650
F 0 "J7" H 14930 5642 50  0000 L CNN
F 1 "Plug in Screw_Terminal" H 14930 5551 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-6_P5.08mm" H 14850 5650 50  0001 C CNN
F 3 "~" H 14850 5650 50  0001 C CNN
	1    14850 5650
	1    0    0    -1  
$EndComp
Wire Wire Line
	14450 5450 14650 5450
Wire Wire Line
	14650 5650 14450 5650
Wire Wire Line
	14450 5750 14650 5750
Wire Wire Line
	14450 5850 14650 5850
Wire Wire Line
	14650 5950 14450 5950
NoConn ~ 14650 5550
$Comp
L Jumper:Jumper_2_Bridged JP1
U 1 1 5F63CDA6
P 8600 10950
F 0 "JP1" H 8600 11145 50  0000 C CNN
F 1 "5V Enable Jumper" H 8600 11054 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Horizontal" H 8600 10950 50  0001 C CNN
F 3 "~" H 8600 10950 50  0001 C CNN
	1    8600 10950
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 10950 8800 10950
Wire Wire Line
	9050 10700 9050 10950
Wire Wire Line
	8400 10950 8200 10950
Wire Wire Line
	8200 10950 8200 10850
Connection ~ 8200 10850
$Comp
L AW_Misc_Library:PCB_Switch_RS479-1413 SW1
U 1 1 5F69DD85
P 14400 7450
F 0 "SW1" H 13750 8350 50  0000 L CNN
F 1 "PCB_Switch_RS479-1413" H 13500 7800 50  0000 L CNN
F 2 "Aw_footprints:PCB Switch RS 479-1413" H 14400 7650 50  0001 C CNN
F 3 "~" H 14400 7650 50  0001 C CNN
	1    14400 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	14100 6650 14200 6650
Wire Wire Line
	13600 6650 13600 7050
Wire Wire Line
	13600 7050 13700 7050
Connection ~ 13600 6650
Wire Wire Line
	13600 6650 13700 6650
Wire Wire Line
	14100 7050 14200 7050
Wire Wire Line
	14200 7050 14200 6650
Connection ~ 14200 6650
Wire Wire Line
	14200 6650 14500 6650
Text Notes 13350 7000 0    50   ~ 0
This switch seems to have incorrect\nwiring.
$EndSCHEMATC
