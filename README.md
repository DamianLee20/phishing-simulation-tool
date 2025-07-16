# Phishing Simulation Tool (Educational Project)

This project simulates a phishing login page for educational and cybersecurity awareness purposes.

## Features

- Fake login page to simulate credential harvesting
- Logs IP address and browser info of visitors
- Stores submitted usernames and passwords
- Protected dashboard for reviewing logs
- Redirects users after login to a real site (e.g., Google)

## Technologies

- Python 3
- Flask
- Ngrok

## Warning

This project is intended for educational use only in lab environments. Do **not** deploy it publicly or use it in unauthorized scenarios.

## Usage

1. Run the app:
phishing_simulation.py

2. Expose it using Ngrok:
Grok http 5050

3. View logs at:
https://bc852c8f5ed6.ngrok-free.app/dashboard

Use login: `admin` / `admin123`

