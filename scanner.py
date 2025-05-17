from scapy.all import ARP, Ether, srp
import sqlite3
from datetime import datetime
import socket

DB_NAME = 'scanner.db'
SUBNET = '192.168.1.0/24'  # Adjust to your local network

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

def scan_network(subnet=SUBNET):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for _, received in result:
        hostname = get_hostname(received.psrc)
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "name": hostname if hostname else None,
            "type": None,
            "vlan": None,
            "location": None,
            "status": "online"
        })
    return devices

def save_to_db(devices):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the table if it does not exist (MAC must be unique)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scanned_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            ip TEXT NOT NULL,
            mac TEXT UNIQUE,
            vlan INTEGER,
            location TEXT,
            status TEXT NOT NULL,
            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    for device in devices:
        cursor.execute('''
            INSERT INTO scanned_devices (name, type, ip, mac, vlan, location, status, scan_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(mac) DO UPDATE SET
                name = excluded.name,
                ip = excluded.ip,
                status = excluded.status,
                scan_time = excluded.scan_time
        ''', (
            device["name"],
            device["type"],
            device["ip"],
            device["mac"],
            device["vlan"],
            device["location"],
            device["status"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()
