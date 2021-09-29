# This is the Pump Remote Switch Panel

'''
    This is intended to mimic much of the operation of the manual contactor switch at the pump site.
    It will do the following.
    a)  The following buttons are available to the user.  All buttons are illuminated and the LED
        in each button may be controlled independently to the button itself.
        1)  Large Start and Stop buttons
            These are ussed to send MQTT start and Stop MQTT messages to the broker when a button is pressed.
        2)  Small mode select buttons consisting of
            a)  Manual mode
            b)  Semi Automatic mode
            c) Automatic mode
        3)  An alarm button

    All messages are JSON formatted.

    Buttons are illuminated with a LED which relies on receipt of the appropriate status message from the pump controller to 
    contol the LED illumination.  The button LEDs operate as follows.

    A status message will define which LED is lit solid.
    When a button is pressed (start, stop or run mode change) the following happens.
     1) If the button is already selected, the led will flash once to acknowledge the press but no MQTT message is sent.
     2) If the button is not selected, the selected buton in that group will be extinguished and the 'just pressed' 
     buton will begin to flash.  It will continue to flas until receipt of a status message from the pump controller.
     The received status message will define the LED state.

     The LEDs will flash in sequence when the system starts up.
    '''


# Changes
# 2020-11-15    Initial version.  This was added under Jupyter.


from gpiozero import Button	# import button from the Pi GPIO library
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice
from gpiozero import CPUTemperature
from gpiozero import LED

import time

import os 			                # imports OS library for Shutdown control
import logging
import platform
import sys
import yaml                         # Install PyYAML
import json
import paho.mqtt.client as mqtt     # Install paho-mqtt

import datetime
import threading
import schedule                     # Install schedule

import smbus                        # Install smbus
import inspect


# ---- Define the GPIO pins used by each button
manual_mode_button = Button(16, bounce_time=0.05)           # Pin 36
semiauto_mode_button = Button(17, bounce_time=0.05)	        # Pin 11
automatic_mode_button = Button(18, bounce_time=0.05)        # Pin 12
pump_start_button = Button(22)                              # Pin 15  Seems to work better with no debounce
pump_stop_button = Button(23)                               # Pin 16
alarm_button = Button(26, bounce_time=0.05)                 # Pin 37

# ---- Define the GPIO pins used by the LEDs inside the buttons
pump_start_button_led = LED(24, active_high=True, initial_value=False, pin_factory=None)        # Pin 18
pump_stop_button_led = LED(25, active_high=True, initial_value=False, pin_factory=None)         # Pin 22
manual_mode_button_led = LED(19, active_high=True, initial_value=False, pin_factory=None)       # Pin 35
semiauto_mode_button_led = LED(20, active_high=True, initial_value=False, pin_factory=None)     # Pin 38
auto_mode_button_led = LED(21, active_high=True, initial_value=False, pin_factory=None)         # Pin 40
alarm_button_led = LED(27, active_high=True, initial_value=False, pin_factory=None)             # Pin 13



# ---------- Configuration load from YAML -----------------------------------------------------------------------------
def yaml_loader(filepath):
    try:
        with open(filepath, "r") as file_descriptor:
            config_data = yaml.load(file_descriptor, Loader=yaml.FullLoader)    #Should avoid the unsafe warning
        return config_data
    except:
        logger.debug(f"ERROR 5.  Unable to open the YAML configuration file at {filepath}.")
        exit(5)



# ---------- Get the temperature and humidity from the SHT31 sensor ---------------------------------------------------
def getEnclosureTempHumi():
    #logger.debug("Getting enclosure temperature and humidity from SHT31 sensor.")
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
    #logger.debug("..SHT31 Temperature : %.1f C" %cTemp)
    #logger.debug("..SHT31 Humidity    : %.0f %%RH" %humidity)

    # And stuff these into the dictionary
    local_system_status['environment_state']['enclosure_temperature'] = format(cTemp,'.1f')
    local_system_status['environment_state']['enclosure_humidity'] = humidity


# ---------- Get Raspberry Pi CPU Temperature -------------------------------------------------------------------------
def getCpuTemperature():
    #logger.debug("Getting CPU temperature from Raspberry Pi CPU.")
    cpu = CPUTemperature()
    #logger.debug('..CPU  temperature  : {}C'.format(cpu.temperature))
    # And stuff it into the dictionary
    local_system_status['environment_state']['cpu_temperature'] = cpu.temperature


# ---------- Publish a generic environmental alarm --------------------------------------------------------------------
def publishEnvironmentAlarm(alarmNumber, alarmState):
    # This will ultimately publish an environment alarm
    '''
        Received parameters ar as follows.
        alarmNumber = alarm number
        alarmState.  1=New alarm.  0=Cleared alarm.
    '''
    logger.debug("Publish the alarm message.")
    x = client.publish(topic_local_status, payload=json.dumps(local_system_status), qos=0, retain=False)
    logger.debug("..Alarm publish result = " + str(x))


# ---------- Now check if we have any alarm conditions present that need to be reported -------------------------------
def checkForLocalAlarms():
    logger.debug('Running a check of local temperature and humidity environmment conditions.')
    '''
        There are many possible alarm conditions to inspect.  
        Each one is done individually and a message is published for fresh alarms and cleared alarms (but not for ongoing alarms).
        '''
    checkAlarm01()      # Enclosure temperature
    checkAlarm02()      # Enclosure humidity
    checkAlarm03()      # CPU Temperature


