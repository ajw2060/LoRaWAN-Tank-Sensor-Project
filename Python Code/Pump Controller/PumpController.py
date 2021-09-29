

# This script will do the following
# - monitor the various GPIO on the Pi for changes and act accordingly


# Changes
# 2020-10-24    Initial version.  This was added under Jupyter.
# 2020-10-31    Added operation mode feature for manual/semi/auto modes receivable via MQTT.
# 2020-11-05    Added subscriber for tank level data via MQTT.
# 2021-07-01    Added better error handler to received MQTT message for tank water level messages.
# 2021-07-18	Added log rotation.
# 2021-07-21    Added tank data keys to status dictionary so this gets reported in status updates also.
# 2021-07-27    Added more logging to pump start/stop processing in automatic mode (to show variables at entry)
# 2021-07-27    Added 'pump turn off' processing in automatic mode.
# 2021-07-28    Simplified logging around receipt of command messages.

from gpiozero import Button# import button from the Pi GPIO library
#from gpiozero import DigitalOutputDevice
#from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice
from gpiozero import CPUTemperature

from ina219 import INA219
from ina219 import DeviceRangeError

import time

import os # imports OS library for Shutdown control
import logging
import logging.handlers
import platform
import sys
from signal import pause
import yaml
import json
import paho.mqtt.client as mqtt
import pprint

import datetime
import threading
import schedule

import smbus

#import socket
#import asyncio



# ---- Define the GPIO pins used by each sense or control line
# The shutdown_button on GPIO7 (Pin 26) is not initialised here as it is used in the separate shutdown script.
phase1_present_sense = Button(16)       #Pin 36
phase2_present_sense = Button(17)       #Pin 11
phase3_present_sense = Button(18)       #Pin 12

pump_running_sense = Button(24)         #Pin 18
pump_fault_sense = Button(25)           #Pin 22

tamper_switch_sense = Button(4)         #Pin 7
fronius_digital1_sense = Button(8)      #Pin 24
fronius_digital2_sense = Button(9)      #Pin 21
fronius_digital3_sense = Button(10)     #Pin 19
fronius_digital4_sense = Button(11)     #Pin 23

pump_start_pulse = OutputDevice(22, active_high=True, initial_value=False, pin_factory=None)       #Pin 15
pump_stop_pulse = OutputDevice(23, active_high=True, initial_value=False, pin_factory=None)        #Pin 16



# ---- Scheduling timers
# next_run_hourly = time.time()
# run_interval_hourly = 3600              # To schedule things every hour (but not necessarily on the hour)


# ---------- Configuration load from YAML -----------------------------------------------------------------------------
def yaml_loader(filepath):
    try:
        with open(filepath, "r") as file_descriptor:
            config_data = yaml.load(file_descriptor, Loader=yaml.FullLoader)    # Should avoid the unsafe warning
        return config_data
    except:
        print(f"ERROR 5.  Unable to open the YAML configuration file at {filepath}.")
        exit(5)


# ---------- Get the temperature and humidity from the SHT31 sensor ---------------------------------------------------
def getEnclosureTempHumi():
    #print("Getting enclosure temperature and humidity from SHT31 sensor.")
    # Get I2C bus
    bus = smbus.SMBus(1)

    # SHT31 address, 0x44(68)
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    time.sleep(0.5)

    # SHT31 address, 0x44(68)
    # Read data back from 0x00(00), 6 bytes
    # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
    data = bus.read_i2c_block_data(0x44, 0x00, 6)

    # Convert the data
    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    # Print the results
    #print("..SHT31 Temperature : %.1f C" %cTemp)
    #print("..SHT31 Humidity    : %.0f %%RH" %humidity)

    # And stuff these into the dictionary
    system_status['environment_state']['enclosure_temperature'] = format(cTemp,'.1f')
    system_status['environment_state']['enclosure_humidity'] = format(humidity,'.0f')


# ---- Get system uptime ----------------------------------------------------------------------------------------------
def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)


# ---------- Get Raspberry Pi CPU Temperature -------------------------------------------------------------------------
def getCpuTemperature():
    #print("Getting CPU temperature from Raspberry Pi CPU.")
    cpu = CPUTemperature()
    #print('..CPU  temperature  : {}C'.format(cpu.temperature))
    # And stuff it into the dictionary
    system_status['environment_state']['cpu_temperature'] = format(cpu.temperature,'.1f')


# ---------- Publish a generic environmental alarm --------------------------------------------------------------------
def publishEnvironmentAlarm(alarmNumber, alarmState):
    # This will ultimately publish an environment alarm
    #print("XXXXXXXXX - Environment alarm publish stub.  Alarm No=[" + str(alarmNumber) + "].  Alarm State =[" + str(alarmState) +"]")
    '''
        Received parameters are as follows.
        alarmNumber = alarm number
        alarmState.  1=New alarm.  0=Cleared alarm.
    '''
    logger.debug("Publish the alarm message.")

    publish_generic_message('Alarm Condition Detected', topic_pump_status, system_status)


# ---------- Now check if we have any alarm conditions present that need to be reported -------------------------------
def checkForAlarms():
    logger.debug('Running a check of all environment conditions (temp, humidity, sensors, etc) now.')
    '''
        There are many possible alarm conditions to inspect.
        Each one is done individually and a message is published for fresh alarms and cleared alarms (but not for ongoing alarms).
        '''
    checkAlarm01()      # Enclosure temperature
    checkAlarm02()      # Enclosure humidity
    checkAlarm03()      # CPU Temperature
    checkAlarm04()      # Still receiving updates from water level sensor
    checkAlarm05()      # Battery voltage
    checkAlarm06()      # Battery is not discharging


