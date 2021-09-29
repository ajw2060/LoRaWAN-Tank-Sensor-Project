# This is the micropython code for the PyCom LoPy4 module.  It does the following.
# - manages the sensor readings for the submersible pressure sensor as well as the various environmental sensors
# - periodically connects to TTN to report the data.


# Change history
# V1    2018-08-20  First attempt to consolidate test components.
# V2    2018-08-24  Added the extra check in the measure 2 loop.
# V3    2018-10-13  Reintroduce UART1 for serial logging.
# V4    2018-10-21  Introduced SHT31 readings
# V5    2018-11-07  Introduced error handler on LoRa join.
# V6    2020-02-01  Changed from ultrasonic to submersible sensor.
# V7    2021-02-17  Picked this up again in 2021, but with the LCD removed and ADS1115 used for A-D conversion.
# v8    2021-04-08  Deleted the code which explicitly set the LoRaWAN downlink channels (and fixed the repeatability issue)
# v9    2021-05-01  Created a separate JSON AppKeys file common to all registered devices to contain all AppKeys.
# v10   2021-05-02  Added a diagnostic loop to read all A-D channels when in offline mode (for testing).


import pycom
import utime
import time

import machine
from machine import UART
from machine import Timer
from machine import Pin
from machine import I2C

from network import LoRa
from network import WLAN
from network import Bluetooth

import sys
import socket
import ubinascii
import uos
import struct
import binascii
import json

import BME280
import ads1x15

import tank_sensor_config       # Local configuration file


'''
This is the overall flow of the application
- Startup.  We may have just woken from deep sleep, or been rebooted.  At
  present this is not significant, but we report it anyway.
- Capture the current time.  This is used later to determine how long the
  processing has taken, and so schedule the length of deep sleep time.
- Join the LoRa WAN.
- Startup the submersible sensor and get the pressure reading.
- Get the environmental readings (temp, humidity, pressure, battery, light)
- Transmit the data and then close the WAN.
- Go into deep sleep for the required interval.

Module physical pin connections used are as follows.  The corresponding
Pin Names are shown in parenthesis as (P17).
------------------------------------
Pin 5/6 = UART1 TX/RX for serial console.  Leave disconnected to minimise power drain.
Pin 10/13 = UART2 TX/RX. Not in use.
Pin 11/12 (P9, P10) = i2C bus.  (P9=SDA, P10=SCL)
Pin 22 (P20) = online or offline sense switch. Ground this to run offline.
Pin 23 (P21) = Boost converter enable (for 24V boost converter which powers the submersible sensor).
All the analog readings from sensors are converted to digital via the ADS1115 module
so none of the microcontoller analog inputs are needed.
'''

# ---- Analog channels used on ADS1115 Analog to Digital Converter ------------
# These define the channels used on the ADS1115 Analog to Digital Converter.
AD_CHANNEL_BATTERY_VOLTAGE = 0
AD_CHANNEL_TANK_PRESSURESENSOR = 1
AD_CHANNEL_LDR_SENSOR = 2
AD_CHANNEL_SPAREUNUSED = 3


# ---- Battery voltage conversion constant -------------------------------------
# This value is used to derive the actual battery voltage from the result 
# of the analog read from the voltage divider.
BATTERY_VOLTAGE_CONSTANT = 19.1056


# ---- Debug logger ------------------------------------------------------------
def c_log(logMessage):
    #logger.write(logMessage + "\n\r")
    print(logMessage + "\r")


# ---- Chrono snapshot --------------------------------------------------------
def chrono_snap():
    time_right_now = chrono.read()
    c_log("==> Chrono snap immediate value = {:.3f} Seconds.".format(time_right_now))



# ---- Generic LED flasher -----------------------------------------------------
def led_flasher(flash_state, flash_count, flash_message):
    '''
    This generic routine is mainly for error alerting.
    Red flash count values for errors are as follows
    5 = unused
    10 = LoRa join failure
    '''
    if (flash_state == 'E'):    # Error condition
        for i in range (flash_count):
            pycom.rgbled(0x500000) # Red flash to indicate error
            time.sleep(0.1)
            pycom.rgbled(0x000000)
            time.sleep(0.1)
    '''
    Blue flash count values for status messages already implemented
    10 = about to hibernate
    '''
    if (flash_state == 'S'):       # Just a status indicator
        for i in range (flash_count):
            pycom.rgbled(0x000050) # Blue flash to indicate status
            time.sleep(0.15)
            pycom.rgbled(0x000000)
            time.sleep(0.15)