# ---------- Alarm check 01 - Enclosure over temperature --------------------------------------------------------------
def checkAlarm01():    
    logger.debug('.Alarm check 01 - Check for enclosure over-temperature alarm.')
    global enclosure_temp_alarm_base_value
    global enclosure_temp_alarm_recovery_value    
    global enclosure_temp_alarm_working_value
    
    if float(local_system_status['environment_state']['enclosure_temperature']) < enclosure_temp_alarm_working_value and not local_system_status['alarms']['enclosure_overtemperature']:
        # All good and nothing to do
        logger.debug(f"..NORMAL.  Enclosure temperature [{float(local_system_status['environment_state']['enclosure_temperature']):.1f}] is below threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")

    elif float(local_system_status['environment_state']['enclosure_temperature']) >= enclosure_temp_alarm_working_value and not local_system_status['alarms']['enclosure_overtemperature']:
        # This is a fresh over temperature alarm.  Set the enclosure over-temp alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  Enclosure temperature [{float(local_system_status['environment_state']['enclosure_temperature']):.1f}] is at or above threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
        local_system_status['alarms']['enclosure_overtemperature'] = True
        publishEnvironmentAlarm(1,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the over-temp alarm threshold from [{enclosure_temp_alarm_working_value:.1f}] to [{enclosure_temp_alarm_recovery_value:.1f}].")
        enclosure_temp_alarm_working_value = enclosure_temp_alarm_recovery_value
        alarm_button_led.blink(on_time=0.05, off_time=0.05, n=20, background = True)    # Rapid flash

    elif float(local_system_status['environment_state']['enclosure_temperature']) >= enclosure_temp_alarm_working_value and local_system_status['alarms']['enclosure_overtemperature']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  Enclosure temperature [{float(local_system_status['environment_state']['enclosure_temperature']):.1f}] remains above threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
    
    elif float(local_system_status['environment_state']['enclosure_temperature']) < enclosure_temp_alarm_working_value and local_system_status['alarms']['enclosure_overtemperature']:
        # This is the recovery of an ongoing alarm.  Clear the enclosure over-temp alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  Enclosure temperature [{float(local_system_status['environment_state']['enclosure_temperature']):.1f}] is now below threshold of [{float(enclosure_temp_alarm_working_value):.1f}].")
        local_system_status['alarms']['enclosure_overtemperature'] = False
        publishEnvironmentAlarm(1,0)
        # Restore threshold temperature.
        logger.debug(f"..Hysterisis restoring the over-temp alarm threshold from [{enclosure_temp_alarm_working_value:.1f}] to [{enclosure_temp_alarm_base_value:.1f}].")
        enclosure_temp_alarm_working_value = enclosure_temp_alarm_base_value

    else:
        logger.debug("ERROR 101.  Problem with interrogating enclosure temperature.")


# ---------- Alarm check 02 - Enclosure over humidity -----------------------------------------------------------------
def checkAlarm02():    
    logger.debug('.Alarm check 02 - Check for enclosure over-humidity alarm.')
    global enclosure_humidity_alarm_base_value
    global enclosure_humidity_alarm_recovery_value    
    global enclosure_humidity_alarm_working_value
    
    if float(local_system_status['environment_state']['enclosure_humidity']) < enclosure_humidity_alarm_working_value and not local_system_status['alarms']['enclosure_overhumidity']:
        # All good and nothing to do
        logger.debug(f"..NORMAL.  Enclosure humidity [{float(local_system_status['environment_state']['enclosure_humidity']):.0f}] is below threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")

    elif float(local_system_status['environment_state']['enclosure_humidity']) >= enclosure_humidity_alarm_working_value and not local_system_status['alarms']['enclosure_overhumidity']:
        # This is a fresh over humidity alarm.  Set the enclosure over-humidity alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  Enclosure humidity [{float(local_system_status['environment_state']['enclosure_humidity']):.1f}] is at or above threshold of [{float(enclosure_humidity_alarm_working_value):.1f}].")
        local_system_status['alarms']['enclosure_overhumidity'] = True
        publishEnvironmentAlarm(2,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the over-humidity alarm threshold from [{enclosure_humidity_alarm_working_value:.0f}] to [{enclosure_humidity_alarm_recovery_value:.0f}].")
        enclosure_humidity_alarm_working_value = enclosure_humidity_alarm_recovery_value
        alarm_button_led.blink(on_time=0.05, off_time=0.05, n=20, background = True)    # Rapid flash

    elif float(local_system_status['environment_state']['enclosure_humidity']) >= enclosure_humidity_alarm_working_value and local_system_status['alarms']['enclosure_overhumidity']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  Enclosure humidity [{float(local_system_status['environment_state']['enclosure_humidity']):.0f}] remains above threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")
    
    elif float(local_system_status['environment_state']['enclosure_humidity']) < enclosure_humidity_alarm_working_value and local_system_status['alarms']['enclosure_overhumidity']:
        # This is the recovery of an ongoing alarm.  Clear the enclosure over-humidity alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  Enclosure humidity [{float(local_system_status['environment_state']['enclosure_humidity']):.0f}] is now below threshold of [{float(enclosure_humidity_alarm_working_value):.0f}].")
        local_system_status['alarms']['enclosure_overhumidity'] = False
        publishEnvironmentAlarm(2,0)
        # Restore threshold humidity.
        logger.debug(f"..Hysterisis restoring the over-humidity alarm threshold from [{enclosure_humidity_alarm_working_value:.0f}] to [{enclosure_humidity_alarm_base_value:.0f}].")
        enclosure_humidity_alarm_working_value = enclosure_humidity_alarm_base_value

    else:
        logger.debug("ERROR 201.  Problem with interrogating enclosure humidity.")


# ---------- Alarm check 03 - CPU over temperature --------------------------------------------------------------------
def checkAlarm03():    
    logger.debug('.Alarm check 03 - Check for CPU over-temperature alarm.')
    global cpu_temp_alarm_base_value
    global cpu_temp_alarm_recovery_value    
    global cpu_temp_alarm_working_value
    
    if float(local_system_status['environment_state']['cpu_temperature']) < cpu_temp_alarm_working_value and not local_system_status['alarms']['cpu_overtemperature']:
        # All good and nothing to do
        logger.debug(f"..NORMAL.  CPU temperature [{float(local_system_status['environment_state']['cpu_temperature']):.1f}] is below threshold of [{float(cpu_temp_alarm_working_value):.1f}].")

    elif float(local_system_status['environment_state']['cpu_temperature']) >= cpu_temp_alarm_working_value and not local_system_status['alarms']['cpu_overtemperature']:
        # This is a fresh over temperature alarm.  Set the cpu over-temp alarm flag and publish an alarm.
        logger.debug(f"..NEW ALARM.  CPU temperature [{float(local_system_status['environment_state']['cpu_temperature']):.1f}] is at or above threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
        local_system_status['alarms']['cpu_overtemperature'] = True
        publishEnvironmentAlarm(3,1)
        # Bump the threshold down to introduce hysterisis for recovery.
        logger.debug(f"..Hysterisis lowering the CPU over-temp alarm threshold from [{cpu_temp_alarm_working_value:.1f}] to [{cpu_temp_alarm_recovery_value:.1f}].")
        cpu_temp_alarm_working_value = cpu_temp_alarm_recovery_value
        alarm_button_led.blink(on_time=0.05, off_time=0.05, n=20, background = True)    # Rapid flash

    elif float(local_system_status['environment_state']['cpu_temperature']) >= cpu_temp_alarm_working_value and local_system_status['alarms']['cpu_overtemperature']:
        # This constitutes an ongoing alarm which does not need to be published again because it has already been done when the condition was first detected.
        logger.debug(f"..CONTINUED ALARM.  CPU temperature [{float(local_system_status['environment_state']['cpu_temperature']):.1f}] remains above threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
    
    elif float(local_system_status['environment_state']['cpu_temperature']) < cpu_temp_alarm_working_value and local_system_status['alarms']['cpu_overtemperature']:
        # This is the recovery of an ongoing alarm.  Clear the cpu over-temp alarm flag and publish a message to indicate recovery.
        logger.debug(f"..CLEARED ALARM.  CPU temperature [{float(local_system_status['environment_state']['cpu_temperature']):.1f}] is now below threshold of [{float(cpu_temp_alarm_working_value):.1f}].")
        local_system_status['alarms']['cpu_overtemperature'] = False
        publishEnvironmentAlarm(3,0)
        # Restore threshold temperature.
        logger.debug(f"..Hysterisis restoring the CPU over-temp alarm threshold from [{cpu_temp_alarm_working_value:.1f}] to [{cpu_temp_alarm_base_value:.1f}].")
        cpu_temp_alarm_working_value = cpu_temp_alarm_base_value

    else:
        logger.debug("ERROR 301.  Problem with interrogating CPU temperature.")



# ---------- Check Status Freshness -----------------------------------------------------------------------------------
def checkStatusFreshness(arg_requester):
    # This checks if the most recent status update is current.  If not go into some form of alarm.
    # Status updates should be received at least every hour.
    logger.debug(f'Checking freshness of most recent status report [{arg_requester}]')
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])

    if seconds_since_last_status_update > status_freshness_threshold * 60:
        logger.debug(f"Last status message is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Alarm raised.")
        alarm_button_led.blink(on_time=0.5, off_time=0.5, n=None, background = True)    # Gives a rapid flash 

        cmd_message_payload['command_code'] = 2          # 2 = Send status update
        logger.debug("..Publish 'send status update' message")
        x = client.publish(topic_pump_cmd, payload=json.dumps(cmd_message_payload), qos=0, retain=False)
        logger.debug("..Publish result = " + str(x))

# ---------- These are the jobs managed by the schedule module --------------------------------------------------------
def jobMinuteHousekeeping():
    # This is intended to run every minute to check for temperature alarms
    # logger.debug("Every minute jobs will now run.")

    getEnclosureTempHumi()
    getCpuTemperature()
    
    decorativeStatusDumper("Minute")
    checkForLocalAlarms()
    checkStatusFreshness("Every Minute")



# --06-------- Generic command message publisher ----------------------------------------------------------------------
def publish_command_message(arg_reason):
    # This is intende as the central pont for publishing all command messages.  The timestamp and requester are 
    # inserted here just before publishing.
    logger.debug(f"Publishing a generic command message requested by [{arg_reason}]")
    cmd_message_payload['publish_timestamp'] = format(time.time(), '.0f')
    cmd_message_payload['publish_requester'] = arg_reason
    x = client.publish(topic_pump_cmd, payload=json.dumps(cmd_message_payload), qos=0, retain=False)
    logger.debug("..Command publish status result = " + str(x))




# ---------- Button handlers which drive state changes ----------------------------------------------------------------
'''
    Each button sends a specific command code to the controller.
    The following command codes are recognised by the controller
        0 = turn off the pump
        1 = turn on the pump
        2 = issue an immediate status update
        7 = switch to manual mode
        8 = switch to semi-automatic mode
        9 = switch to automatic mode
'''

# ---- 01 Stop button handler
def pump_stop_button_pressed():
    logger.debug("BUTTON ==> Pump stop button has been pressed.")
    # decorativeStatusDumper('stop button')
    
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])

    if controller_status_mimic['alarms']['cpu_overtemperature']:                # Check for CPU over temp
        logger.debug('A CPU over temperature alarm exists.  Button press ignored.')
        
    elif controller_status_mimic['pump_run_state']['pump_fault']:               # Check for pump fault
        logger.debug('Pump fault exists.  Stop button press ignored.')
 
    elif broker_supplied_status['lwt_offline']:                                 # Check if the controller is in a LWT offline status
        seconds_since_lwt_received = time.time() - float(broker_supplied_status['lwt_offline_timestamp'])
        logger.debug(f"The controller has been offline for [{seconds_since_lwt_received:.0f}] seconds.  Stop button press ignored.")
        
    elif seconds_since_last_status_update > status_freshness_threshold * 60:    # Check if the last status is still fresh.
        logger.debug(f"Last controller status update is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Pump stop disabled.")
        
    elif not controller_status_mimic['pump_run_state']['pump_running']:          # Check the current pump run status
        # The pump must already be stopped so just flick the LED to acknowledge the press, but do zilch.
        logger.debug("..Status reports the pump as already stopped so no action will be taken.")
        pump_stop_button_led.blink(on_time=0.1, off_time=0.1, n=5, background = False)
        pump_stop_button_led.on()       # Ensure it is left on.
    
    else:
        # The pump is presumably running so extinguish the start LED and blink the stop LED slowly to indicate a pending action.
        logger.debug("..Status reports the pump is currently started so initiate stop sequence.")
        pump_start_button_led.off()
        pump_stop_button_led.blink(on_time=0.3, off_time=0.3, n=None, background = True)
        # Send the power off message.  Rely on the ensuing status message to set the new LED status.
        cmd_message_payload['command_code'] = 0
        logger.debug("..Publish 'pump stop' message")
        publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function
        #x = client.publish(topic_pump_cmd, payload=json.dumps(cmd_message_payload), qos=0, retain=False)
        #logger.debug("..Publish result = " + str(x))