# ---------- Alarm check 01 - Enclosure over temperature --------------------------------------------------------------
def checkAlarm01():
    #logger.debug('.Alarm check 01 - Check for enclosure over-temperature alarm.')
    global enclosure_temp_alarm_base_value
    global enclosure_temp_alarm_recovery_value
    global enclosure_temp_alarm_working_value

    if float(system_status['environment_state']['enclosure_temperature']) < enclosure_temp_alarm_working_value and not system_status['alarms']['enclosure_overtemperature']:
        # All good and nothing to do
        #logger.debug(f"..NORMAL.  Enclosure temperature [{float(system_status['environment_state']['enclosure_temperature']):.1f}] is below threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
        pass

    elif float(system_status['environment_state']['enclosure_temperature']) >= enclosure_temp_alarm_working_value and not system_status['alarms']['enclosure_overtemperature']:
        # This is a fresh over temperature alarm.  Set the enclosure over-temp alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  Enclosure temperature [{float(system_status['environment_state']['enclosure_temperature']):.1f}] is at or above threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
        system_status['alarms']['enclosure_overtemperature'] = True
        publishEnvironmentAlarm(1,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the over-temp alarm threshold from [{enclosure_temp_alarm_working_value:.1f}] to [{enclosure_temp_alarm_recovery_value:.1f}].")
        enclosure_temp_alarm_working_value = enclosure_temp_alarm_recovery_value

    elif float(system_status['environment_state']['enclosure_temperature']) >= enclosure_temp_alarm_working_value and system_status['alarms']['enclosure_overtemperature']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  Enclosure temperature [{float(system_status['environment_state']['enclosure_temperature']):.1f}] remains above threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")

    elif float(system_status['environment_state']['enclosure_temperature']) < enclosure_temp_alarm_working_value and system_status['alarms']['enclosure_overtemperature']:
        # This is the recovery of an ongoing alarm.  Clear the enclosure over-temp alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  Enclosure temperature [{float(system_status['environment_state']['enclosure_temperature']):.1f}] is now below threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
        system_status['alarms']['enclosure_overtemperature'] = False
        publishEnvironmentAlarm(1,0)
        # Restore threshold temperature.
        logger.debug(f"..Hysterisis restoring the over-temp alarm threshold from [{enclosure_temp_alarm_working_value:.1f}] to [{enclosure_temp_alarm_base_value:.1f}].")
        enclosure_temp_alarm_working_value = enclosure_temp_alarm_base_value

    else:
        #logging.error("ERROR 101.  Problem with interrogating enclosure temperature.")
        print("ERROR 101.  Problem with interrogating enclosure temperature.")


# ---------- Alarm check 02 - Enclosure over humidity -----------------------------------------------------------------
def checkAlarm02():
    #logger.debug('.Alarm check 02 - Check for enclosure over-humidity alarm.')
    global enclosure_humidity_alarm_base_value
    global enclosure_humidity_alarm_recovery_value
    global enclosure_humidity_alarm_working_value

    if float(system_status['environment_state']['enclosure_humidity']) < enclosure_humidity_alarm_working_value and not system_status['alarms']['enclosure_overhumidity']:
        # All good and nothing to do
        #logger.debug(f"..NORMAL.  Enclosure humidity [{float(system_status['environment_state']['enclosure_humidity']):.0f}] is below threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")
        pass

    elif float(system_status['environment_state']['enclosure_humidity']) >= enclosure_humidity_alarm_working_value and not system_status['alarms']['enclosure_overhumidity']:
        # This is a fresh over humidity alarm.  Set the enclosure over-humidity alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  Enclosure humidity [{float(system_status['environment_state']['enclosure_humidity']):.1f}] is at or above threshold of [{float(enclosure_humidity_alarm_working_value):.1f}].")
        system_status['alarms']['enclosure_overhumidity'] = True
        publishEnvironmentAlarm(2,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the over-humidity alarm threshold from [{enclosure_humidity_alarm_working_value:.0f}] to [{enclosure_humidity_alarm_recovery_value:.0f}].")
        enclosure_humidity_alarm_working_value = enclosure_humidity_alarm_recovery_value

    elif float(system_status['environment_state']['enclosure_humidity']) >= enclosure_humidity_alarm_working_value and system_status['alarms']['enclosure_overhumidity']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  Enclosure humidity [{float(system_status['environment_state']['enclosure_humidity']):.0f}] remains above threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")

    elif float(system_status['environment_state']['enclosure_humidity']) < enclosure_humidity_alarm_working_value and system_status['alarms']['enclosure_overhumidity']:
        # This is the recovery of an ongoing alarm.  Clear the enclosure over-humidity alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  Enclosure humidity [{float(system_status['environment_state']['enclosure_humidity']):.0f}] is now below threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")
        system_status['alarms']['enclosure_overhumidity'] = False
        publishEnvironmentAlarm(2,0)
        # Restore threshold humidity.
        logger.debug(f"..Hysterisis restoring the over-humidity alarm threshold from [{enclosure_humidity_alarm_working_value:.0f}] to [{enclosure_humidity_alarm_base_value:.0f}].")
        enclosure_humidity_alarm_working_value = enclosure_humidity_alarm_base_value

    else:
        logger.error("ERROR 201.  Problem with interrogating enclosure humidity.")


# ---------- Alarm check 03 - CPU over temperature --------------------------------------------------------------------
def checkAlarm03():
    #logger.debug('.Alarm check 03 - Check for CPU over-temperature alarm.')
    global cpu_temp_alarm_base_value
    global cpu_temp_alarm_recovery_value
    global cpu_temp_alarm_working_value

    if float(system_status['environment_state']['cpu_temperature']) < cpu_temp_alarm_working_value and not system_status['alarms']['cpu_overtemperature']:
        # All good and nothing to do
        #logger.debug(f"..NORMAL.  CPU temperature [{float(system_status['environment_state']['cpu_temperature']):.1f}] is below threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
        pass

    elif float(system_status['environment_state']['cpu_temperature']) >= cpu_temp_alarm_working_value and not system_status['alarms']['cpu_overtemperature']:
        # This is a fresh over temperature alarm.  Set the cpu over-temp alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  CPU temperature [{float(system_status['environment_state']['cpu_temperature']):.1f}] is at or above threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
        system_status['alarms']['cpu_overtemperature'] = True
        publishEnvironmentAlarm(3,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the CPU over-temp alarm threshold from [{cpu_temp_alarm_working_value:.1f}] to [{cpu_temp_alarm_recovery_value:.1f}].")
        cpu_temp_alarm_working_value = cpu_temp_alarm_recovery_value

    elif float(system_status['environment_state']['cpu_temperature']) >= cpu_temp_alarm_working_value and system_status['alarms']['cpu_overtemperature']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  CPU temperature [{float(system_status['environment_state']['cpu_temperature']):.1f}] remains above threshold of [{float(cpu_temp_alarm_working_value):.1f}].")

    elif float(system_status['environment_state']['cpu_temperature']) < cpu_temp_alarm_working_value and system_status['alarms']['cpu_overtemperature']:
        # This is the recovery of an ongoing alarm.  Clear the cpu over-temp alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  CPU temperature [{float(system_status['environment_state']['cpu_temperature']):.1f}] is now below threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
        system_status['alarms']['cpu_overtemperature'] = False
        publishEnvironmentAlarm(3,0)
        # Restore threshold temperature.
        logger.debug(f"..Hysterisis restoring the CPU over-temp alarm threshold from [{cpu_temp_alarm_working_value:.1f}] to [{cpu_temp_alarm_base_value:.1f}].")
        cpu_temp_alarm_working_value = cpu_temp_alarm_base_value

    else:
        logger.error("ERROR 302.  Problem with interrogating CPU temperature.")


# ---------- Alarm check 04 - Confirm we are still recieving live updates from the water level sensor -----------------
def checkAlarm04():
    global tank_waterlevel_maximum_age
    #logger.debug(f".Alarm check 04 - Check that level sensor updates received (at worst) every [{float(tank_waterlevel_maximum_age)/3600:.2f}] hours.")

    if time.time() - float(tank_water_status['tank_waterlevel_lastupdate']) < tank_waterlevel_maximum_age and not system_status['alarms']['water_level_sensor_offline']:
        # All good - must have received a recent water level update.
        #logger.debug(f"..NORMAL.  Time since last update [{(time.time() - float(tank_water_status['tank_waterlevel_lastupdate']))/3600:.2f}] hours.")
        pass

    elif  time.time() - float(tank_water_status['tank_waterlevel_lastupdate']) >= tank_waterlevel_maximum_age and not system_status['alarms']['water_level_sensor_offline']:
        # This is a fresh alarm.  The sensor must have recently stopped sending updates.
        logger.debug(f"..NEW ALARM.  Sensor has gone offline.  Time since last update [{(time.time() - float(tank_water_status['tank_waterlevel_lastupdate']))/3600:.2f}] hours.")
        system_status['alarms']['water_level_sensor_offline'] = True
        publishEnvironmentAlarm(4,1)

    elif time.time() - float(tank_water_status['tank_waterlevel_lastupdate']) >= tank_waterlevel_maximum_age and system_status['alarms']['water_level_sensor_offline']:
        # This is a continuing alarm.  Sensor remains offline.
        logger.debug(f"..CONTINUED ALARM.  Sensor remains offline.  Time since last update [{(time.time() - float(tank_water_status['tank_waterlevel_lastupdate']))/3600:.2f}] hours.")

    elif time.time() - float(tank_water_status['tank_waterlevel_lastupdate']) < tank_waterlevel_maximum_age and system_status['alarms']['water_level_sensor_offline']:
        # This is the recovery of the alarm.  Sensor has started sending water level updates again.
        logger.debug(f"..CLEARED ALARM.  Sensor back online.  Time since last update [{(time.time() - float(tank_water_status['tank_waterlevel_lastupdate']))/3600:.2f}] hours.")
        system_status['alarms']['water_level_sensor_offline'] = False
        publishEnvironmentAlarm(4,0)


# ---------- Alarm check 05 - Confirm the battery level is above threshold --------------------------------------------
def checkAlarm05():
    global battery_low_voltage_alarm_base_value
    global battery_low_voltage_alarm_recovery_value
    global battery_low_voltage_alarm_working_value

    #logger.debug(f".Alarm check 05 - Check if the battery voltage is above the threshold of [{battery_low_voltage_alarm_base_value}] volts.")
    #decorativeStatusDumper("Alarm 05")
    if system_status['power']['battery_voltage'] > battery_low_voltage_alarm_working_value and not system_status['alarms']['battery_low'] :
        # All good - battery is fine
        #logger.debug(f"..NORMAL.  Battery voltage [{system_status['power']['battery_voltage']}] is above threshold of [{battery_low_voltage_alarm_base_value}].")
        pass

    elif system_status['power']['battery_voltage'] <= battery_low_voltage_alarm_working_value and not system_status['alarms']['battery_low']:
        # Battery low has just been detected
        system_status['alarms']['battery_low'] = True
        logger.debug(f"..NEW ALARM.  Battery voltage of [{system_status['power']['battery_voltage']}] is at or below threshold of [{battery_low_voltage_alarm_working_value}] volts.")
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis raising the low battery alarm threshold from [{battery_low_voltage_alarm_working_value:.1f}] to [{battery_low_voltage_alarm_recovery_value:.1f}].")
        battery_low_voltage_alarm_working_value = battery_low_voltage_alarm_recovery_value
        publishEnvironmentAlarm(5,1)

    elif system_status['power']['battery_voltage'] <= battery_low_voltage_alarm_working_value and system_status['alarms']['battery_low']:
        # Stale low battery alarm
        logger.debug(f"..CONTINUED ALARM.  Battery voltage now at [{system_status['power']['battery_voltage']}].  Battery is still going flat.")

    elif system_status['power']['battery_voltage'] > battery_low_voltage_alarm_working_value and system_status['alarms']['battery_low']:
        # Battery voltage has recovered so restore the threshold and clear the alarm flag
        logger.debug(f"..CLEARED ALARM.  Battery voltage of [{system_status['power']['battery_voltage']}] has recovered to be above [{battery_low_voltage_alarm_working_value}].")
        # Restore threshold value.
        logger.debug(f"..Hysterisis restoring the low battery alarm threshold from [{battery_low_voltage_alarm_working_value:.1f}] to [{battery_low_voltage_alarm_base_value:.1f}].")
        battery_low_voltage_alarm_working_value = battery_low_voltage_alarm_base_value
        # Clear the alarm flag
        system_status['alarms']['battery_low'] = False
        publishEnvironmentAlarm(5,0)

    else:
        logger.error("ERROR 105.  Problem with interrogating battery voltage.")
        print("ERROR 105.  Problem with interrogating battery voltage.")


# ---------- Alarm check 06 - Confirm the battery is not discharging --------------------------------------------------
def checkAlarm06():
    #logger.debug(f".Alarm check 06 - Check if the battery is discharging.")
    #decorativeStatusDumper("Before Alarm 06 check")
    # The battery current value of 50 is chosen because the INA219 does not seem to be completely accurate so give it a big threshold.
    pass

    if system_status['power']['battery_current'] < 0 and not system_status['alarms']['battery_discharging']:
        # All good - battery is charging (negative current means charge and positive means discharge)
        #logger.debug(f"..NORMAL.  Battery current of [{system_status['power']['battery_current']}] indicates battery is charging normally.")
        pass
    
    elif system_status['power']['battery_current'] > 50 and not system_status['alarms']['battery_discharging']:
        # Battery discharging condition has just been detected
        logger.debug(f"..NEW ALARM.  Battery current of [{system_status['power']['battery_current']}] indicates battery is discharging.")
        system_status['alarms']['battery_discharging'] = True
        publishEnvironmentAlarm(6,1)

    elif system_status['power']['battery_current'] > 50 and system_status['alarms']['battery_discharging']:
        # Battery is still discharging
        logger.debug(f"..CONTINUED ALARM.  Battery current of [{system_status['power']['battery_current']}] indicates battery is still discharging.")

    elif system_status['power']['battery_current'] < 0 and system_status['alarms']['battery_discharging']:
        # Battery just started to recharge.  Possibly the AC power has recovered.
        logger.debug(f"..CLEARED ALARM.  Battery current of [{system_status['power']['battery_current']}] indicates battery is recharging.")
        system_status['alarms']['battery_discharging'] = False
        publishEnvironmentAlarm(6,0)

    else:
        logger.debug(f"..ERROR.  Possible battery fault.  Battery current of [{system_status['power']['battery_current']}]  Is Discharging Flag[{system_status['alarms']['battery_discharging']}].")


# ---------- These are the jobs managed by the schedule module --------------------------------------------------------
def jobHourlyHousekeeping():
    # This is intended to run every hour on the hour for simple housekeeping
    logger.debug("=== Starting 'On the Hour' scheduled housekeeping tasks.")
    publish_generic_message('Hourly report', topic_pump_status, system_status)
    logger.debug("=== Completed 'On the Hour' scheduled housekeeping tasks.")


def jobRegularHousekeeping():
    # This is intended to run every fitteen minutes or so to monotor tank level and inverter state and possibly turn the pump on or off
    logger.debug("--- Quarter hourly scheduled housekeeping starting.")
    pump_action_checker("Scheduled")
    logger.debug("--- Quarter hourly scheduled tasks completed.")


def jobMinuteHousekeeping():
    # This is intended to run every minute to check for temperature alarms
    # print("Every minute jobs will now run.")

    getEnclosureTempHumi()
    getCpuTemperature()
    readPowerValues("Every Minute")

    #decorativeStatusDumper("Minute")
    checkForAlarms()


# ---------- State change functions -----------------------------------------------------------------------------------
# These could probably be optimised by grabbing the object that fired the callback but it looks hard to parse
def phase1_lost():
    logger.debug("ISR. Phase 1 has been lost.")
    system_status['power_state']['phase1_present'] = phase1_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def phase1_restored():
    logger.debug("ISR. Phase 1 has been restored.")
    system_status['power_state']['phase1_present'] = phase1_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def phase2_lost():
    logger.debug("ISR. Phase 2 has been lost.")
    system_status['power_state']['phase2_present'] = phase2_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def phase2_restored():
    logger.debug("ISR. Phase 2 has been restored.")
    system_status['power_state']['phase2_present'] = phase2_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def phase3_lost():
    logger.debug("ISR. Phase 3 has been lost.")
    system_status['power_state']['phase3_present'] = phase3_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def phase3_restored():
    logger.debug("ISR. Phase 3 has been restored.")
    system_status['power_state']['phase3_present'] = phase3_present_sense.value
    system_status['environment_state']['change_detected'] = 1
    #print(system_status)

def pump_running():
    logger.debug("ISR. Pump has just started.")
    system_status['pump_run_state']['pump_running'] = pump_running_sense.value
    system_status['environment_state']['change_detected'] = 1

def pump_stopped():
    logger.debug("ISR. Pump has just stopped.")
    system_status['pump_run_state']['pump_running'] = pump_running_sense.value
    system_status['environment_state']['change_detected'] = 1

def pump_fault_detected():
    logger.debug("ISR. Pump fault has just been detected.")
    system_status['pump_run_state']['pump_fault'] = pump_fault_sense.value
    system_status['environment_state']['change_detected'] = 1

def pump_fault_cleared():
    logger.debug("ISR. Pump fault has just cleared.")
    system_status['pump_run_state']['pump_fault'] = pump_fault_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_1_active():
    logger.debug("ISR. Fronius digital 1 has just been enabled.")
    system_status['fronius_state']['fronius_1'] = fronius_digital1_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_1_inactive():
    logger.debug("ISR. Fronius digital 1 has just been disabled.")
    system_status['fronius_state']['fronius_1'] = fronius_digital1_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_2_active():
    logger.debug("ISR. Fronius digital 2 has just been enabled.")
    system_status['fronius_state']['fronius_2'] = fronius_digital2_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_2_inactive():
    logger.debug("ISR. Fronius digital 2 has just been disabled.")
    system_status['fronius_state']['fronius_2'] = fronius_digital2_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_3_active():
    logger.debug("ISR. Fronius digital 3 has just been enabled.")
    system_status['fronius_state']['fronius_3'] = fronius_digital3_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_3_inactive():
    logger.debug("ISR. Fronius digital 3 has just been disabled.")
    system_status['fronius_state']['fronius_3'] = fronius_digital3_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_4_active():
    logger.debug("ISR. Fronius digital 4 has just been enabled.")
    system_status['fronius_state']['fronius_4'] = fronius_digital4_sense.value
    system_status['environment_state']['change_detected'] = 1

def fronius_4_inactive():
    logger.debug("ISR. Fronius digital 4 has just been disabled.")
    system_status['fronius_state']['fronius_4'] = fronius_digital4_sense.value
    system_status['environment_state']['change_detected'] = 1



# --01-------- The connection acknowledgement callback ----------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    logger.debug("..ON-CONNECT callback processing.")
    if rc == 0:
        logger.debug("..Connected to broker = [" + str(rc) + "] and UserData = [" + str(userdata) + "]")
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
        # Publish a NULL message to a couple topics which have retained flag set just
        # to clear out garbage when this script restarts
        # Probably not needed, but seems like good practice

        logger.debug("..Publish NULL message to any possible previously retained topics.")
        client.publish(topic_pump_status, None, 1, retain=True)        # Receipt of an empty status message currently breaks the remote switch code.  TODO
        client.publish(topic_pump_lwt, None, 1, retain=True)

        logger.debug("..Subscribing to various topics.")

        logger.debug("..Subscribe to cmd topic ......................... [" + topic_pump_cmd + "]")
        client.subscribe(topic_pump_cmd)

        logger.debug("..Subscribe to water level messages topic ........ [" + topic_tank_waterlevel + "]")
        client.subscribe(topic_tank_waterlevel)

        client.connected_flag = True

        # Check if Home Assistant needs to be advised
        if data['home_assistant_configuration']['ha_announce_on_start']:
            logger.info(f"Announcement to Home Assistant on topic [{data['home_assistant_configuration']['ha_announce_topic']}].")
            x = client.publish(data['home_assistant_configuration']['ha_announce_topic'], payload=json.dumps(data['home_assistant_configuration']['ha_config_data']), qos=0, retain=False)
            logger.debug("..HA publish announce result = " + str(x))   

            x = client.publish(data['home_assistant_configuration']['ha_available_topic'], payload="online", qos=0, retain=False)
            logger.debug("..HA publish available result = " + str(x))   


    else:
        logging.error("ERROR.  Client ON-CONNECT has failed")


# --02-------- The disconnect callback --------------------------------------------------------------------------------
def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")
    if rc != 0:
        logging.error(
            "ERROR.  Unexpected disconnection from broker.  RC [" + str(rc) + "].  Userdata [" + str(userdata) + "]")


# --03-------- The callback when the broker has acknowledged the subscription -----------------------------------------
def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("...Subscription confirmed.  Mid= " + str(mid) + "  Granted QoS= " + str(granted_qos))


# --04-------- The callback for when a message is received from the broker --------------------------------------------
def on_message(client, userdata, msg):
    logger.debug("======> New message received from broker.")
    logger.debug("..Message Topic:    [" + str(msg.topic) + "]")
    logger.debug("..Retained Flag:    [" + str(msg.retain) + "]")
    received_message_payload = msg.payload.decode("utf-8")

    # Acknowledge the received message regardless of the type of message.
    logger.debug('..Acknowledging received message.')
    cmd_ack_message_payload = dict([('stationid',''), ('receivedtopic',''), ('receivedmessage','')])
    cmd_ack_message_payload['stationid'] = local_station_name
    cmd_ack_message_payload['receivedtopic'] = str(msg.topic)
    cmd_ack_message_payload['receivedmessage'] = received_message_payload
    x = client.publish(topic_pump_cmdack, str(cmd_ack_message_payload), 0, False)
    logger.debug("..CMD ACK publish result = " + str(x))

    # Determine the message type and handle each message type appropriately.
    logger.debug("Now attempting to parse the received message.")

    if (str(msg.topic) == topic_pump_cmd):                                      # Pump control command
        logger.debug("..This is a 'command' message.")
        #logger.debug("..Message Payload: " + "[" + received_message_payload + "]")

        '''
        The following command codes are recognised
            0 = turn off the pump
            1 = turn on the pump
            2 = issue an immediate status update
            7 = switch to manual mode
            8 = switch to semi-automatic mode
            9 = switch to automatic mode
        '''
        try:
            temp_dict = json.loads(received_message_payload)

            if temp_dict['command_code'] == 0:          # Turn off
                logger.debug(f"..Requested command code [{temp_dict['command_code']}] is [{command_code_lookup[temp_dict['command_code']]}].")
                pump_handler_turnoff(True, "MQTT off message")

            elif temp_dict['command_code'] == 1:        # Turn on
                logger.debug(f"..Requested command code [{temp_dict['command_code']}] is [{command_code_lookup[temp_dict['command_code']]}].")
                pump_handler_turnon(True, "MQTT on message")

            elif temp_dict['command_code'] == 2:        # Send status update
                publish_generic_message("Solicited", topic_pump_status, system_status)

            elif temp_dict['command_code'] == 7:        # Switch to manual mode
                logger.debug(f"..Requested command code [{temp_dict['command_code']}] is [{command_code_lookup[temp_dict['command_code']]}].")
                system_status['controller_run_state']['run_mode'] = 1
                system_status['controller_run_state']['run_mode_changed_by'] = 'MQTT Message'
                system_status['controller_run_state']['run_mode_command_source'] = temp_dict['command_source']
                system_status['controller_run_state']['run_mode_changed_time'] = int(time.time())
                system_status['environment_state']['change_detected'] = 1

            elif temp_dict['command_code'] == 8:        # Switch to semi-automatic mode
                logger.debug(f"..Requested command code [{temp_dict['command_code']}] is [{command_code_lookup[temp_dict['command_code']]}].")
                system_status['controller_run_state']['run_mode'] = 2
                system_status['controller_run_state']['run_mode_changed_by'] = 'MQTT Message'
                system_status['controller_run_state']['run_mode_command_source'] = temp_dict['command_source']
                system_status['controller_run_state']['run_mode_changed_time'] = int(time.time())
                system_status['environment_state']['change_detected'] = 1

            elif temp_dict['command_code'] == 9:        # Switch to automatic mode
                logger.debug(f"..Requested command code [{temp_dict['command_code']}] is [{command_code_lookup[temp_dict['command_code']]}].")
                system_status['controller_run_state']['run_mode'] = 3
                system_status['controller_run_state']['run_mode_changed_by'] = 'MQTT Message'
                system_status['controller_run_state']['run_mode_command_source'] = temp_dict['command_source']
                system_status['controller_run_state']['run_mode_changed_time'] = int(time.time())
                system_status['environment_state']['change_detected'] = 1

            else:
                logger.debug("An unknown command code was received so it has been ignored.")
        
        
        except:
            logger.error("ERROR 300.  Unable to load JSON received command.  See payload below.")
            logger.error(received_message_payload)
            #exit(300)

        try:
            logger.debug(f"..Command source [{temp_dict['command_source']}]")
            logger.debug(f"..Command code   [{temp_dict['command_code']}]")
        except:
            logger.error("ERROR 301.  Unable to parse received JSON message.  See message payload below. ")
            logger.error(received_message_payload)
            #schedule.clear()
            #sys.exit("ERROR 301 happened.")
            


    elif (str(msg.topic) == topic_tank_waterlevel):                             # Tank water level update
        logger.debug("..Message Type:    [Update to water level in monitored tank]")
        logger.debug("..Message Payload: " + "[" + received_message_payload + "]")
        # This message is JSON, so convert to a dict so we can extract elements
        try:
            tank_info_update_data = json.loads(received_message_payload)
            tank_water_status['tank_name'] = tank_info_update_data['tank_id']
            tank_water_status['tank_waterlevel'] = tank_info_update_data['tank_water_level']
            tank_water_status['tank_waterlevel_lastupdate'] = format(time.time(), '.0f')
            # Also pop it into the system_status dictionary (as a precursor to obsoleting the separate tank data dict)
            system_status['tank_status']['tank_name'] = tank_info_update_data['tank_id']
            system_status['tank_status']['tank_waterlevel'] = tank_info_update_data['tank_water_level']
            system_status['tank_status']['tank_waterlevel_lastupdate'] = int(time.time())

            logger.debug(f"Water level in [{tank_info_update_data['tank_id']}] updated to [{tank_info_update_data['tank_water_level']}].")
        except:
            logger.error(f'ERROR 222. Cannot parse received dictionary.  {sys.exc_info()[0]}')
    else:
        logger.error("Message received on unrecognised topic.")      # This should never happen as we only subscribe to selected topics anyway.


# --05-------- The MQTT logging callback ------------------------------------------------------------------------------
def on_log(client, userdata, level, buf):
    print("log: ", buf)



# --06-------- Generic message publisher ------------------------------------------------------------------------------
def publish_generic_message(arg_reason, topic_to_publish, dict_to_publish):
    # This is intended as the central pont for publishing all status reports and command acknowledgements.
    # The timestamp and requester are inserted here just before publishing.
    # Mostly the request is to publish system_status, but even if not, we still update the calculated
    # fields in system_status.  Probably a smarter way to do this, but meh.


    logger.debug(f"Publishing on topic [{topic_to_publish}] as requested by [{arg_reason}].")
    # print(dict_to_publish)

    # Update the details in both of these dictionaries.  This is a bit more effort but no real consequence.
    logger.debug("..Calculating and inserting dynamic data into 'system_status' dictionary ready for publishing.")
    system_status['controller_run_state']['publish_timestamp'] = int(time.time())
    system_status['controller_run_state']['publish_requester'] = arg_reason
    system_status['controller_details']['system_uptime'] = get_system_uptime()
    system_status['controller_details']['script_uptime'] = int(time.time()) - system_status['controller_details']['script_starttime']
    system_status['tank_status']['tank_waterlevel_age'] = int(time.time()) - system_status['tank_status']['tank_waterlevel_lastupdate']

    cmd_response_message['publish_timestamp'] = int(time.time())
    cmd_response_message['publish_requester'] = arg_reason

    x = client.publish(topic_to_publish, payload=json.dumps(dict_to_publish), qos=0, retain=False)
    logger.debug("..Generic publish result = " + str(x))




# ---------- Pump Turn ON function ------------------------------------------------------------------------------------
def pump_handler_turnon(publish_response, ool_arg_command_source):
    '''
    These 'turn on' and 'turn off' requests can originate from the following.
        a) The function called from the MQTT message parser, so all the MQTT responses need to be forwarded.
        b) The function called from the local pump action checker so no response messaging is needed.

    If it is called with publish_response set to True, then a message is published, otherwise nothing is published.

    Regardless of the source of the command, most of the same preparatory checks need to be completed before turning 
    the pump on or off. If the command came from MQTT then the response needs to be published, but 
    if the command is local, no MQTT response is needed.  So the CMD RESP messages are only sent if this is called
    by a MQTT action.
    (Considered having this system publish the ON or OFF message to itself so there was only one message source
    but this means it would not operate without the broker so that idea was shelved.)

    Possible response codes to the following ON/OFF messages are as follows
      00 - Command executed successfully (well the appropriate relay was operated anyway)
      21 - Pump is already turned on so no action is required
      22 - One (or more) of the AC phases is missing so cannot turn on the pump
      23 - Pump is in fault condition
      31 - Pump is already turned off so no action is required
    '''

    logger.debug("Processing a pump turn ON request Type " + "[" + str(ool_arg_command_source) + "]")


    bool_pump_clear_to_start = True        # Overall flag to control start readiness - assume OK unless told otherwise
    problem_counter_pumpstart = 0          # Increment this each time we find a problem preventing a pump start

    # Prepare the response message (regardless of whether it gets sent or not)
    cmd_response_message['received_command'] = 'ON'

    # Do the negative logic checks before trying to turn the pump on
    logger.debug("PRESTART Check 1 - Confirm the pump is not already running.")
    if system_status['pump_run_state']['pump_running']:                               #Check pump is not already running
        #print("Pump seems to be already turned on so command is ignored.")
        logger.debug("..Pump is already running so no further action will be taken.")
        bool_pump_clear_to_start = False
        problem_counter_pumpstart =+ 1
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '21'
            cmd_response_message['response_message'] = 'Pump is already running so the [start] command is ignored.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)
    else:
        logger.debug("..Pump is not already running so it may be possible to start it.")

    logger.debug("PRESTART Check 2 - Confirm that all AC phases are present.")
    if not system_status['power_state']['phase1_present'] or not system_status['power_state']['phase2_present'] or not system_status['power_state']['phase3_present']:         #Check all the AC is avaiulable
        #print("At least one of the AC Phases is missing so command is ignored.")
        logger.debug("..At least one AC phase is missing.")
        bool_pump_clear_to_start = False
        problem_counter_pumpstart =+ 1
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '22'
            cmd_response_message['response_message'] = 'At least one of the AC Phases is missing so the [start] command is ignored.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)
    else:
        logger.debug("..All AC Power phases are available.")

    logger.debug("PRESTART Check 3 - Confrm that the pump is not in FAULT condition.")
    if system_status['pump_run_state']['pump_fault']:     #Check the pump is not in fault condition
        #print("Pump is in FAULT coindition so command is ignored.")
        logger.debug("..Pump is in FAULT condition.")
        bool_pump_clear_to_start = False
        problem_counter_pumpstart =+ 1
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '23'
            cmd_response_message['response_message'] = 'Pump is in FAULT condtion so the [start] command is ignored.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)
    else:
        logger.debug("..Pump is not in FAULT condition.")

    if bool_pump_clear_to_start:
        logger.debug("PRESTART Complete.  All conditions are good for a pump start.")
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '00'
            cmd_response_message['response_message'] = 'Clear for pump start.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)

        # So now push the virtual start button                        # Here is where the work happens!
        logger.debug('Pulsing the pump start relay now.')
        pump_start_pulse.on()
        time.sleep(0.7)
        pump_start_pulse.off()
        logger.debug('..Start pulse is complete.  The pump should now be running so expect a status change.'  )
    else:
        logger.debug(f"Detected [{str(problem_counter_pumpstart)}] of the preceding conditions so start request has been ignored.")


# ---------- Pump Turn OFF function -----------------------------------------------------------------------------------
def pump_handler_turnoff(publish_response, ool_arg_command_source):

    logger.debug("Processing a pump turn OFF request Type " + "[" + str(ool_arg_command_source) + "]")
    if ool_arg_command_source:
        logger.debug('..Turn OFF request from MQTT message.')
    else:
        logger.debug('..Turn OFF request from local pump action checker.')

    problem_counter_pumpstop = 0            # Increment this each time we find a problem preventing a pump stop
    bool_pump_clear_to_stop = True          # Overall flag to control start readiness - assume OK unless told otherwise

    # Prepare the response message (regardless of whether it gets sent or not)
    cmd_response_message['received_command'] = 'OFF'

    # Do the negative logic checks before trying to turn the pump off (there is only one precheck for stop!)
    logger.debug("PRESTOP Check 1 - Confirm the pump in not already stopped.")
    if not system_status['pump_run_state']['pump_running']:                               #Check pump is not already stopped
        #print("Pump seems to be already turned off so command is ignored.")
        logger.debug("..Pump is already stopped so no further action is needed.")
        problem_counter_pumpstop =+ 1
        bool_pump_clear_to_stop = False
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '31'
            cmd_response_message['response_message'] = 'Pump is already stopped so [stop] command is ignored.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)
    else:
        logger.debug("..Pump is running so it may be possible to stop it.")

    if bool_pump_clear_to_stop:
        logger.debug("All conditions are good for a pump stop.")
        if publish_response:          # Publish only if MQTT was involved
            cmd_response_message['response_code'] = '00'
            cmd_response_message['response_message'] = 'Clear for pump stop.'
            publish_generic_message(ool_arg_command_source, topic_pump_cmdack, cmd_response_message)

        # So now push to stop button                        # Here is where the work happens!
        logger.debug('Pulsing the pump stop relay now.')
        pump_stop_pulse.on()
        time.sleep(0.7)
        pump_stop_pulse.off()
        logger.debug('..Stop pulse is complete.  The pump should now be stopped so expect a status change.')
    else:
        logger.debug(f"Detected [{str(problem_counter_pumpstop)}] of the preceding conditions so stop request has been ignored.")


# ---------- Periodic pump check --------------------------------------------------------------------------------------
def pump_action_checker(arg_reason):
    logger.debug("Pump tank and solar action checks initiated by [" + arg_reason + "].  Run number [" + str(system_status['environment_state']['run_sequence']) + "].")
    #logger.debug(system_status['run_state']['run_mode'])
    #decorativeStatusDumper()

    '''
        The 'pump action checker' operates as follows.
        - This check runs once at system startup (baseline run).  Some special handling happens on this first run.
        - It is then run regularly on a schedule of 15 minutes or so (schelule run).

        It is intended to assimilate all the status from the sensors and decide whether or not the pump should be
        running or stopped.

        The received parameters indicating 'Baseline' or 'Scheduled run' are decorative only.  The determination whether
        it is the initial baseline run is made using just the run number where zero indicates the baseline run.

        The intelligence for pump management is all in this module!
        Depending on the system operational mode, different rules are applied.

        1) Manual mode
            This pays no heed to water level and just allows stop and start functions to be actioned.  In this mode
            this module will do nothing.

        2) Semi automatic mode
            This pays attention to only the tank water level and the recency of the tank water level data.
            If the data is old (more than a defined period of typically two hours) then we cannot trust it so turn the pump off.
            This condition could be due to a failure of the water level sensor or the sensor reporting network.
            If the reading is recent and the tank shows full (or over the threshold) then turn the pump off.

        3) Automatic mode
            Turn off is the same as semi-automatic.
            Turn on also considers the recency of the data and will only turn on with a recent level showing tank is below threshold.

        The initial run (run 0) needs some extra special handling.
        The 'water level last updated' timestamp is set to zero when the system starts.
        If the water level timestamp is still old (epoch 0) because it has never been updated by the sensor,
        then the normal action would be to stop the pump because the water level is old and cannot be trusted.
        In semi-automatic or automatic mode this is not ideal because we may simply not have received a water
        level update yet so we allow a grace period during which the pump can continue to run (if it is in fact running).

        This grace period is enabled by setting the timestamp on the water level update to about 90 minutes in the past.
        This lets the pump continue to run in the absence of a recent water level update, but only for a constrained tme.
        The tank could actually be full at this time, but it may not matter if we run the tank over for these 90 minutes.
        This grace period will also prevent a premature 'sensor offline' alarm from being generated.
    '''

    # Check if this is run zero and if so adust that timestamp to something older then the timeout
    # This will ensure the flag is initially set to stale.
    if int(system_status['environment_state']['run_sequence']) == 0:
        amount_of_setback = tank_waterlevel_maximum_age + 60        # Adding another minute should suffice.
        logger.debug(f"..Initial run so the 'waterlevel_lastupdate' timestamp adjusted backwards by [{amount_of_setback}] seconds.")
        tank_water_status['tank_waterlevel_lastupdate'] = time.time() - amount_of_setback

    # This bit simplifies some of the variables and flags used in the subsequent checks.  These are 
    # easier to use if simplified.

    # Item 1 - figure out the three states of the tank water level.  These can be as follows.
    #  1 = below the low threshold
    #  2 = at or above low, but below high
    #  3 = at or above high
    tank_condition_code = 0
    if tank_water_status['tank_waterlevel'] < tank_threshold_low:
        tank_condition_code = 1     # Condition 1 = Critically low
    
    elif tank_water_status['tank_waterlevel'] >= tank_threshold_low and tank_water_status['tank_waterlevel'] < tank_threshold_high:
        tank_condition_code = 2     # Condition 2 = Adequate

    elif tank_water_status['tank_waterlevel'] >= tank_threshold_high:
        tank_condition_code = 3     # Condition 3 = Full
        
    # Item 2 - Create a flag here to show the freshness of the water level reading.  
    logger.debug("Determine freshness of current water level reading based on age of the reading.")
    water_level_reading_fresh = ''
    if int(time.time() - int(tank_water_status['tank_waterlevel_lastupdate'])) <= tank_waterlevel_maximum_age:
        water_level_reading_fresh = True
    else:
        water_level_reading_fresh = False

    # Item 3 - Calculate the age of the current water level reading.  This one is just decorative.
    age_of_water_level_reading_seconds = int(time.time()) - int(tank_water_status['tank_waterlevel_lastupdate'])
    age_of_water_level_reading_minutes = float(age_of_water_level_reading_seconds / 60)

    # Item 4 - Create a flag here to show the state of the Fronius 1 signal.
    fronuis1_available = ''
    if system_status['fronius_state']['fronius_1']:
        fronuis1_available = True
    else:
        fronuis1_available = False

    # Now proceed with the normal handling and check the run mode as this dictates what checks need to be done
    # Dump the status variables upon entry
    logger.debug("Current status values are as follows.")
    logger.debug(f" - Controller run mode ................... [{system_status['controller_run_state']['run_mode']}].")
    logger.debug(f" - Pump currently running (flag) ......... [{system_status['pump_run_state']['pump_running']}].")
    logger.debug(f" - Tank condition (level code) ........... [{tank_condition_code}]   Actual level [{tank_water_status['tank_waterlevel']}].")
    logger.debug(f" - Age of water level update ............. [{age_of_water_level_reading_minutes:.1f}] minutes.")
    logger.debug(f" - Water level reading fresh (flag) ...... [{water_level_reading_fresh}].")
    logger.debug(f" - Fronuis 1 state (flag) ................ [{fronuis1_available}].")
    
    # ---- Manual mode so do nothing
    if system_status['controller_run_state']['run_mode'] == 1:                     
        logger.debug("..Current controller run mode is 'manual' so no checks are needed.")

    # ---- Semi automatic mode so just check if tank is full
    elif system_status['controller_run_state']['run_mode'] == 2:                   
        logger.debug("..Current controller run mode is 'semi-automatic' so only pump 'turn off' actions are managed.")
        '''
            The possible actions in semi-automatic mode are as follows.
            a) Pump is already stopped --> no action needed.
            b) Pump is running but the grace period has expired (reading is stale) --> stop the pump.
            c) Pump is running and tank is full.  No need to check freahness of reading as we will stop the pump anyway --> stop the pump
        '''
       
        if system_status['pump_run_state']['pump_running']:                 # Pump running so proceed with subsequent checks
            logger.debug("Process pump running conditions in semi-automatic mode.")
        
            if not water_level_reading_fresh:                               # Water level reading is stale ==> turn pump off
                logger.debug("..Condition SEMI-1. Pump [RUNNING].  Level validity [STALE].")
                logger.debug(f"..Pump will now be switched off because water level reading is stale.  Actual age [{age_of_water_level_reading_minutes:.1f}] minutes.")
                pump_handler_turnoff(False, 'Pump semiauto mode checker - Unknown water level in tank (stale reading) so pump will be turned off.')

            elif tank_condition_code == 3:                                  # Tank full ==> turn off pump
                logger.debug("..Condition SEMI-2. Pump [RUNNING].  Tank level [FULL].")
                logger.debug('..Pump will now be switched off because the tank is full.')
                pump_handler_turnoff(False, 'Pump semiauto mode checker - Tank is full.')

            else:
                logger.warning("WARNING.  Condition SEMI-10.  No condition match found.  An additional condition check is probably needed here.")

        else:                                                               # Pump stopped ==> do nothing
            logger.debug("..Condition SEMI-3. Pump is not running right now so no checks are needed here.")


    # ---- Full automatic mode so check inverter power also
    elif system_status['controller_run_state']['run_mode'] == 3:
        logger.debug("..Current controller run mode is 'automatic' so 'turn on' and 'turn off' actions are managed.")
        # The 'False' in the turnon and turnoff indicates message stemmed from a local (made by the controller itself) decision.

        # This uses a nested if where we consider 'pump running' conditions followed by 'pump stopped' condtions
        # Firstly the 'pump running' conditions
        if system_status['pump_run_state']['pump_running']:
            logger.debug("Process pump running conditions in automatic mode.")

            if not water_level_reading_fresh:                                                       # Water level reading is stale ==> turn pump off  
                logger.debug("..Condition AUTO-1. Pump [RUNNING].  Level validity [STALE].")
                logger.debug(f"..Pump will now be switched off because water level reading is stale.  Age [{age_of_water_level_reading_minutes:.1f}] minutes.")
                pump_handler_turnoff(False, 'Pump auto mode checker - AUTO-1 - Unknown water level in tank (stale reading) so pump will be turned off.')
            
            elif tank_condition_code == 3:                                                          # Tank full ==> turn pump off
                logger.debug(f"..Condition AUTO-2. Pump [RUNNING].  Tank level [FULL].  Condition code: [{tank_condition_code}] .")
                logger.debug('..Pump will now be switched off because the tank is full.')
                pump_handler_turnoff(False, 'Pump auto mode checker - AUTO-2 - Tank is full.')

            elif water_level_reading_fresh and not fronuis1_available and tank_condition_code == 2: # Reading fresh + no fronius + level above critical ==> turn pump off
                logger.debug(f"..Condition AUTO-3. Pump [RUNNING].  Level validity [FRESH].  Age [{age_of_water_level_reading_minutes:.1f}] minutes old.  Actual tank condition code [{tank_condition_code}].  Fronius power [{fronuis1_available}]")
                logger.debug('..Pump will now be switched off as we have adequate water but no Fronius free power.')
                pump_handler_turnoff(False, 'Pump auto mode checker - AUTO-3 - Tank is adequate.')

            else:
                logger.warning("WARNING.  Condition AUTO-11.  No condition match found.  This is probably not good.")

        # Now the 'pump stopped' conditions
        elif not system_status['pump_run_state']['pump_running']:
            logger.debug("Process pump stopped conditions.")

            if not water_level_reading_fresh:
                logger.debug(f"..Condition AUTO-4. Reading [STALE].  Age [{age_of_water_level_reading_minutes:.1f}] minutes old.")  
                logger.debug("..As the water level reading is stale, no further checks will be performed and the pump will remain stopped.")

            else:   # Reading is fresh so continue with subsequent checks.
                logger.debug(f"..Water level reading is [FRESH] so further checks will happen.  Age [{age_of_water_level_reading_minutes:.1f}] minutes old.")    

                if tank_condition_code == 1:                                   # Tank level is critical ==> turn pump on regardless
                    logger.debug(f"..Condition AUTO-5. Pump [STOPPED].  Reading [FRESH].  Tank [CRITICAL]."  )
                    logger.debug('..Pump will now be switched on as the water level is critical (even if it is night time).')
                    pump_handler_turnon(False, 'Pump auto mode checker - Tank level critical AUTO-5')

                elif tank_condition_code == 2 and fronuis1_available:          # Tank level is adequate & fronius has power ==> turn pump on 
                    logger.debug(f"..Condition AUTO-6. Pump [STOPPED].  Reading [FRESH].  Tank [ADEQUATE].  Fronius [AVAILABLE]. Tank condition code [{tank_condition_code}].  Actual level [{tank_water_status['tank_waterlevel']}].")
                    logger.debug('..Pump will now be switched on to opportunistically pump as water is needed.')
                    pump_handler_turnon(False, 'Pump auto mode checker - Tank level adequate only AUTO-6')               

                elif tank_condition_code == 2 and not fronuis1_available:      # Tank level is adequate & fronius has no power  ==> leave pump off
                    logger.debug(f"..Condition AUTO-7. Pump [STOPPED].  Reading [FRESH].  Tank [ADEQUATE].  Fronius [NOT AVAILABLE]. Tank condition code [{tank_condition_code}].  Actual level [{tank_water_status['tank_waterlevel']}].")
                    logger.debug('..Pump can stay off as water level is adequate and no current solar power.')

                elif tank_condition_code == 3:                                 # Pump stopped & water level full ==> leave pump off
                    logger.debug(f"..Condition AUTO-8. Pump [STOPPED].  Reading [FRESH].  Tank [FULL].  Tank condition code [{tank_condition_code}].  Actual level [{tank_water_status['tank_waterlevel']}].")
                    logger.debug('..The pump can stay off as tank is full.')

                else:
                    logger.warning("WARNING.  Condition AUTO-12.  No condition match found.  This is probably not good.")

        else:
            logger.debug("Invalid condition.  Pump must be running or not running.")
    
    else:       # ---- This condition should never be reached
        logger.debug(f"An invalid controller run mode [{system_status['controller_run_state']['run_mode']}] was detected (must be 1, 2 or 3).")

    system_status['environment_state']['run_sequence'] += 1     # Increment the sequence number.
    logger.debug(f"Pump tank and solar checks initiated by [{arg_reason}] have completed.")




# ---------- Simple dump of these dictionaries ------------------------------------------------------------------------
def decorativeStatusDumper(argSource):
    print(f'\n\n=============== SYSTEM STATUS DUMP ======[{argSource}]==================')
    print(' General system ---------------------------')
    print(f"  System run mode                   {system_status['controller_run_state']['run_mode']}")
    print(f"  Run mode last changed by          {system_status['controller_run_state']['run_mode_changed_by']}")
    print(f"  Run mode last command source      {system_status['controller_run_state']['run_mode_command_source']}")
    print(f"  Run mode changed at time          {system_status['controller_run_state']['run_mode_changed_time']}")
    print(' AC Power ---------------------------------')
    print(f"  AC Phase 1 status                 {system_status['power_state']['phase1_present']}")
    print(f"  AC Phase 2 status                 {system_status['power_state']['phase2_present']}")
    print(f"  AC Phase 3 status                 {system_status['power_state']['phase3_present']}")
    print(' Pump conditions --------------------------')
    print(f"  Pump running                      {system_status['pump_run_state']['pump_running']}")
    print(f"  Pump fault                        {system_status['pump_run_state']['pump_fault']}")
    print(' Fronius inverter digital IO --------------')
    print(f"  Fronuis Digital I/O #1            {system_status['fronius_state']['fronius_1']}")
    print(f"  Fronuis Digital I/O #2            {system_status['fronius_state']['fronius_2']}")
    print(f"  Fronuis Digital I/O #3            {system_status['fronius_state']['fronius_3']}")
    print(f"  Fronuis Digital I/O #4            {system_status['fronius_state']['fronius_4']}")
    print(' Environment state ------------------------')
    print(f"  Run sequence number               {system_status['environment_state']['run_sequence']}")
    print(f"  Change detected flag              {system_status['environment_state']['change_detected']}")
    print(f"  CPU temperature                   {system_status['environment_state']['cpu_temperature']}")
    print(f"  Enclosure temperature             {system_status['environment_state']['enclosure_temperature']}")
    print(f"  Enclosure humidity                {system_status['environment_state']['enclosure_humidity']}")
    print(' Alarms -----------------------------------')
    print(f"  Enclosure over-temperature alarm  {system_status['alarms']['enclosure_overtemperature']}")
    print(f"  Enclosure over-humidity alarm     {system_status['alarms']['enclosure_overhumidity']}")
    print(f"  CPU over-temperature alarm        {system_status['alarms']['cpu_overtemperature']}")
    print(f"  Water level sensor offline        {system_status['alarms']['water_level_sensor_offline']}")
    print(f"  Tamper switch                     {system_status['alarms']['tamper_switch']}")
    print(f"  Low Battery alarm                 {system_status['alarms']['battery_low']}")
    print(f"  Battery discharging alarm         {system_status['alarms']['battery_discharging']}")
    print(' Tank and water level ---------------------')
    print(f"  Tank ID                           {tank_water_status['tank_name']}")
    print(f"  Tank Water Level                  {tank_water_status['tank_waterlevel']}")
    print(f"  Tank Water Level updated at       {int(tank_water_status['tank_waterlevel_lastupdate'])}")
    print(' Power ------------------------------------')
    print(f"  Supply voltage                    {system_status['power']['supply_voltage']}")
    print(f"  Supply current                    {system_status['power']['supply_current']}")
    print(f"  Battery voltage                   {system_status['power']['battery_voltage']}")
    print(f"  Battery current                   {system_status['power']['battery_current']}")
    print(f"  Load voltage                      {system_status['power']['load_voltage']}")
    print(f"  Load current                      {system_status['power']['load_current']}")
    print('===========================================================\n\n')

# ---- Get power readings for each source
def readPowerValues(argSource):
    logger.debug(f'Getting power readings from Supply, Battery and Load circuits.  [{argSource}]')

    # Configurations for Supply
    ina_supply = INA219(0.1, address=0x40)
    #ina_supply.configure(ina_supply.RANGE_32V, ina_supply.GAIN_AUTO, ina_supply.ADC_12BIT, ina_supply.ADC_128SAMP)
    ina_supply.configure()

    # Configurations for Battery
    ina_battery = INA219(0.1, address=0x41)
    #ina_battery.configure(ina_battery.RANGE_16V, ina_battery.GAIN_AUTO, ina_battery.ADC_12BIT, ina_battery.ADC_128SAMP)
    ina_battery.configure()

    # Configurations for Load
    ina_load = INA219(0.1, address=0x45)
    #ina_load.configure(ina_load.RANGE_16V, ina_load.GAIN_AUTO, ina_load.ADC_12BIT, ina_load.ADC_128SAMP)
    ina_load.configure()

    # Supply readings
    try:
        system_status['power']['supply_voltage'] = float("{:.2f}".format(ina_supply.voltage()))
        system_status['power']['supply_current'] = float("{:.2f}".format(ina_supply.current()))
        logger.debug(f"..Supply voltage  [{system_status['power']['supply_voltage']}].  Current [{system_status['power']['supply_current']}].")
    except DeviceRangeError as e:
        logger.error("Current overflow when reading INA219 Supply voltage and current.")
        print(e)

    # Battery readings
    try:
        system_status['power']['battery_voltage'] = float("{:.2f}".format(ina_battery.voltage()))
        system_status['power']['battery_current'] = float("{:.2f}".format(ina_battery.current()))
        logger.debug(f"..Battery voltage [{system_status['power']['battery_voltage']}].  Current [{system_status['power']['battery_current']}].")

    except DeviceRangeError as e:
        logger.error("Current overflow when reading INA219 Battery voltage and current.")
        print(e)

    # Load readings
    try:
        system_status['power']['load_voltage'] = float("{:.2f}".format(ina_load.voltage()))
        system_status['power']['load_current'] = float("{:.2f}".format(ina_load.current()))
        logger.debug(f"..Load voltage    [{system_status['power']['load_voltage']}].  Current [{system_status['power']['load_current']}].")
    except DeviceRangeError as e:
        logger.errorprint("Current overflow when reading INA219 Load voltage and current.")
        print(e)

    #decorativeStatusDumper("Straight after power readings")


# ==== MAIN CODE =======================================================================================================
print("\n\n\n\n\n===============================================================")
print("Startup ...")


mqtt.Client.connected_flag = False   # Seems like this flag name is fixed


# ----- Confirm the necessary CLI parameters
if len(sys.argv) < 3:
    print("ERROR.  Found " + str(len(sys.argv) - 1) +
          " CLI parameters.  \n\tSpecify the following two command line parameters in order.  " +
          "\n\t  1) The fully qualified name of the local YAML config file, and " +
          "\n\t  2) The fully qualified name of the local (OS dependant) message log file. ")
    exit(2)
else:
    yaml_configuration_file = sys.argv[1]
    print("  YAML configuration will be retrieved from \t\t[" + yaml_configuration_file + "]")
    log_location = sys.argv[2]
    print("  Python logging system messages will be stored at \t[" + log_location + "]")



# ---------- These values come from the command line
filepath = yaml_configuration_file          # Where to find the YAML configuration file
data = yaml_loader(filepath)                # Where to write script errors before logging starts


# ---------- Set operating parameters from the retrieved YAML configuration data
try:
    system_startup_mode = data['system_configuration']['system_startup_mode']       # Sets manual, semi-automatic or automatic mode
    mqtt_broker_name =    data['broker_configuration']['broker_name']
    mqtt_broker_port =    data['broker_configuration']['broker_port']
    mqtt_broker_timeout = data['broker_configuration']['broker_timeout']
    local_station_name =  data['station_configuration']['mqtt_station_name']
    mqtt_user_name =      data['station_configuration']['mqtt_user_name']
    mqtt_user_password =  data['station_configuration']['mqtt_user_password']

    topic_pump_cmd    =   data['subscribe_topic_names']['topic_pump_cmd']

    topic_pump_lwt    =   data['publish_topic_names']['topic_pump_lwt']
    topic_pump_cmdack =   data['publish_topic_names']['topic_pump_cmdack']
    #topic_pump_cmdresp =  data['publish_topic_names']['topic_pump_cmdresp']
    topic_pump_status =   data['publish_topic_names']['topic_pump_status']
    topic_pump_lwt    =   data['publish_topic_names']['topic_pump_lwt']

    tank_threshold_low           = data['tank_level_thresholds']['tank_threshold_low']
    tank_threshold_high          = data['tank_level_thresholds']['tank_threshold_high']
    tank_waterlevel_maximum_age  = data['tank_level_thresholds']['tank_waterlevel_maximum_age']

    topic_tank_waterlevel = data['subscribe_topic_names']['topic_tank_waterlevel']

    nix_data_parking_area = data['backup_data_handling']['nix_data_parking_area']
    win_data_parking_area = data['backup_data_handling']['win_data_parking_area']

    enclosure_temp_alarm_base_value      = data['environment_thresholds']['enclosure_temp_alarm_setting']
    enclosure_humidity_alarm_base_value  = data['environment_thresholds']['enclosure_humidity_alarm_setting']
    cpu_temp_alarm_base_value            = data['environment_thresholds']['cpu_temp_alarm_setting']
    battery_low_voltage_alarm_base_value = data['environment_thresholds']['battery_low_voltage_alarm_setting']

    '''
        Initial alarm comparison is done against the base value, but once that base is exceeded the threshold
        gets lowered to the recovery value to introduce hysterisis.
        Different thresholds enjoy different hysterisis values which are in the YAML config.
    '''
    enclosure_temp_alarm_working_value =   enclosure_temp_alarm_base_value
    enclosure_temp_alarm_recovery_value =  enclosure_temp_alarm_base_value - data['environment_threshold_recovery_hysterisis']['enclosure_temp_recovery_hysterisis_value']

    enclosure_humidity_alarm_working_value =   enclosure_humidity_alarm_base_value
    enclosure_humidity_alarm_recovery_value =  enclosure_humidity_alarm_base_value - data['environment_threshold_recovery_hysterisis']['enclosure_humidity_recovery_hysterisis_value']

    cpu_temp_alarm_working_value =   cpu_temp_alarm_base_value
    cpu_temp_alarm_recovery_value =  cpu_temp_alarm_base_value - data['environment_threshold_recovery_hysterisis']['cpu_temp_recovery_hysterisis_value']

    battery_low_voltage_alarm_working_value =  battery_low_voltage_alarm_base_value
    battery_low_voltage_alarm_recovery_value = battery_low_voltage_alarm_base_value + data['environment_threshold_recovery_hysterisis']['battery_low_voltage_recovery_hysterisis_value']



except:
    print("ERROR 20.  Unable to parse YAML configuration data.  Check the config file for errors.")
    exit(2)


# ---- Determine the OS so we know which log location to use
if (platform.system() == "Windows"):
    os_type = "Windows"
    local_log_location = win_data_parking_area
elif (platform.system() == "Linux"):
    os_type = "Linux"
    local_log_location = nix_data_parking_area
else:
    os_type = "Unknown"
print("  Operating System detected as \t\t\t\t[" + os_type +"]")



'''
logging.getLogger("schedule").setLevel(logging.WARNING)         # Suppress trivial logs from the schedule module
logging.getLogger("ina219").setLevel(logging.WARNING)
logging.getLogger('12c').addHandler(logging.NullHandler())
'''

# ---- Use the python logging system to write log messages (advanced method).
# This config still has a problem suppressing the INA219 debug messages fromthe console.  Cannot seem to stop this rot.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch = logging.FileHandler(log_location)
ch = logging.handlers.TimedRotatingFileHandler(log_location, when='midnight', backupCount=30)


# class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None, errors=None)


handler2 = logging.NullHandler
handler3 = logging.FileHandler(log_location)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s \t%(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)




logger.info("---------------------------------------------------------------------------- ")  # Readability only
logger.info("---------- Script Startup ---------- " + "[" + os.path.basename(__file__) + "] -----")
logger.info("Config was retrieved from YAML [" + filepath + "]")

logger.debug("Script name is  [" + str(sys.argv[0]) + "]")
logger.debug("OS detected as  [" + os_type + "]")



# ---- Clobber the existing debug file (if appropriate during development)
CLOBBER = False
if CLOBBER:
    print("Attempting to delete any old debug file ==> " + str(log_location))
    try:
        os.remove(str(log_location))
        print("..Old debug log file deleted successfully.")
    except:
        print("..No old debug log file found to delete.")
else:
    print("Existing debug file [" + str(log_location) + "] is retained and appended to for this run.")





# ---- Build the big dictionary to hold all the status values and mode control and alarms
'''
    This entire object is reported any time an alarm occurs or the broker requests a ststus report.
    The environment_alarms section is just boolean flags indicating the presence of some type of alarm.  
    The flag is set when one of the conditions considered to be an alarm is triggered.  
    Refer to another section to determine the value of (for example) the value of the enclosure 
    temperature which triggered the alarm.  The timestamp is inserted when the publish occurs.
'''
system_status = {
    'controller_details': {
        'controller_name': '',
        'system_uptime': '',
        'script_starttime': 0,
        'script_uptime': ''
    },
    'controller_run_state': {
        'publish_timestamp': 0,
        'publish_requester': '',
        'run_mode': '',
        'run_mode_changed_by': '',
        'run_mode_command_source': '',
        'run_mode_changed_time': ''
    },
    'power_state': {
        'phase1_present': '', 
        'phase2_present': '',
        'phase3_present': ''
    },
    'pump_run_state': {
        'pump_running': '',
        'pump_fault': ''
    },
    'fronius_state': {
        'fronius_1': '',
        'fronius_2': '',
        'fronius_3': '', 
        'fronius_4': ''
    },
    'environment_state': {
        'run_sequence': 0,
        'change_detected': 0,
        'cpu_temperature': '',
        'enclosure_temperature': '',
        'enclosure_humidity': ''
    },
    'tank_status': {
        'tank_name': 'unset',
        'tank_waterlevel': 0,
        'tank_waterlevel_lastupdate': 0,
        'tank_waterlevel_age': 0
    },
    'alarms': {
        'enclosure_overtemperature': 0,
        'enclosure_overhumidity': 0,
        'cpu_overtemperature': 0,
        'water_level_sensor_offline': 0,
        'tamper_switch': 0,
        'battery_low': 0,
        'battery_discharging': 0
    },
    'power': {
        'supply_voltage': '',
        'supply_current': '',
        'battery_voltage': '',
        'battery_current': '',
        'load_voltage': '',
        'load_current': ''
    }
}

# ---- Build this dictionary to hold command responses
cmd_response_message = {
    'publish_timestamp': 0,                     # Standard inclusions in all messages
    'publish_requester': '',
    'stationid': local_station_name,            # This is always the case.
    'received_command': '',
    'response_code': '',
    'response_message': ''
}


# ---- Build this dictionary to hold tank water level data received from the broker. Start with some null type values.
tank_water_status = {
    'tank_name': 'undefined',
    'tank_waterlevel': 0,
    'tank_waterlevel_lastupdate': 0
}

# ---- Build this dictionary to define the command codes used.  This is just to make the debus moe readable.
logger.debug("Building 'command_code_lookup' dictionary.")  # Note the keys in this dict are integers.
command_code_lookup = {
    0: 'Stop Pump',
    1: 'Start Pump',
    2: 'Status Request',
    3: '3-Undefined',
    4: '4-Undefined',
    5: '5-Undefined',
    6: '6-Undefined',
    7: 'Switch to Manual Mode',
    8: 'Switch to Semi-automatic Mode',
    9: 'Switch to Automatic Mode'
}


# ---- Initialise the system run mode based on configuration from YAML
logger.debug("Setting the system run mode from the YAML configuration.")
'''
  run_modes are as follows.
  1 = manual
  2 = semi automatic
  3 = automatic   (this is the default mode)
'''

if int(system_startup_mode) == 1:
    logger.debug("..System run mode initialised to 'manual' by YAML configuration.")
    system_status['controller_run_state']['run_mode'] = 1
    system_status['controller_run_state']['run_mode_changed_by'] = "YAML configuration"

elif int(system_startup_mode) == 2:
    logger.debug("..System run mode initialised to 'semi-automatic' by YAML configuration.")
    system_status['controller_run_state']['run_mode'] = 2
    system_status['controller_run_state']['run_mode_changed_by'] = "YAML configuration"

elif int(system_startup_mode) == 3:
    logger.debug("..System run mode initialised to 'automatic' by YAML configuration.")
    system_status['controller_run_state']['run_mode'] = 3
    system_status['controller_run_state']['run_mode_changed_by'] = "YAML configuration"

else:
    logger.debug("..System run mode cannot be determined by YAML configuration so default to 'manual' mode.")
    system_status['controller_run_state']['run_mode'] = 1
    system_status['controller_run_state']['run_mode_changed_by'] = "Defaulted because YAML configuration is undefined."

system_status['controller_run_state']['run_mode_changed_time'] = int(time.time())



# ---- Initialise the system status dictionary
# These items are static, whereas other timers need to be calculated on demand when requested.
logger.debug("Initialising static data in the 'system_status' dictionary.")
system_status['controller_details']['controller_name'] = local_station_name
system_status['controller_details']['script_starttime'] = int(time.time())
system_status['controller_details']['script_uptime'] = int(time.time()) - system_status['controller_details']['script_starttime']



# ---- Determine the baseline status of all sense lines at script startup
'''
    This simply pokes the value read from the GPIO straight into the dict as a 0 or 1.
'''
logger.debug("Reading all control (GPIO) inputs and updating system status dictionary accordingly.")
system_status['power_state']['phase1_present'] = phase1_present_sense.value
system_status['power_state']['phase2_present'] = phase2_present_sense.value
system_status['power_state']['phase3_present'] = phase3_present_sense.value
system_status['pump_run_state']['pump_running'] = pump_running_sense.value
system_status['pump_run_state']['pump_fault'] = pump_fault_sense.value
system_status['environment_state']['tamper'] = tamper_switch_sense.value
system_status['fronius_state']['fronius_1'] = fronius_digital1_sense.value
system_status['fronius_state']['fronius_2'] = fronius_digital2_sense.value
system_status['fronius_state']['fronius_3'] = fronius_digital3_sense.value
system_status['fronius_state']['fronius_4'] = fronius_digital4_sense.value

# ---- Simple dump of these dictionaries
starter = time.time()
readPowerValues("Baseline run")

endert = time.time()

print(f"Time taken {(endert-starter)*1000:.0f}")
#exit(0)


# ---- Register the callbacks for the sense monitors
logger.debug("Registering callbacks for state change monitors.")
phase1_present_sense.when_released = phase1_lost
phase2_present_sense.when_released = phase2_lost
phase3_present_sense.when_released = phase3_lost
phase1_present_sense.when_held = phase1_restored
phase2_present_sense.when_held = phase2_restored
phase3_present_sense.when_held = phase3_restored
pump_running_sense.when_held = pump_running
pump_running_sense.when_released = pump_stopped
pump_fault_sense.when_held = pump_fault_detected
pump_fault_sense.when_released = pump_fault_cleared
fronius_digital1_sense.when_held = fronius_1_active
fronius_digital1_sense.when_released = fronius_1_inactive
fronius_digital2_sense.when_held = fronius_2_active
fronius_digital2_sense.when_released = fronius_2_inactive
fronius_digital3_sense.when_held = fronius_3_active
fronius_digital3_sense.when_released = fronius_3_inactive
fronius_digital4_sense.when_held = fronius_4_active
fronius_digital4_sense.when_released = fronius_4_inactive



# ---- Setup the MQTT client
logger.debug("Setting up MQTT connection to broker at [" + mqtt_broker_name + "] and registering callbacks.")
client = mqtt.Client(client_id="", userdata=None, clean_session=True, protocol=4)  # client ID must get made up
client.username_pw_set(username=mqtt_user_name, password=mqtt_user_password)

# ---- Register the MQTT callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
logger.debug('..Starting MQTT client loop.')
client.loop_start()


# ---- Do the MQTT connect
logger.debug('..Establishing MQTT connection to broker with LWT set.')

client.will_set(topic_pump_lwt, payload="The Pump Controller [" + local_station_name + "] has gone offline", qos=0, retain=False)
client.connect(mqtt_broker_name, mqtt_broker_port, mqtt_broker_timeout)
connect_start_time = time.time()
while not client.connected_flag:
    print("..Waiting for successful client connection to MQTT broker")
    time.sleep(0.5)
connect_stop_time = time.time()
logger.debug("..Client successfully connected to MQTT broker.")
logger.debug(f'..Time taken for broker connect was about {connect_stop_time - connect_start_time:.1f} seconds.')


# ---- Run a status check upon startup to grab baseline values
logger.debug('Determining the baseline state for the entire system (water level, pump state, solar, etc).')
pump_action_checker("Baseline")


# ---- Publish the system status right away so dependents such as the remote switch get an immediate status update.
logger.debug('Controller is now online so publish the baseline status.')
publish_generic_message("Baseline", topic_pump_status, system_status)


# ---- Now start the scheduled tasks
logger.debug("Now starting all scheduled tasks.")
schedule.every().hour.at(":00").do(jobHourlyHousekeeping)       # Should run pretty much every hour on the hour.
schedule.every(15).minutes.do(jobRegularHousekeeping)           # Should run rvery 15 minutes but not necessarily on the hour.
schedule.every(1).minutes.do(jobMinuteHousekeeping)             # Should run every minute to check for environment alarms


while True:
    if system_status['environment_state']['change_detected']:
        #print("Some monitored status has changed")
        #decorativeStatusDumper("while true loop")
        logger.debug("Publish system status update due to status change.")

        publish_generic_message('Status Change', topic_pump_status, system_status)
        system_status['environment_state']['change_detected'] = False       # Clear the change detected flag

    time.sleep(1)
    schedule.run_pending()