# ---- LED Rainbow function -----------------------------------------------------
def led_rainbow():
    # This just increments and decrements the onboard LED to create a pretty effect
    c_log("LED Rainbow pattern")

    # Red increase to 255
    for i in range(0, 255):
        pycom.rgbled(0 + i*65536)       # Increment red
        time.sleep(0.005)
    
    # Red decrease to 0 while green increase to 255
    for i in range(0, 255):
        pycom.rgbled((16711680 - i*65536) + (i*256))    # Decrement red and increment green
        time.sleep(0.005)
    
    # Green decrease to 0 while blue increases to 255
    for i in range(0, 255):
        pycom.rgbled((65280 - i*256) + i)    # Decrement green and increment blue
        time.sleep(0.005)
    
    # Blue decreases to 0 
    for i in range(0, 255):
        pycom.rgbled((255 - i))    # Decrement blue 
        time.sleep(0.005)

    c_log("LED Rainbow complete")


# ---- String manipulation -----------------------------------------------------
def rawbytes(s):
    # Convert a string to raw bytes without encoding
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('b', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)



# ---- Get the AppKey needed by this device from the external AppKeys file
def get_my_appkey(arg_appkey_file, arg_loramac):
    c_log("  AppKey file to search [" + arg_appkey_file + "].")
    c_log("  Device EUI to find    [" + arg_loramac + "].")
    try:
        with open(arg_appkey_file) as json_file:
            appkey_data = json.load(json_file)
            localMyAppKey = ubinascii.unhexlify(appkey_data["" + arg_loramac + ""])
            c_log("  Found required AppKey for this Device EUI.")
            return localMyAppKey
    except:
        c_log("ERROR 902.  The requiured AppKey was not found in the file.  Terminating now.")   
        sys.exit(902) 


# ---- Join a network using OTAA -----------------------------------------------
def do_lora_otaa_join():
    c_log("\nStarting LoRa Join.")
    lora.join(activation=LoRa.OTAA, auth=(myAppEui, myAppKey), timeout = 0, dr = 0)   # Try join on lowest data rate
    c_log("  Return from join call.")
    # Wait until the module has joined the network
    x=0
    while (not lora.has_joined() and x < lora_join_attempts):
        pycom.rgbled(0x0f0f00) # pale red plus pale green
        c_log('    Waiting [%d] on LoRaWAN join to complete successfully...' %(x))
        x=x+1
        time.sleep(2.0)  # Wait time between join attempts
        if (lora.has_joined() and x < lora_join_attempts):
            c_log('  Join completed.')
            # print(lora.stats())
            pycom.rgbled(0x007f00) # Bright green indicates connected OK
            time.sleep(1)
            pycom.rgbled(0x000000)
            return(True)
        else:
            pycom.rgbled(0x000000)
            time.sleep(0.5)

    c_log("ERROR.  LoRaWAN join was not successful during the allowed period.")
    return(False)


