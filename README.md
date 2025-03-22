Shelly Control Script
Deutsch 🇩🇪
Beschreibung

Dieses Python-Skript steuert ein Shelly-Relais basierend auf der Netzeinspeisung eines SolarEdge-Wechselrichters. Wenn eine bestimmte Einspeiseleistung (z. B. 6000 W) für 5 Minuten überschritten wird, wird das Shelly-Gerät aktiviert. Danach wird eine Sperrzeit von 60 Minuten eingehalten, bevor das Gerät erneut ausgelöst werden kann.
Voraussetzungen 📌

    Python 3.8 oder höher muss installiert sein.

    Folgende Python-Pakete werden benötigt:

pip install requests

    SolarEdge Monitoring API Zugang:

        Erstelle ein Konto auf SolarEdge Monitoring.

        Generiere einen API-Schlüssel unter "Admin" → "Zugriffssteuerung" → "API-Schlüssel erstellen".

        Notiere deine Site ID aus dem Dashboard.

    Shelly-Gerät (z. B. Shelly Plus 1 oder Shelly Pro 2):

        Stelle sicher, dass die IP-Adresse des Shelly-Geräts bekannt ist (z. B. 192.168.1.100).

        Stelle sicher, dass die Web-API aktiviert ist.

    USOC-Datenlieferant (falls verwendet):

        API-URL und Auth-Token erforderlich.

Einrichtung 🔧

Bearbeite die Konfigurationsvariablen in shelly_control.py:

`SHELLY_IP = "192.168.1.100"
SOLAREDGE_API_KEY = "DEIN_SOLAREDGE_API_KEY"
SOLAREDGE_SITE_ID = "DEINE_SITE_ID"
USOC_URL = "http://192.168.1.50/api/v2/status"
HEADERS = {"Auth-Token": "DEIN_AUTH_TOKEN"}`

Passe die Schwellwerte an, um das Shelly-Gerät nach deinen Bedürfnissen zu steuern:

TRIGGER_THRESHOLD = 6000  # Einspeisung in Watt
HOLD_TIME = 300  # Mindestdauer in Sekunden
LOCKOUT_TIME = 3600  # Sperrzeit in Sekunden

Starte das Skript:

python shelly_control.py

Englisch 🇬🇧
Description

This Python script controls a Shelly relay based on the grid feed-in from a SolarEdge inverter. If a specified feed-in power (e.g., 6000 W) is exceeded for 5 minutes, the Shelly device is triggered. A lockout period of 60 minutes follows before it can be activated again.
Requirements 📌

    Python 3.8 or later must be installed.

    Required Python packages:

pip install requests

    SolarEdge Monitoring API access:

        Create an account on SolarEdge Monitoring.

        Generate an API key under "Admin" → "Access Control" → "Create API Key".

        Note your Site ID from the dashboard.

    Shelly device (e.g., Shelly Plus 1 or Shelly Pro 2):

        Ensure the IP address of the Shelly device is known (e.g., 192.168.1.100).

        Ensure the Web API is enabled.

    USOC data source (if used):

        API URL and Auth Token required.

Setup 🔧

Edit the configuration variables in shelly_control.py:

SHELLY_IP = "192.168.1.100"
SOLAREDGE_API_KEY = "YOUR_SOLAREDGE_API_KEY"
SOLAREDGE_SITE_ID = "YOUR_SITE_ID"
USOC_URL = "http://192.168.1.50/api/v2/status"
HEADERS = {"Auth-Token": "YOUR_AUTH_TOKEN"}

Adjust the trigger thresholds to control the Shelly device according to your needs:

TRIGGER_THRESHOLD = 6000  # Feed-in power in watts
HOLD_TIME = 300  # Minimum duration in seconds
LOCKOUT_TIME = 3600  # Lockout time in seconds

Run the script:

python shelly_control.py
