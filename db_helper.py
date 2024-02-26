# db_helper.py
import sqlite3

DATABASE_NAME = "network_analysis.db"

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS port_scan_results (
            id INTEGER PRIMARY KEY,
            target TEXT NOT NULL,
            port INTEGER NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS packet_sniffing_results (
            id INTEGER PRIMARY KEY,
            packet_summary TEXT NOT NULL,
            packet_details TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_sweep_results (
            id INTEGER PRIMARY KEY,
            network_address TEXT NOT NULL,
            start_host TEXT NOT NULL,
            end_host TEXT NOT NULL,
            live_hosts TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network_info (
            id INTEGER PRIMARY KEY,
            ip_address TEXT NOT NULL,
            subnet_mask TEXT NOT NULL,
            default_gateway TEXT NOT NULL,
            dns_servers TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_scan_result(target, port, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO port_scan_results (target, port, status)
        VALUES (?, ?, ?)
    ''', (target, port, status))
    conn.commit()
    conn.close()

def insert_packet_sniff_result(packet_summary, packet_details):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO packet_sniffing_results (packet_summary, packet_details)
        VALUES (?, ?)
    ''', (packet_summary, packet_details))
    conn.commit()
    conn.close()
    
def insert_ping_sweep_result(network_address, start_host, end_host, live_hosts):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ping_sweep_results (network_address, start_host, end_host, live_hosts)
            VALUES (?, ?, ?, ?)
        ''', (network_address, start_host, end_host, live_hosts))
        conn.commit()
    except Exception as e:
        print(f"Database insert error: {e}")
    finally:
        conn.close()

def insert_network_info(ip_address, subnet_mask, default_gateway, dns_servers):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO network_info (ip_address, subnet_mask, default_gateway, dns_servers)
        VALUES (?, ?, ?, ?)
    ''', (ip_address, subnet_mask, default_gateway, dns_servers))
    conn.commit()
    conn.close()