# ---- This squirrels away the nuts and puts yogi bear to sleep for winter -----
def go_hibernate(cause_code):
    '''
        The cause_code can control the duration of hibernation.
        - We can have normal hibernation at the standard duration when everything goeas as desired
        - We have a shorter ('retry hibernation') when LoRaWAN join fails
        Cause_code 0 means normal sleep until next reading.
        Cause_code 1 means join failed so try again soon using short_hibernate_interval.

        The chrono reads are specified in seconds.  The processing interval is
        also specified in seconds.  The time_to_sleep value must be passed
        in milliseconds.
    '''

    if (cause_code == 0):
        c_log("  This is a normal hibernation so saving LoRaWAN state into NVRAM.")
        lora.nvram_save()
        processing_interval = long_hibernate_interval
        c_log("  Deep sleep interval for normal hibernation is {:.0f} Seconds. \r".format(processing_interval))
        time.sleep(2)
    else:
        c_log("  This is a failed connect attempt so no need to save LoRaWAN state.")
        processing_interval = short_hibernate_interval
        c_log("  Deep sleep interval for LoRaWAN join failure and retry is {:.0f} Seconds. \r".format(processing_interval))
        time.sleep(2)

    led_flasher('S', 10, 'Now hibernating')
    hardreset_counter = pycom.nvs_get('hrc')
    sleep_counter = pycom.nvs_get('sleeps')

    c_log("  Saving sleep counter to NVRAM ready for deep sleep.")
    sleep_counter+=1
    c_log("  Writing sleeps counter value [" + str(sleep_counter) + "] into NVRAM.")
    pycom.nvs_set('sleeps', sleep_counter)


    # ---- Now calculate how long this processing has taken
    completed_time = chrono.read()
    c_log("  Chrono value at completion was (roughly) {:.3f} Seconds. \r".format(completed_time))

    processing_time_taken = completed_time - startup_time
    c_log("  Processing time taken during this cycle {:.1f} Seconds. \r".format(processing_time_taken))

    seconds_to_sleep = processing_interval - processing_time_taken
    c_log("  Resulting deep sleep duration will be {:.1f} Seconds. \r".format(seconds_to_sleep))
    
    millis_to_sleep = int(seconds_to_sleep * 1000)
    #c_log("  Now entering deep sleep for about {:.1f} Seconds. \r".format(seconds_to_sleep))
    c_log("  Now entering deep sleep for about {:.0f} Minutes. \r".format(seconds_to_sleep / 60))
    print("Now entering deep sleep for exactly {:.1f} mS. \r".format(millis_to_sleep))
    machine.deepsleep(millis_to_sleep)


# ----Diagnostic mode analogue reads
def get_analog_reads_diag():
    '''
        This function gets the readings from the analog to digital converter and 
        presents them in a pretty table.  This is intende for offline dignostic use
        to test the response from the converter.
    '''
    local_loop_counter = 100
    local_loop_delay = 0.15

    c_log("  Reading analog values in the loop.  Counter [" + str(local_loop_counter) + "].")
    c_log('  Enabling 24 volt DC supply to sensor and allowing stabilisation delay.')
    dpin_24boost_enable.value(1)
    time.sleep(1)
    c_log("----- Raw Analogue Readings -----------------------------------------")
    c_log("{: >12} {: >12} {: >12} {: >12} {: >12}".format("Count", "Battery", "LDR", "Pressure", "Unused"))
    for i in range (local_loop_counter):
        pycom.rgbled(0x0F0F05)  # Pale whitish
        ad_battery = adc.read(0, AD_CHANNEL_BATTERY_VOLTAGE)
        ad_ldr = adc.read(0, AD_CHANNEL_LDR_SENSOR)
        ad_pressure = adc.read(0, AD_CHANNEL_TANK_PRESSURESENSOR)
        ad_spare = adc.read(0, AD_CHANNEL_SPAREUNUSED)
        c_log("{: >12} {: >12} {: >12} {: >12} {: >12}".format(i+1, ad_battery, ad_ldr, ad_pressure, ad_spare))
        pycom.rgbled(0x000000)  # Off
        time.sleep(local_loop_delay)
    c_log("---------------------------------------------------------------------")
    c_log("  Disabling 24 volt DC supply to pressure sensor.")
    dpin_24boost_enable.value(0)
    time.sleep(1)





# ---- Main function -----------------------------------------------------------
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n------------- System startup - Submersible Sensor Version ---------------")
print("All debug output will be directed to UART1.")
# All future log output goes to UART1.


# ---- Initialise the logger UART
logger = UART(1, baudrate=57600, pins=('P3', 'P4')) # Standard pins but why not specify them.
c_log("\r\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n----------------------- System startup -----------------------")
c_log("Tank water level monitoring system.")
c_log("PyCom LoPy4 Submersible pressure sensor monitor.")


# ---- Start chrono
c_log("\nStartup tasks.")
c_log("  Starting Chrono now.")
chrono = Timer.Chrono()


# ---- Grab the startup time and stash it.
chrono.start()
startup_time = chrono.read()
c_log("  Chrono value at start = {:.3f} Seconds.".format(startup_time))


# ---- LED control
c_log("  Disable heartbeat LED.")
pycom.heartbeat(False)


# ---- Flash the green LED a few times so the observer knows it has started
c_log("  Flashing green LED a few times.")
for i in range (5):
    pycom.rgbled(0x000F00)  # Green
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(0.2)