# ---- 02 Start button handler
def pump_start_button_pressed():
    logger.debug("BUTTON ==> Pump start button has been pressed.")
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])
    
    if controller_status_mimic['alarms']['cpu_overtemperature']:
        logger.debug('A CPU over temperature alarm exists.  Start button press ignored.')
        
    elif controller_status_mimic['pump_run_state']['pump_fault']:
        logger.debug('Pump fault exists.  Start button press ignored.')

    elif broker_supplied_status['lwt_offline']:                     # Check if the controller is in a LWT offline status
        seconds_since_lwt_received = time.time() - float(broker_supplied_status['lwt_offline_timestamp'])
        logger.debug(f"The controller has been offline for [{seconds_since_lwt_received:.0f}] seconds.  Start button press ignored.")
        
    elif seconds_since_last_status_update > status_freshness_threshold * 60:
        logger.debug(f"Last controller status update is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Pump start disabled.")
        
    elif controller_status_mimic['pump_run_state']['pump_running']:             # Check the current pump run status
        # The pump must already be running so just flick the LED to acknowledge the press, but do zilch.
        logger.debug("..Status reports the pump as already running so no action will be taken.")
        pump_start_button_led.blink(on_time=0.1, off_time=0.1, n=5, background = False)
        pump_start_button_led.on()       # Ensure it is left on.

    else:
        # The pump is presumably stopped so extinguish to stopped LED and blink the start LED slowly to indicate a pending action.
        logger.debug("..Status reports the pump is currently stopped so initiate start sequence.")
        pump_stop_button_led.off()
        pump_start_button_led.blink(on_time=0.3, off_time=0.3, n=None, background = True)
        # Send the power on message.  Rely on the ensuing status message to set the new LED status.
        cmd_message_payload['command_code'] = 1
        logger.debug("..Publish 'pump start' message")
        publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function


        # x = client.publish(topic_pump_cmd, payload=json.dumps(cmd_message_payload), qos=0, retain=False)
        # logger.debug("..Publish result = " + str(x))


