import requests
import time
import json
import os
from datetime import datetime

# Configuration (Replace with actual values)
SHELLY_IP = "YOUR_SHELLY_IP"
SOLAREDGE_API_KEY = "YOUR_SOLAREDGE_API_KEY"
SOLAREDGE_SITE_ID = "YOUR_SOLAREDGE_SITE_ID"
PV_API_URL = f"https://monitoringapi.solaredge.com/site/{SOLAREDGE_SITE_ID}/currentPowerFlow.json?api_key={SOLAREDGE_API_KEY}"
LOG_FILE = "shelly_log.txt"

# API URL and Auth Token for USOC value
USOC_URL = "YOUR_USOC_API_URL"
HEADERS = {"Auth-Token": "YOUR_AUTH_TOKEN"}

# Switching Parameters
TRIGGER_THRESHOLD = 6000  # 6 kW feed-in threshold
HOLD_TIME = 300  # 5 minutes of sustained feed-in (in seconds)
LOCKOUT_TIME = 3600  # 60-minute lockout period after activation (in seconds)

start_time = None
last_trigger_time = 0
last_log_reset = None

# Logging function
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    try:
        with open(LOG_FILE, "a", encoding="utf-8", errors='ignore') as file:
            file.write(log_entry + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# Function to reset the log file daily at 01:00 AM
def check_log_reset():
    global last_log_reset
    current_time = datetime.now()
    
    if current_time.hour == 1 and (last_log_reset is None or last_log_reset.date() != current_time.date()):
        try:
            open(LOG_FILE, "w").close()
            log("Log file reset at 01:00 AM.")
            last_log_reset = current_time
        except Exception as e:
            log(f"Error resetting log file: {e}")

# Function to retrieve grid feed-in and battery status
def get_power_flow():
    try:
        response = requests.get(PV_API_URL, timeout=10)
        data = response.json()

        if "siteCurrentPowerFlow" not in data:
            raise KeyError("siteCurrentPowerFlow missing from API response!")

        power_data = data["siteCurrentPowerFlow"]
        
        pv_power = power_data.get("PV", {}).get("currentPower", 0) * 1000  
        grid_power = power_data.get("GRID", {}).get("currentPower", 0) * 1000  
        load_power = power_data.get("LOAD", {}).get("currentPower", 0) * 1000  
        battery_status = power_data.get("STORAGE", {}).get("status", "unknown")  
        battery_power = power_data.get("STORAGE", {}).get("currentPower", 0) * 1000  

        grid_feed_in = grid_power if pv_power > load_power else -grid_power  
        
        return grid_feed_in, battery_status, battery_power
    except Exception as e:
        log(f"Error retrieving PV data: {e}")
        return 0, "unknown", 0

# Function to retrieve USOC value
def get_usoc():
    try:
        response = requests.get(USOC_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("USOC", "N/A")
        else:
            log(f"USOC request error: {response.status_code}")
            return "N/A"
    except Exception as e:
        log(f"Error retrieving USOC value: {e}")
        return "N/A"

# Function to trigger Shelly switch
def trigger_shelly():
    url_on = f"http://{SHELLY_IP}/rpc/Switch.Set?id=0&on=true"
    url_off = f"http://{SHELLY_IP}/rpc/Switch.Set?id=0&on=false"
    
    try:
        response_on = requests.get(url_on, timeout=5)
        if response_on.status_code == 200:
            log("Shelly turned ON!")
        else:
            log(f"Error turning on Shelly: {response_on.status_code}")
        
        time.sleep(5)
        response_off = requests.get(url_off, timeout=5)
        if response_off.status_code == 200:
            log("Shelly turned OFF!")
        else:
            log(f"Error turning off Shelly: {response_off.status_code}")
        return True
    except Exception as e:
        log(f"Error switching Shelly: {e}")
        return False

# Script start logging
grid_power, battery_status, battery_power = get_power_flow()
usoc = get_usoc()
log("SCRIPT STARTED")
log(f"Current grid feed-in: {grid_power} W")
log(f"Battery: {usoc}%")
log(f"Lockout time after activation: {LOCKOUT_TIME//60} minutes")
log("Waiting for 6 kW feed-in for at least 5 minutes...\n")

while True:
    check_log_reset()

    grid_power, battery_status, battery_power = get_power_flow()
    usoc = get_usoc()
    
    log(f"Grid feed-in: {grid_power} W | Battery: {usoc}%")

    current_time = time.time()

    if grid_power >= TRIGGER_THRESHOLD and (current_time - last_trigger_time >= LOCKOUT_TIME):
        if start_time is None:
            start_time = current_time
            log("6 kW grid feed-in reached – Waiting period starts...")
        
        elif current_time - start_time >= HOLD_TIME:
            log("6 kW grid feed-in sustained for 5 minutes – Triggering Shelly!")
            if trigger_shelly():
                last_trigger_time = current_time  
                start_time = None  

    if grid_power < TRIGGER_THRESHOLD:
        if start_time is not None:
            log("Feed-in dropped below 6 kW – Timer reset.")
        start_time = None  

    if current_time - last_trigger_time < LOCKOUT_TIME:
        remaining_lockout = LOCKOUT_TIME - (current_time - last_trigger_time)
        log(f"Lockout active – Shelly can be triggered again in {int(remaining_lockout // 60)} minutes.")

    time.sleep(30)