# ---- Disable radios to conserve power.
c_log("\nDisable onboard radios to reduce power consumption.")
c_log("  Disable Wi-Fi.")
wlan = WLAN()
wlan.deinit()
c_log("  Disable Bluetooth.")
bluetooth = Bluetooth()
bluetooth.deinit()


# ---- Assign variables from the config file
c_log("\nAssign local variables from the config file.")
long_hibernate_interval = tank_sensor_config.tsc_processing_interval    # Delay between readings in seconds
short_hibernate_interval = tank_sensor_config.tsc_retry_interval        # Retry interval when LoRaWAN join fails
myAppEui = ubinascii.unhexlify(tank_sensor_config.tsc_myAppEui)
#myAppKey = ubinascii.unhexlify(tank_sensor_config.tsc_myAppKey)
lora_join_attempts = tank_sensor_config.tsc_lora_join_attempts
appkey_file = tank_sensor_config.tsc_appkey_file

try:
    c_log("  Processing (deep sleep) interval .. [" + str(long_hibernate_interval) + "] seconds.")
    c_log("  Retry interval when join fails .... [" + str(short_hibernate_interval) + "] seconds.")
    c_log("  Application EUI ................... [" + str(ubinascii.hexlify(myAppEui)) + "].")
    #c_log("  App Key = [" + str(ubinascii.hexlify(myAppKey)) + "].")
    c_log("  LoRa join attempt counter ......... [" + str(lora_join_attempts) + "].")
    c_log("  Name of the AppKeys file .......... [" + appkey_file + "].")
except:
    c_log("ERROR 901.  Problem reading or displaying parameter from configuration file.")
    sys.exit(901)



# ---- Initialise digital I/O pins --------------------------------------------
c_log("\nInitialise system digital I/O pins.")
dpin_online = Pin('P20', mode=Pin.IN, pull=Pin.PULL_UP)
dpin_24boost_enable = Pin('P21', mode=Pin.OUT)


# ---- Setup for I2C for various modules --------------------------------------
c_log("\nInitialise I2C I/O pins and scan for available devices.")
i2c = I2C(0)                            # create on bus 0
i2c = I2C(0, I2C.MASTER)                # create and init as a master
i2c = I2C(0, pins=('P9','P10'))         # create and use default PIN assignments (P9=SDA, P10=SCL)
i2c.init(I2C.MASTER, baudrate=20000)    # init as a master
i2c_device_list = i2c.scan()

if len(i2c_device_list) == 0:
    led_flasher('E', 7, 'No I2C devices found')
    c_log("ERROR 900.  No I2C devices detected.  The system cannot operate without these devices and will now terminate.")
    print("\nERROR 900.  No I2C devices detected.  The system cannot operate without these devices and will now terminate.\n")
    sys.exit(2)
else:
    c_log("  Number of I2C devices found = [" + str(len(i2c_device_list)) + "].")
    for this_item in i2c_device_list:
        c_log("  ..Device found at Hex address: [" + str(hex(this_item)) + "].")
c_log("  Done.")


# ---- Check the online/offline state switch ----------------------------------
c_log("\nCheck for online or offline operation.")
if(dpin_online.value()):
    online_mode = True
    c_log("  Running in normal ONLINE mode.  LoRaWAN Communications will be enabled.")
    time.sleep(1)   
else:
    online_mode = False
    c_log("  Running in diagnostic OFFLINE mode. LoRaWAN communications will be disabled.")
    time.sleep(2)   # Linger longer when offline...


# ---- Set up the NVRAM deep sleeps counter
c_log("\nChecking for the presence of the NVRAM 'deep_sleeps' counter.")
try:
    sleep_counter = pycom.nvs_get('sleeps')
    c_log("  The retrieved 'deep_sleeps' counter value is [" + str(sleep_counter) + "].")
except:
    c_log("  The 'deep_sleeps' counter was not found in storage so it will be initialised.")
    pycom.nvs_set('sleeps', 0)
    sleep_counter = pycom.nvs_get('sleeps')
    c_log("  Initialised 'deep_sleeps' counter now with value [" + str(sleep_counter) + "].")
# chrono_snap()


# ---- Set up the NVRAM hard resets counter
c_log("\nChecking the presence of NVRAM 'hard_resets' counter.")
try:
    hardreset_counter = pycom.nvs_get('hrc')
    c_log("  The retrieved 'hard_resets' counter value is [" + str(hardreset_counter) + "].")