# ---- 03 Manual mode button handler
def manual_mode_button_pressed():
    logger.debug("BUTTON ==> Manual mode button has been pressed.")
    logger.debug(f"..Current controller run mode [{controller_status_mimic['controller_run_state']['run_mode']}].")

    # Check the current controller run mode for manual mode
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])
    if broker_supplied_status['lwt_offline']:           # Check if the controller is in a LWT offline status
        seconds_since_lwt_received = time.time() - float(broker_supplied_status['lwt_offline_timestamp'])
        logger.debug(f"The controller has been offline for [{seconds_since_lwt_received:.0f}] seconds so command input is prevented.")
        manual_mode_button_led.blink(on_time=0.1, off_time=0.1, n=3, background = True)
    elif seconds_since_last_status_update > status_freshness_threshold * 60:
        logger.debug(f"Last controller status update is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Mode change not permitted.")
        semiauto_mode_button_led.off()
        auto_mode_button_led.off()
        manual_mode_button_led.blink(on_time=0.05, off_time=0.05, n=5, background = True)
    elif  controller_status_mimic['controller_run_state']['run_mode'] == 1:
        # The controller must already be running in manual mode so just flick the LED to acknowledge the press, but do zilch.
        manual_mode_button_led.blink(on_time=0.3, off_time=0.3, n=5, background = False)
        manual_mode_button_led.on()       # Ensure it is left on.
    else:
        # The controller must be in one of the other modes, so extinguish both other LEDs and blink the manual mode LED slowly to indicate a pending action.
        semiauto_mode_button_led.off()
        auto_mode_button_led.off()
        manual_mode_button_led.blink(on_time=0.3, off_time=0.3, n=None, background = True)
        # Send the 'go to manual mode' message.  Rely on the ensuing status message to set the new LED status.
        cmd_message_payload['command_code'] = 7         # 7 = Go to manual mode
        logger.debug("..Publish 'switch to manual mode' message.")
        publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function


# ---- 04 Semi-automatic button handler
def semiauto_mode_button_pressed():
    logger.debug("BUTTON ==> Semi-automatic mode button has been pressed.")
    logger.debug(f"..Current controller run mode [{controller_status_mimic['controller_run_state']['run_mode']}].")

    # Check the current controller run mode for semiauto mode
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])
    if broker_supplied_status['lwt_offline']:           # Check if the controller is in a LWT offline status
        seconds_since_lwt_received = time.time() - float(broker_supplied_status['lwt_offline_timestamp'])
        logger.debug(f"The controller has been offline for [{seconds_since_lwt_received:.0f}] seconds so command input is prevented.")
        semiauto_mode_button_led.blink(on_time=0.1, off_time=0.1, n=3, background = True)
    elif seconds_since_last_status_update > status_freshness_threshold * 60:
        logger.debug(f"Last controller status update is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Mode change not permitted.")
        manual_mode_button_led.off()
        auto_mode_button_led.off()
        semiauto_mode_button_led.blink(on_time=0.05, off_time=0.05, n=5, background = True)
    elif  controller_status_mimic['controller_run_state']['run_mode'] == 2:
        # The controller must already be running in semi-automatic mode so just flick the LED to acknowledge the press, but do zilch.
        semiauto_mode_button_led.blink(on_time=0.1, off_time=0.1, n=5, background = False)
        semiauto_mode_button_led.on()       # Ensure it is left on.
    else:
        # The controller must be in one of the other modes, so extinguish both other LEDs and blink the semiauto mode LED slowly to indicate a pending action.
        manual_mode_button_led.off()
        auto_mode_button_led.off()
        semiauto_mode_button_led.blink(on_time=0.3, off_time=0.3, n=None, background = True)
        # Send the 'go to semi-auto mode' message.  Rely on the ensuing status message to set the new LED status.
        cmd_message_payload['command_code'] = 8      # 8 - Go to semi-automatic mode
        logger.debug("..Publish 'switch to semi-automatic mode' message.")
        publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function
        

# ---- 05 Automatic button handler
def automatic_mode_button_pressed():
    logger.debug("BUTTON ==> Automatic mode button has been pressed.")
    logger.debug(f"..Current controller run mode [{controller_status_mimic['controller_run_state']['run_mode']}].")
    
    # Check the current controller run mode for auto mode
    seconds_since_last_status_update = time.time() - float(controller_status_mimic['controller_run_state']['publish_timestamp'])
    if broker_supplied_status['lwt_offline']:           # Check if the controller is in a LWT offline status
        seconds_since_lwt_received = time.time() - float(broker_supplied_status['lwt_offline_timestamp'])
        logger.debug(f"The controller has been offline for [{seconds_since_lwt_received:.0f}] seconds so command input is prevented.")
        auto_mode_button_led.blink(on_time=0.1, off_time=0.1, n=3, background = True)
    elif seconds_since_last_status_update > status_freshness_threshold * 60:
        logger.debug(f"Last controller status update is [{(seconds_since_last_status_update / 60):.1f}] minutes old and is stale.  Mode change not permitted.")
        manual_mode_button_led.off()
        semiauto_mode_button_led.off()
        auto_mode_button_led.blink(on_time=0.05, off_time=0.05, n=5, background = True)
    elif  controller_status_mimic['controller_run_state']['run_mode'] == 3:
        # The controller must already be running in automatic mode so just flick the LED to acknowledge the press, but do zilch.
        auto_mode_button_led.blink(on_time=0.1, off_time=0.1, n=5, background = False)
        auto_mode_button_led.on()       # Ensure it is left on.
    else:
        # The controller must be in one of the other modes, so extinguish both other LEDs and blink the automatic mode LED slowly to indicate a pending action.
        manual_mode_button_led.off()
        semiauto_mode_button_led.off()
        auto_mode_button_led.blink(on_time=0.3, off_time=0.3, n=None, background = True)
        # Send the 'go to automatic mode' message.  Rely on the ensuing status message to set the new LED status.
        cmd_message_payload['command_code'] = 9          # 9 = Go to automatic mode
        logger.debug("..Publish 'switch to automatic mode' message.")
        publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function
       



