'''
This is the configuration file for the micropython system.
This file is imported into the project to provide configuration data.

The parameters held here are prefixed with 'tsc' (tank sensor config)
for readability only.  It diffentiates them from parameters managed
within the script itself.
'''

# ---- Variables ---------------------------------------------------------------
tsc_processing_interval = 3600      # Delay between readings in seconds
tsc_retry_interval = 60             # Used when LoRaWAN join fails.  Suggest using 600 in production.

# ---- LoRa join attempts
tsc_lora_join_attempts = 10

# ---- AppEUI (for mill_tank application)
tsc_myAppEui = 'XXXXXXXXXXXXXXXX'       # As defined in TTN


# ---- Name of the AppKey file
tsc_appkey_file = "appkeys.json"