except:
    c_log("  The 'hard_resets' counter was not found in storage so it will be initialised.")
    pycom.nvs_set('hrc', 0)
    hardreset_counter = pycom.nvs_get('hrc')
    c_log("  Initialised 'hard_resets' counter now with value [" + str(hardreset_counter) + "].")


# ---- General decorative startup reports
c_log("\n------------- Interesting Startup Details ----------------------")
c_log(" Firmware related")
c_log("   Machine unique ID ..........  " + str(ubinascii.hexlify(machine.unique_id())))
c_log("   System Name [0] ............  " + str(os.uname()[0]))
c_log("   Node Name   [1] ............  " + str(os.uname()[1]))
c_log("   Release     [2] ............  " + str(os.uname()[2]))
c_log("   Version     [3] ............  " + str(os.uname()[3]))
c_log("   Machine     [4] ............  " + str(os.uname()[4]))
c_log("   LoRaWAN     [5] ............  " + str(os.uname()[5]))
c_log("   Sigfox      [6] ............  " + str(os.uname()[6]))
c_log("   PyBytes     [7] ............  " + str(os.uname()[7]))
c_log(" Counters and other status information")
c_log("   Machine CPU Frequency ......  " + str(machine.freq()))
c_log("   Stack information ..........  " + str(machine.info()))
c_log("   The 'hard_resets' counter ..  " + str(hardreset_counter))
c_log("   The 'deep_sleeps' counter ..  " + str(sleep_counter))
c_log("   Normal processing interval .  {:.0f} Seconds \r".format(long_hibernate_interval))
c_log("   Retry processing interval ..  {:.0f} Seconds \r".format(short_hibernate_interval))
c_log("   Online operation mode ......  " + str(online_mode))
c_log("---------------------------------------------------------------")


# ---- LoRa initialisation
c_log("\nLoRa initialisation and network join.")
c_log("  Select LoRaWAN and region AU915 and enable ADR.")
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915, public=True, adr=True, device_class=LoRa.CLASS_A)

# ---- Show some decorative detail
c_log("\nDevice EUI (LoRa MAC) [%s]." % (ubinascii.hexlify(lora.mac()).upper().decode('ascii')))

# ---- Dig out the appkey needed by this device -------------------------------
c_log("\nLook up the AppKey needed by this node to connect to this application.")
myAppKey = get_my_appkey(appkey_file, ubinascii.hexlify(lora.mac()).upper().decode('ascii'))


# ---- Remove default channels
c_log("\nRemoving all LoRaWAN channels 0-72.")
for index in range(0, 72):
    lora.remove_channel(index)


# ---- Set  AU ISM 915 channel plan for TTN Australia
# ---- Add the uplink channels
c_log("  Adding AU915 Sub Band 2 channels 8-15 and 65.")
for index in range(8, 16):
    uplink_frequency = 915200000 + index * 200000
    lora.add_channel(index, frequency=uplink_frequency, dr_min=0, dr_max=5)  # Changed from 3
    c_log("   Added Uplink Channel [{:02d}] using Frequency [{:05.1f}] MHz" .format(index, uplink_frequency / 1000000))

lora.add_channel(65, frequency=917500000,  dr_min=6,  dr_max=6) # Changed from 4 and 4
c_log("   Added Uplink Channel [65] Using Frequency [917.5] MHz")


# Seems like no need to add the downlink channels.  
# This has been 100% relaible since explicit add of downlinks was removed.




# ---- Figure out what restarted the system this time
c_log("\nChecking reason for this wake up " + str(machine.wake_reason()))
int_wakeup_cause = machine.wake_reason()[0]
if int_wakeup_cause == 0:
    c_log("  System restarted due to hard reset.")
    lora.nvram_erase()
    c_log("  LoRa NVRAM settings erased.")
    local_hardreset_counter = pycom.nvs_get('hrc')
    local_hardreset_counter += 1
    c_log("  Writing new 'hard_resets' counter value [" + str(local_hardreset_counter) + "] into NVRAM.")
    pycom.nvs_set('hrc', local_hardreset_counter)
elif int_wakeup_cause == 2:
    c_log("  System restarted due to deep sleep wakeup.")
    lora.nvram_restore()
    c_log("  LoRa NVRAM settings restored.")