# ---- 06 Alarm button handler
def alarm_button_pressed():
    logger.debug("BUTTON ==> Alarm button has been pressed.")
    '''
        The alarm button is used to reset the status lights.  It does the following.
        - clears the alarm LED and sts it to fast blink
        - solicits a status update from the controller, which means the LEDS will get reset to the correct state
    '''
    pump_start_button_led.off()
    pump_stop_button_led.off()
    manual_mode_button_led.off()
    semiauto_mode_button_led.off()
    auto_mode_button_led.off()
    alarm_button_led.off()
    
    # Send the 'request status update' message.  Rely on the ensuing status message to set the new LED status.
    alarm_button_led.blink(on_time=0.1, off_time=0.5, n=None, background = True)    # Gives a fast flash 
    cmd_message_payload['command_code'] = 2          # 2 = Send status update
    logger.debug("..Publish 'request status update' message")
    publish_command_message(inspect.stack()[0][3])        # This grabs the name of the current function

    


# ---- LED flash on startup -------------------------------------------------------------------------------------------
def led_startup_sequence():
    # Turn the LEDS on and off in sequence
    logger.debug("Testing all button LEDs.")
    pump_start_button_led.on()
    time.sleep(0.5)

    pump_stop_button_led.on()
    time.sleep(0.5)

    manual_mode_button_led.on()
    time.sleep(0.5)

    semiauto_mode_button_led.on()
    time.sleep(0.5)

    auto_mode_button_led.on()
    time.sleep(0.5)

    alarm_button_led.on()
    time.sleep(0.5)

    pump_start_button_led.off()
    time.sleep(0.5)

    pump_stop_button_led.off()
    time.sleep(0.5)

    manual_mode_button_led.off()
    time.sleep(0.5)

    semiauto_mode_button_led.off()
    time.sleep(0.5)

    auto_mode_button_led.off()
    time.sleep(0.5)

    alarm_button_led.off()
    time.sleep(0.5)

    logger.debug("..Button LED tests complete.")

# ---- Extinguish all LEDS --------------------------------------------------------------------------------------------
def extinguish_all_button_leds():
    # Simple function to turn them all off.
    
    pump_start_button_led.off()
    pump_stop_button_led.off()

    manual_mode_button_led.off()
    semiauto_mode_button_led.off()
    auto_mode_button_led.off()
    alarm_button_led.off()




# ---- Process a received status message
def process_status_message(message_payload):
    logger.debug('Processing a received status message.')
    # Copy the details received in the JSON payload into the local dictionary.  This dictionary
    # is intended to mimic the system_status dictionary maintained on the controller itself.
    # Not all of the received data is used here but a future release of the switch panel may incorporate
    # a more extensive display to report all this detail so cater for the data now.

    #logger.debug(f"\nRaw received: {message_payload}")
    received_status_message = json.loads(message_payload)
    #logger.debug(f"\nJSON Recieved: {received_status_message}")

    # Any kind of status update from the controller suggests it is online so clear any LWT flag
    broker_supplied_status['lwt_offline'] = False
    broker_supplied_status['lwt_offline_timestamp'] = time.time()

    # ---- Update the local mimic of the controller status
    # Run state details
    controller_status_mimic['controller_run_state']['publish_timestamp']      = received_status_message['controller_run_state']['publish_timestamp']
    controller_status_mimic['controller_run_state']['publish_requester']      = received_status_message['controller_run_state']['publish_requester']
    controller_status_mimic['controller_run_state']['run_mode']               = received_status_message['controller_run_state']['run_mode']
    controller_status_mimic['controller_run_state']['run_mode_changed_by']    = received_status_message['controller_run_state']['run_mode_changed_by']
    controller_status_mimic['controller_run_state']['run_mode_changed_time']  = received_status_message['controller_run_state']['run_mode_changed_time']

    # Power state details
    controller_status_mimic['power_state']['phase1_present']  = received_status_message['power_state']['phase1_present']
    controller_status_mimic['power_state']['phase2_present']  = received_status_message['power_state']['phase2_present']
    controller_status_mimic['power_state']['phase3_present']  = received_status_message['power_state']['phase3_present']

    # Pump state details
    controller_status_mimic['pump_run_state']['pump_running'] = received_status_message['pump_run_state']['pump_running']
    controller_status_mimic['pump_run_state']['pump_fault']   = received_status_message['pump_run_state']['pump_fault']

    # Fronius state details
    controller_status_mimic['fronius_state']['fronius_1']  = received_status_message['fronius_state']['fronius_1']
    controller_status_mimic['fronius_state']['fronius_2']  = received_status_message['fronius_state']['fronius_2']
    controller_status_mimic['fronius_state']['fronius_3']  = received_status_message['fronius_state']['fronius_3']
    controller_status_mimic['fronius_state']['fronius_4']  = received_status_message['fronius_state']['fronius_4']

    # Environment state details
    controller_status_mimic['environment_state']['run_sequence']           = received_status_message['environment_state']['run_sequence']
    controller_status_mimic['environment_state']['change_detected']        = received_status_message['environment_state']['change_detected']
    controller_status_mimic['environment_state']['cpu_temperature']        = received_status_message['environment_state']['cpu_temperature']
    controller_status_mimic['environment_state']['enclosure_temperature']  = received_status_message['environment_state']['enclosure_temperature']
    controller_status_mimic['environment_state']['enclosure_humidity']     = received_status_message['environment_state']['enclosure_humidity']

    # Alarm state details
    controller_status_mimic['alarms']['enclosure_overtemperature']   = received_status_message['alarms']['enclosure_overtemperature']
    controller_status_mimic['alarms']['enclosure_overhumidity']      = received_status_message['alarms']['enclosure_overhumidity']
    controller_status_mimic['alarms']['cpu_overtemperature']         = received_status_message['alarms']['cpu_overtemperature']
    controller_status_mimic['alarms']['water_level_sensor_offline']  = received_status_message['alarms']['water_level_sensor_offline']
    controller_status_mimic['alarms']['tamper_switch']               = received_status_message['alarms']['tamper_switch']
    controller_status_mimic['alarms']['battery_low']                 = received_status_message['alarms']['battery_low']
    controller_status_mimic['alarms']['battery_discharging']         = received_status_message['alarms']['battery_discharging']

    # Power details
    controller_status_mimic['power']['supply_voltage']   = received_status_message['power']['supply_voltage']
    controller_status_mimic['power']['supply_current']   = received_status_message['power']['supply_current']
    controller_status_mimic['power']['battery_voltage']  = received_status_message['power']['battery_voltage']
    controller_status_mimic['power']['battery_current']  = received_status_message['power']['battery_current']
    controller_status_mimic['power']['load_voltage']     = received_status_message['power']['load_voltage']
    controller_status_mimic['power']['load_current']      = received_status_message['power']['load_current']

    decorativeStatusDumper('Status Update')

    # ---- Now setup the LEDs based on this status update.
    # 01 - Set the start and stop LEDs
    if controller_status_mimic['pump_run_state']['pump_running']:
        # Indicates pump is running
        pump_start_button_led.on()
        pump_stop_button_led.off()
    else:
        # Indicates the pump is stopped
        pump_start_button_led.off()
        pump_stop_button_led.on()

    # 02 - Set the run mode LEDs
    if controller_status_mimic['controller_run_state']['run_mode'] == 1:
        # Looks like manual mode
        manual_mode_button_led.on()
        semiauto_mode_button_led.off()
        auto_mode_button_led.off()
    elif controller_status_mimic['controller_run_state']['run_mode'] == 2:
        # Looks like semi automatic mode
        manual_mode_button_led.off()
        semiauto_mode_button_led.on()
        auto_mode_button_led.off()
    elif controller_status_mimic['controller_run_state']['run_mode'] == 3:
        # Looks like automatic mode
        manual_mode_button_led.off()
        semiauto_mode_button_led.off()
        auto_mode_button_led.on()
    
    # 03 - Set the error condition LEDs
    '''
        The on/off timing for various environment alarms varies and this helps
        identify the actual alarm type.
        Alarm Type                      On_Time Off_Time
         Pump Fault                      5       0.1
         AC Phase failure (any phase)    5       1
         Enclosure over temperature      3       2
         Enclosure over humidity         3       4 
         CPU over temperature            3       6
         Water level sensor offline      0.1     10
         Tamper switch activated         0.1     15
         Battery low                     1       2
         Battery discharging             2       4
        '''
    
    if controller_status_mimic['pump_run_state']['pump_fault']:               # Pump fault condition
        logger.debug('Pump fault')
        alarm_button_led.blink(on_time=5.0, off_time=0.1, n=None, background = True)
    
    elif (not controller_status_mimic['power_state']['phase1_present'] or 
        not controller_status_mimic['power_state']['phase2_present'] or 
        not controller_status_mimic['power_state']['phase3_present']):          # One or more AC phases is missing
        logger.debug('At least one of the AC phases is missing.')
        alarm_button_led.blink(on_time=5.0, off_time=1, n=None, background = True)
        
    elif controller_status_mimic['alarms']['enclosure_overtemperature']:        # Enclosure over temp
        alarm_button_led.blink(on_time=3, off_time=2, n=None, background=True)
        logger.debug('..Controller alarm - enclosure overtemperature.')

    elif controller_status_mimic['alarms']['enclosure_overhumidity']:           # Enclosure over humidity
        alarm_button_led.blink(on_time=3, off_time=4, n=None, background=True)
        logger.debug('..Controller alarm - enclosure overhumidity.')

    elif controller_status_mimic['alarms']['cpu_overtemperature']:              # CPU over temperature
        alarm_button_led.blink(on_time=3, off_time=6, n=None, background=True)
        logger.debug('..Controller alarm - CPU overtemperature.')
        
    elif controller_status_mimic['alarms']['water_level_sensor_offline']:       # Water level sensor offline
        alarm_button_led.blink(on_time=0.1, off_time=10, n=None, background=True)
        logger.debug('..Controller alarm - Water level sensor offline.')
       
    elif controller_status_mimic['alarms']['tamper_switch']:                    # Tamper switch
        alarm_button_led.blink(on_time=0.1, off_time=15, n=None, background=True)
        logger.debug('..Controller alarm - Tamper switch activated.')
       
    elif controller_status_mimic['alarms']['battery_low']:                      # Battery low
        alarm_button_led.blink(on_time=1, off_time=2, n=None, background=True)
        logger.debug('..Controller alarm - Battery low.')
       
    elif controller_status_mimic['alarms']['battery_discharging']:              # Battery discharging
        alarm_button_led.blink(on_time=2, off_time=4, n=None, background=True)
        logger.debug('..Controller alarm - Battery discharging.')
        
    else:
        alarm_button_led.off()
        logger.debug('..No alarms reported from controller.')




