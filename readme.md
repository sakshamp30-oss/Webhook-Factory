Webhook-Factory
NOT AN IP GRABBER

A Python-based honeytoken factory and threat intelligence dashboard.

This tool generates fake files (like .env configs or HTML login portals) embedded with unique tracking tokens. When a bot or human opens them, the files silently ping a local listener. The listener logs their IP, User-Agent, and geolocation.

It is designed to catch attackers who are already inside your network looking for credentials, without triggering false positives on legitimate users and not to make random links and be used as a ip grabber please.
Features

    Dynamic Traps: Generates .env files with fake AWS keys and HTML pages with hidden 1x1 tracking pixels. Every generated file gets a unique 12-character token.

    Local GeoIP Lookup: Uses MaxMind GeoLite2 databases instead of third-party APIs. Because getting rate-limited by Facebook bots within five minutes of going live is annoying.

    ASN/VPN Detection: Checks the network owner of the incoming IP. If it belongs to a hosting provider or known VPN, it flags it. It won't catch a sophisticated attacker using a residential proxy, but it catches the lazy ones.

    Secret Dashboard: A local web UI to view your captured targets. It's protected by a randomized URL generated on startup, so random people can't browse your threat intel.

Architecture

    The Factory (make_*.py): Generates the trap files and builds the tracking URLs.

    The Listener (server.py): A FastAPI endpoint that catches the incoming webhooks and returns a blank 1x1 PNG so the client doesn't get suspicious.

    The Enrichment (geoip.py): Takes the IP and looks it up in the local MaxMind databases to find the city, country, and ISP.

    The Database (db.py): Logs the data in SQLite.

    The Dashboard: Renders the SQLite data into a basic HTML table.

Setup

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn requests geoip2 user-agents
```
2. Get the GeoIP Databases:
You need the local MaxMind databases for location tracking to work and get which VPN or organisation is being used by the person using vpn. Run these commands in your terminal to download them directly into your data/ folder:
```bash
mkdir -p data
wget -O data/GeoLite2-City.mmdb https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-City.mmdb
wget -O data/GeoLite2-ASN.mmdb https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-ASN.mmdb
```
(If you are on Mac, you might need to use curl -o instead of wget).

3. Start the server:
```bash
uvicorn server:app --reload
```
Check your terminal. The server will print a Dashboard Path: /dashboardXXXXXX. Save that URL; it's the only way to access the web UI. This is done to make reaching the dashboard from unauthorised people impossible or close to impossible as the random string generating has more than 3 sextillion combinations.
4. Generate a trap:
Open a second terminal tab. Pass your public tunnel URL (via ngrok, VS Code Ports, etc.) as an argument. Make sure to include /t/ at the end.
```bash
python make_html_trap.py <paste_your_url_here>
```
or you can create a secrets.env file as well for a trap so run:
```bash
python make_credential.py <paste_your_url_here>
```
The url u get is from porting from vscode or using external tools like ssh, cloudflared or ngrok

5. Deploy:
Move the generated company_login.html or secrets.env file to a location an attacker might look. Monitor your dashboard or database to see who takes the bait.

Disclaimer and Ethical Use

This tool is designed for defensive cybersecurity, educational purposes, and authorized security testing only.

Because this tool logs incoming IP addresses, User-Agents, and geolocates requests, it operates on the exact same technical principles as an ip grabber.

By downloading or using this software, you agree to the following:

    You will only deploy these honeytokens on systems, servers, or networks that you own or have explicit, written permission to test.

    You will not use this tool to track, dox, harass, or deceive individuals without their consent.

    You will comply with all local, state, and international privacy laws regarding the collection and storage of personal data.

    I assume no liability and am not responsible for any misuse, damage, or legal consequences caused by this software. Do not cause any harm using this.

    Made for educational purposes by Saksham Paudel: (https://github.com/sakshamp30-oss)