else:
    c_log("  Unknown reset cause.")
    lora.nvram_erase()
    c_log("  LoRa NVRAM settings erased for safety due to unknown restart cause.")


# ---- Check if LoRa join has already been done in a previous life.
if not online_mode:
    c_log("\nSystem is operating OFFLINE so LoRaWAN communications will not be attempted.")
else:
    c_log("\nSystem is operating ONLINE so LoRaWAN communications will be used.")
    c_log("  Checking if a LoRaWAN join has already been done during a previous session.")
    if (lora.has_joined()):
        c_log('  LoRaWAN join was previously completed so it will not be repeated.')
        pycom.rgbled(0x007f00) # Bright green indicates connected OK
        time.sleep(1)
        pycom.rgbled(0x000000)
    else:
        c_log("  No NVRAM data showing previous LoRaWAN join so a new join is required.")
        if not (do_lora_otaa_join()):
            led_flasher('E', 10, 'LoRaWAN join failure')    # ---- Flash red a few times to report the error
            c_log("LoRaWAN join reported a failure so aborting further activity.")
            lora.nvram_erase()
            c_log("LoRaWAN NVRAM settings erased due to this join failure.")   #Not really needed, but just to be sure.
            c_log("\nPreparing short hibernate because LoRaWAN join was not successful.")
            go_hibernate(1)
    # Should be joined (new or existing) by here


    # ---- Create the raw socket to send some data
    c_log("\nCreating the raw socket.")
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)


    # ---- Set the LoRaWAN data rate
    c_log("  Set socket data rate.")
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


# ---- Do the measurements now so we have some actual data to send
# ---- Get BME280 readings which are returned as a string.
c_log("\nStart BME280 sensor reading.")
bme = BME280.BME280(i2c=i2c)
temp = bme.temperature
hum = bme.humidity
pres = bme.pressure
c_log('  Temperature ==> ' + temp)
c_log('  Humidity    ==> ' + hum)
c_log('  Pressure    ==> ' + pres)

'''
    Temperature reading is manipulated as follows,
    -   Add 100 (to remove subzero readings)
    -   Multiply by 10 to capture one decimal point precision
        This produces a value of (say) 1257 for a temp of 25.7, which
        uses two bytes to send.
    Humidity
    -   No manipulation needed so the actual value is returned.
    '''

reportable_temperature = int((float(temp) + 100) * 10)
reportable_humidity = int(round(float((hum))))
reportable_atmospheric_pressure = int(round(float(pres)))


# ---- Get the analog readings from the ADS1115 
c_log("\nStart ADS1115 Analog to Digital converter to get analog sensor readings.")
GAIN = 1
adc = ads1x15.ADS1115(i2c, 0x48, GAIN)


if not online_mode:
    c_log("  In OFFLINE mode the debug reads get thrown in first.")
    get_analog_reads_diag()


# ---- 01 - Battery voltage divider
c_log('  01 - Get battery voltage from ADS1115 analog channel [' + str(AD_CHANNEL_BATTERY_VOLTAGE) + '].')
battery_accumulated_count = 0
battery_average_count = 0
battery_reading_repeater = 10
for i in range(battery_reading_repeater):
    battery_accumulated_count += adc.read(0, AD_CHANNEL_BATTERY_VOLTAGE)
    pycom.rgbled(0x0F000F)  # Dim purple
    time.sleep(0.5)
    pycom.rgbled(0x000000)  # Off
battery_average_count =  battery_accumulated_count/ battery_reading_repeater
# Divide this value by the conversion constant to get the actual voltage to report.
# This will provide a four digit decimal number which is 100 times the actual voltage.
# This avoide s the need to manage a decimal point.  The top of the range will be 
# around 1365 representing 13.65 volts.
c_log('    The averaged (high resolution) battery voltage count is [' + str(battery_average_count) + '].')
reportable_count_battery = battery_average_count / BATTERY_VOLTAGE_CONSTANT
c_log('    The reportable (centi-volts) battery voltage is [' + str(reportable_count_battery) + '].')