# --01-------- The connection acknowledgement callback ----------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    logger.debug("..ON-CONNECT callback processing.")
    if rc == 0:
        logger.debug("..Connected to broker = [" + str(rc) + "] and UserData = [" + str(userdata) + "]")
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
        # The subscribes would be better if we waited for a positive confirmation.

        logger.debug("..Subscribing to various topics.")

        logger.debug("..Subscribe to status messages ................. [" + topic_pump_status + "]")
        client.subscribe(topic_pump_status)

        logger.debug("..Subscribe to water level messages ............ [" + topic_tank_waterlevel + "]")
        client.subscribe(topic_tank_waterlevel)

        logger.debug("..Subscribe to LWT messages from controller..... [" + topic_pump_lwt + "]")
        client.subscribe(topic_pump_lwt)

        client.connected_flag = True
    else:
        logger.debug("ERROR.  Client ON-CONNECT has failed.")


# --02-------- The disconnect callback --------------------------------------------------------------------------------
def on_disconnect(client, userdata, rc):
    logger.debug("Disconnected from broker")
    if rc != 0:
        logger.debug(
            "ERROR.  Unexpected disconnection from broker.  RC [" + str(rc) + "].  Userdata [" + str(userdata) + "]")


# --03-------- The callback when the broker has acknowledged the subscription -----------------------------------------
def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("...Subscription confirmed.  Mid= " + str(mid) + "  Granted QoS= " + str(granted_qos))


# --04-------- The callback for when a message is received from the broker --------------------------------------------
def on_message(client, userdata, msg):
    logger.debug("================> New message received from broker.")
    logger.debug("..Message Topic:    [" + str(msg.topic) + "]")
    logger.debug("..Retained Flag:    [" + str(msg.retain) + "]")
    received_message_payload = msg.payload.decode("utf-8")
        
    #logger.debug("LOOK HERE -------------------------------")
    #logger.debug(received_message_payload)
    #logger.debug("-----------------------------------------")

    # If the message contains no payload (a NULL message) then it may be from an attempt 
    # to purge a retained message on the same topic so simply ignore it
    if received_message_payload == '':
        logger.debug("Ignoring received NULL message.")

    else:
        # Determine the message type and handle each message type appropriately.
        logger.debug("Attempting to parse the received message.")

        if (str(msg.topic) == topic_pump_status):                                      # Pump control command
            #logger.debug("..Message Type:    [Status Update Message]")
            #logger.debug("..Message Payload: " + "[" + received_message_payload + "]")
            process_status_message(received_message_payload)

        elif (str(msg.topic) == topic_tank_waterlevel):                             # Tank water level update
            #logger.debug("..Message Type:     [Update to water level in monitored tank]")
            #logger.debug("..Message Payload:  " + "[" + received_message_payload + "]")
            # This message is JSON, so convert to a dict so we can extract elements
            tank_info_update_data = json.loads(received_message_payload)
            tank_water_status['tank_name'] = tank_info_update_data['tank_name']  
            tank_water_status['tank_waterlevel'] = tank_info_update_data['tank_water_level']
            tank_water_status['tank_waterlevel_lastupdate'] = format(time.time(), '.0f')
            logger.debug(f"Water level in [{tank_info_update_data['tank_name']}] updated to [{tank_info_update_data['tank_water_level']}].")

        elif (str(msg.topic) == topic_pump_lwt):                                    # LWT message
            logger.debug("..Message Type:     [LWT]")
            logger.debug("..Message Payload:  " + "[" + received_message_payload + "]")
            process_controller_offline()

        else:
            logger.debug("Message received on unparsable topic.")      # This should never happen as we only subscribe to selected topics anyway.

        