# ---- 02 - Submersible pressure sensor shunt voltage
c_log('  02 - Get submersible pressure sensor voltage from ADS1115 analog channel [' + str(AD_CHANNEL_TANK_PRESSURESENSOR) + '].')
pressure_accumulated_count = 0
pressure_average_count = 0
pressure_reading_repeater = 10
c_log('    Enabling 24 volt DC supply to sensor and allowing stabilisation delay.')
dpin_24boost_enable.value(1)
time.sleep(1)
for i in range(pressure_reading_repeater):
    pressure_this_read = adc.read(0, AD_CHANNEL_TANK_PRESSURESENSOR)
    pressure_accumulated_count += pressure_this_read
    pycom.rgbled(0x0F0F00)  # Dim yellow
    time.sleep(0.5)
    pycom.rgbled(0x000000)  # Off
pressure_average_count =  pressure_accumulated_count/ pressure_reading_repeater

# Check if the value is below zero.  This will likely happen if the sensor is not connected.
# Rather than report any sub-zero values, just set it to zero.
c_log('    The averaged (high resolution) pressure count is [' + str(pressure_average_count) + '].')
if pressure_average_count < 0:
    c_log('    The "pressure_average_count" is below zero.  Sensor may be faulty. Value set to zero.')
    pressure_average_count = 0

reportable_count_water_pressure = int(round(pressure_average_count))
c_log('    The reportable pressure count value is [' + str(reportable_count_water_pressure) + '].')
if not online_mode:
    c_log("    ==> In OFFLINE mode an extra 30 second delay is inserted here.")
    time.sleep(30)
c_log('    Disabling 24 volt DC supply to sensor.')
dpin_24boost_enable.value(0)

# ---- 03 - LDR sensor reading
c_log('  03 - Get LDR sensor voltage from ADS1115 analog channel [' + str(AD_CHANNEL_LDR_SENSOR) + '].')
ldr_accumulated_count = 0
ldr_average_count = 0
ldr_reading_repeater = 10
ldr_reading_divisor = 256
pycom.rgbled(0x000000)  # Ensure the LED really is off before reading the LDR
time.sleep(0.1)
for i in range(ldr_reading_repeater):
    ldr_accumulated_count += adc.read(0, AD_CHANNEL_LDR_SENSOR)
    pycom.rgbled(0x000F0F)  # Dim cyan
    time.sleep(0.5)
    pycom.rgbled(0x000000)  # Off
ldr_average_count =  ldr_accumulated_count/ ldr_reading_repeater
# Also divide the result by 128 to give me about an 8 bit resolution result.
# This provides 256 steps of illumination.  This is accurate enough.
c_log('    The averaged (high resolution) LDR sensor count is [' + str(ldr_average_count) + '].')
reportable_count_ldr = int(round(ldr_average_count / ldr_reading_divisor))
c_log('    The reportable (low resolution) LDR sensor count is [' + str(reportable_count_ldr) + '].')


# ---- Once all the readings are in hand, append to the byte array
c_log("\nPreparing the LoRaWAN message payload by concatenating strings.")
lora_message_payload=""
#print("payload = [" + str(lora_message_payload) +"]")

# ---- Element 1 is a protocol identifier (1 byte)
# This allows future modification of the payload without having to have all devices on the same version.
# The parser is instructed to parse based on just the first byte whch is the format identifier.
# This version is Format 2.  (Format 1 was never formally identified so bit of a problem with backward compatibility)
protocol_formatidentifier_hex = '{:01X}'.format(2)
c_log("  01 Append format identifier   \t [" + protocol_formatidentifier_hex + "] \t\t Uses 'Format 2' payload.")
lora_message_payload += protocol_formatidentifier_hex

# ---- Element 2 is Sequence number (4 characters)
mysleeps_dec = '{:04d}'.format(pycom.nvs_get('sleeps')%10000)         # This number needs to be a modulus to constrain to 4 characters.
c_log("  02 Append sequence number     \t [" + mysleeps_dec + "] \t decimal deep sleep counts.")
lora_message_payload += mysleeps_dec

# ---- Element 3 is Water level (4 characters)
# This one is the raw reading from the AD converter presented in hex with padding
mywaterlevel_hex = '{:04X}'.format(reportable_count_water_pressure)
c_log("  03 Append water level reading \t [" + mywaterlevel_hex + "]   \t hex from submersible sensor.")
lora_message_payload += mywaterlevel_hex

# ---- Element 4 is enclosure temperature (4 characters)
myenclosuretemp_dec = '{0:04.0f}'.format(reportable_temperature)        # Rounds, truncates decimals and zero pads to 4 characters
c_log("  04 Append temperature reading \t [" + myenclosuretemp_dec + "] \t from BME280.")
lora_message_payload += myenclosuretemp_dec

# ---- Element 5 is enclosure humidity (2 characters) readable in decimal just as reported.
myenclosurehumi_dec = '{0:02.0f}'.format(reportable_humidity)               
c_log("  05 Append humidity reading    \t [" + myenclosurehumi_dec + "]   \t from BME280.")
lora_message_payload += myenclosurehumi_dec

# ---- Element 6 is enclosure atmospheric pressure (4 characters)
myenclosurepressure_dec = '{0:04.0f}'.format(reportable_atmospheric_pressure)   # Rounds, truncates decimals and zero pads to 4 characters
c_log("  06 Append atmospheric pressure    \t [" + myenclosurepressure_dec + "] \t from BME280.")
lora_message_payload += myenclosurepressure_dec

# ---- Element 7 is the Battery Voltage (4 characters in centi-volts)
mybatteryvoltage_dec = '{0:04.0f}'.format(reportable_count_battery)    # Rounds, truncates decimals and zero pads to 4 characters
c_log("  07 Append battery voltage     \t [" + mybatteryvoltage_dec + "]   \t actual centivolts.")
lora_message_payload += mybatteryvoltage_dec

# ---- Element 8 is the ambient light reading (2 byte)
ldrreading_hex = '{:02X}'.format(reportable_count_ldr)                       # 8 bits
c_log("  08 Append ambient light level \t [" + ldrreading_hex + "]   \t hex from LDR.")
lora_message_payload += ldrreading_hex

c_log("  Completed payload assembly \t\t [" + str(lora_message_payload) +"].")



# ---- Finally just dump the payload
if not online_mode:
    c_log("\nSystem is in OFFLINE mode so LoRaWAN transmission will not be attempted.")
    c_log("Hibernation does not occur in offline mode.")
else:
    c_log("\nReady to send LoRaWAN data.")

    # ---- Make the socket blocking before sending
    c_log("  Make socket blocking before transmission.")
    s.setblocking(True)
    time_at_transmit = chrono.read()

    c_log("  Sending payload of [{:d}] bytes.".format(len(lora_message_payload)))
    send_count = s.send(bytearray(lora_message_payload))  # Send the data
    
    # ---- Make the socket non blocking after sending
    c_log("  Make socket non blocking after transmission.")
    s.setblocking(False)
    time_after_transmit = chrono.read()
    transmission_time = time_after_transmit - time_at_transmit
    c_log("  Transmit took [{:.3f}] seconds.".format(transmission_time))
    c_log("  Transmit sent %s bytes" % send_count)

    # print(lora.stats())
    c_log("  LoraWAN message has been sent.")
    
    # ---- Details of the last transmission
    c_log("\n------- LoRaWAN Transmit Statistics ------------")
    c_log("   RX Timestamp [0] ......  " + str(lora.stats()[0]))
    c_log("   RSSI [1] ..............  " + str(lora.stats()[1]))
    c_log("   SNR [2] ...............  " + str(lora.stats()[2]))
    c_log("   SFRX [3] ..............  " + str(lora.stats()[3]))
    c_log("   SFTX [4] ..............  " + str(lora.stats()[4]))
    c_log("   TX Trials [5] .........  " + str(lora.stats()[5]))
    c_log("   TX Power [6] ..........  " + str(lora.stats()[6]))
    c_log("   TX Time on Air [7] ....  " + str(lora.stats()[7]))
    c_log("   TX Counter [8] ........  " + str(lora.stats()[8]))
    c_log("   TX Frequency [9] ......  " + str(lora.stats()[9]))
    c_log("-----------------------------------------------")

    # Show the pretty rainbow effect on the built in LED.
    led_rainbow()

    # ---- Diags only.  Check for received data and print it
    c_log("\nCheck for received data and print it.")
    data = s.recv(128)
    c_log(data)
    c_log("Data received: " + str(binascii.hexlify(data)))

    # ---- And now close the socket gracefully
    c_log("\nClosing socket.")
    s.close()

    # ---- And all is completed gracefully so deep sleep now.
    c_log("\nPreparing to hibernate because processing has completed successfully.")
    go_hibernate(0)

go_hibernate(0)


# ---- If deep sleep works properly, we never execute this.
time.sleep(5)
c_log("---------- All finished -----------\r\n\n\n")