# --05-------- The MQTT logging callback ------------------------------------------------------------------------------
def on_log(client, userdata, level, buf):
    print("log: ", buf)



# --06-------- The Controller Offline Message handler -----------------------------------------------------------------
def process_controller_offline():
    logger.debug('The broker has issued the LWT message on behalf of the controller.')
    # So the controller has gone offline so the local status LEDs are meaningless so extinguish all of them.
    # Things will be re-established once the controller comes online and sends a status update.
    pump_start_button_led.off()
    pump_stop_button_led.off()
    manual_mode_button_led.off()
    semiauto_mode_button_led.off()
    auto_mode_button_led.off()
    alarm_button_led.on()
    logger.debug('..All local status LEDs have been extinguished except for the Alarm LED.')

    # Set the LWT related flags in the 'broker_supplied_status' dictionary
    # This will prevent button press avctions during this offline time
    broker_supplied_status['lwt_offline'] = True
    broker_supplied_status['lwt_offline_timestamp'] = time.time()
    
    


# ---- Simple dump of these dictionaries
def decorativeStatusDumper(argSource):
    logger.debug(f'=========== MIMIC SYSTEM STATUS DUMP ======[{argSource}]=============')
    try:
        logger.debug(' General system -------------------------------------')
        logger.debug(f"  Publish timestamp                             {controller_status_mimic['controller_run_state']['publish_timestamp']}")
        logger.debug(f"  Publish requester                             {controller_status_mimic['controller_run_state']['publish_requester']}")
        logger.debug(f"  Pump Controller run state                     {controller_status_mimic['controller_run_state']['run_mode']}")
        logger.debug(f"  Run state last changed by                     {controller_status_mimic['controller_run_state']['run_mode_changed_by']}")
        logger.debug(f"  Run state changed at time                     {float(controller_status_mimic['controller_run_state']['run_mode_changed_time']):.0f}")
        logger.debug(' Pump conditions ------------------------------------')
        logger.debug(f"  Pump run state                                {controller_status_mimic['pump_run_state']['pump_running']}")
        logger.debug(f"  Pump fault state                              {controller_status_mimic['pump_run_state']['pump_fault']}")
        logger.debug(' Power state ----------------------------------------')
        logger.debug(f"  Phase 1 AC Power                              {controller_status_mimic['power_state']['phase1_present']}")
        logger.debug(f"  Phase 2 AC Power                              {controller_status_mimic['power_state']['phase2_present']}")
        logger.debug(f"  Phase 3 AC Power                              {controller_status_mimic['power_state']['phase3_present']}")
        logger.debug(' Controller Environment state ------------------------')
        logger.debug(f"  Controller Run sequence number                {controller_status_mimic['environment_state']['run_sequence']}")
        logger.debug(f"  Controller Change detected flag               {controller_status_mimic['environment_state']['change_detected']}")
        logger.debug(f"  Controller CPU temperature                    {float(controller_status_mimic['environment_state']['cpu_temperature']):.1f}")
        logger.debug(f"  Controller Enclosure temperature              {float(controller_status_mimic['environment_state']['enclosure_temperature']):.1f}")
        logger.debug(f"  Controller Enclosure humidity                 {float(controller_status_mimic['environment_state']['enclosure_humidity']):.0f}")
        logger.debug(' Controller Alarms -----------------------------------')
        logger.debug(f"  Controller Enclosure over-temperature alarm   {controller_status_mimic['alarms']['enclosure_overtemperature']}")
        logger.debug(f"  Controller Enclosure over-humidity alarm      {controller_status_mimic['alarms']['enclosure_overhumidity']}")
        logger.debug(f"  Controller CPU over-temperature alarm         {controller_status_mimic['alarms']['cpu_overtemperature']}")
        logger.debug(f"  Controller Water level sensor offline         {controller_status_mimic['alarms']['water_level_sensor_offline']}")
        logger.debug(f"  Controller Tamper switch                      {controller_status_mimic['alarms']['tamper_switch']}")
        logger.debug(f"  Controller Low Battery alarm                  {controller_status_mimic['alarms']['battery_low']}")
        logger.debug(f"  Controller Battery discharging alarm          {controller_status_mimic['alarms']['battery_discharging']}")
        logger.debug(' Broker advised LWT status ---------------------------')
        logger.debug(f"  LWT status received from broker               {broker_supplied_status['lwt_offline']}")
        logger.debug(f"  LWT received from broker timestamp            {float(broker_supplied_status['lwt_offline_timestamp']):.0f}")
        
        #logger.debug(' Tank and water level ---------------------')
        #logger.debug(f"  Tank Name                         {tank_water_status['tank_name']}")
        #logger.debug(f"  Tank Water Level                  {tank_water_status['tank_waterlevel']}")
        #logger.debug(f"  Tank Water Level updated at       {tank_water_status['tank_waterlevel_lastupdate']}")
    except:
        logger.error('ERROR.  An error occurred during this logging attempt.  This is non critcal and has been bypassed.')
    logger.debug('=================================================================\n')



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
    # Broker to connect to
    mqtt_broker_name =      data['broker_configuration']['broker_name']
    mqtt_broker_port =      data['broker_configuration']['broker_port']
    mqtt_broker_timeout =   data['broker_configuration']['broker_timeout']
    # Station details for this station
    local_station_name =    data['station_configuration']['mqtt_station_name']
    mqtt_user_name =        data['station_configuration']['mqtt_user_name']
    mqtt_user_password =    data['station_configuration']['mqtt_user_password']
    mqtt_station_alias =    data['station_configuration']['mqtt_station_alias']
    # Subscribe topics
    topic_pump_status    =  data['subscribe_topic_names']['topic_pump_status']
    topic_pump_lwt       =  data['subscribe_topic_names']['topic_pump_lwt']
    topic_tank_waterlevel = data['subscribe_topic_names']['topic_tank_waterlevel']
    # Publish topics
    topic_pump_cmd =        data['publish_topic_names']['topic_pump_cmd']
    topic_local_status  =   data['publish_topic_names']['topic_local_status']

    nix_data_parking_area = data['backup_data_handling']['nix_data_parking_area']
    win_data_parking_area = data['backup_data_handling']['win_data_parking_area']

    enclosure_temp_alarm_base_value      = data['environment_thresholds']['enclosure_temp_alarm_setting']
    enclosure_humidity_alarm_base_value  = data['environment_thresholds']['enclosure_humidity_alarm_setting']
    cpu_temp_alarm_base_value            = data['environment_thresholds']['cpu_temp_alarm_setting']
    battery_low_voltage_alarm_base_value = data['environment_thresholds']['battery_low_voltage_alarm_setting']

    # Time threshold for alarms
    status_freshness_threshold = data['alarm_thresholds']['status_freshness_threshold']

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




# ---- Use the python logging system to write log messages (advanced method).
# This config still has a problem suppressing the INA219 debug messages fromthe console.  Cannot seem to stop this rot.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s \t%(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)





logger.debug("---------------------------------------------------------------------------- ")  # Readability only
logger.debug("---------- Script Startup ---------- " + "[" + os.path.basename(__file__) + "] -----")
logger.debug("Config was retrieved from YAML [" + filepath + "]")

logger.debug("Script name is  [" + str(sys.argv[0]) + "]")
logger.debug("OS detected as  [" + os_type + "]")

# ---- Sequence the LEDs
led_startup_sequence()



# ---- Build the big dictionaries to hold all the status values and mode control and alarms
'''
    The controller_status_mimic describes the status of the controller itself.
    This entire object is reported any time an alarm occurs on the controller or the broker 
    requests a status report.
    
    The local_system_status describes the status of this system.
    Both have environmental alarms.
    The float values such as temperature are initialised to zero (although thia is never going to be a valid
    reading) just so the print finction does not barf at printing '' as a float.  Probably a better way to do this.
'''
controller_status_mimic = {
    'controller_run_state':{
        'publish_timestamp': 0,
        'publish_requester': '',
        'run_mode':'',
        'run_mode_changed_by':'',
        'run_mode_changed_time':''
    },
    'power_state':{
        'phase1_present':'', 
        'phase2_present':'',
        'phase3_present':''
    },
    'pump_run_state':{
        'pump_running':'',
        'pump_fault':''
    },
    'fronius_state':{
        'fronius_1':'',
        'fronius_2':'',
        'fronius_3':'', 
        'fronius_4':''
    },
    'environment_state':{
        'run_sequence':0,
        'change_detected': 0,
        'cpu_temperature': 0,
        'enclosure_temperature': 0,
        'enclosure_humidity': 0
    },
    'alarms':{
        'enclosure_overtemperature':0,
        'enclosure_overhumidity':0,
        'cpu_overtemperature':0,
        'water_level_sensor_offline':0,
        'tamper_switch':0,
        'battery_low':0,
        'battery_discharging':0
    },
    'power':{
        'supply_voltage'  :'',
        'supply_current'  :'',
        'battery_voltage' :'',
        'battery_current' :'',
        'load_voltage'    :'',
        'load_current'    :''
    }
}

local_system_status = {
    'environment_state':{
        'run_sequence':0,
        'change_detected': 0,
        'cpu_temperature': 0,
        'enclosure_temperature': 0,
        'enclosure_humidity': 0
    },
    'alarms':{
        'enclosure_overtemperature':0,
        'enclosure_overhumidity':0,
        'cpu_overtemperature':0
    },
}

# This dictionary captures the LWT event
broker_supplied_status = {
    'lwt_offline': '',
    'lwt_offline_timestamp': 0
}


# ---- Build this dictionary to hold tank water level data received from the broker
tank_water_status = {
    'tank_name': '',
    'tank_waterlevel': '',
    'tank_waterlevel_lastupdate': ''
}

# ---- Set the water level last updated timestamp to 0 to indicate it has never been updated.
tank_water_status['tank_waterlevel_lastupdate'] = 0
tank_water_status['tank_waterlevel'] = 0        # Just so we have a defined value


# ---- Build this dictionary to hold commands sent to the controller
cmd_message_payload = {
        'publish_timestamp': 0,
        'publish_requester': '',
        'command_source': '',
        'command_code': ''
    }
cmd_message_payload['command_source'] = mqtt_station_alias


# ---- Register the callbacks for the button presses
logger.debug("Registering callbacks for button presses.")
pump_start_button.when_pressed = pump_start_button_pressed
pump_stop_button.when_pressed = pump_stop_button_pressed

manual_mode_button.when_pressed = manual_mode_button_pressed
semiauto_mode_button.when_pressed = semiauto_mode_button_pressed
automatic_mode_button.when_pressed = automatic_mode_button_pressed
alarm_button.when_pressed = alarm_button_pressed



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
logger.debug('..Establishing MQTT connection to broker.')
client.connect(mqtt_broker_name, mqtt_broker_port, mqtt_broker_timeout)
connect_start_time = time.time()
while not client.connected_flag:
    logger.debug("...Waiting for successful client connection to MQTT broker")
    time.sleep(0.5)
connect_stop_time = time.time()
logger.debug("..Client successfully connected to MQTT broker.")
logger.debug(f'..Time taken for broker connect was about {connect_stop_time - connect_start_time:.1f} seconds.')



# ---- Set the initial condition of the Alarm LED and send an initial 'request status update' message.  
# Rely on the ensuing status message to set the new LED status.
alarm_button_led.blink(on_time=0.03, off_time=5.0, n=None, background = True)    # Gives a slow flash

cmd_message_payload['command_code'] = 2          # 2 = Request status update
logger.debug("..Publish an initial 'send status update' message.")
x = client.publish(topic_pump_cmd, payload=json.dumps(cmd_message_payload), qos=0, retain=False)
logger.debug("..Publish result = " + str(x))


# ---- Start the scheduler
logger.debug("Now starting all scheduled tasks.")
schedule.every(1).minutes.do(jobMinuteHousekeeping)             # Should run every minute to check for local environment alarms



while True:
    if local_system_status['environment_state']['change_detected']:

        logger.debug("Some monitored status has changed")
        decorativeStatusDumper("while true loop")

        local_system_status['environment_state']['change_detected'] = False       # Clear the change detected flag

    time.sleep(1)
    schedule.run_pending()

# That is the end!
