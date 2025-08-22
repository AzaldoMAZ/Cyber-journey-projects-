#!/usr/bin/env python3
"""
Advanced SSH Honeypot - A professional learning tool to understand cyber attacks
"""

import socket
import threading
import paramiko
import time
import datetime
import os
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

class SSHHoneypot:
    def __init__(self, host='0.0.0.0', port=2222):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        
        # Statistics tracking
        self.stats = {
            'total_attempts': 0,
            'unique_ips': set(),
            'unique_users': set(),
            'start_time': datetime.datetime.now(),
            'last_attack': None
        }
        
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        self.log_file = f'logs/honeypot_{datetime.datetime.now().strftime("%Y%m%d")}.log'
        self.detailed_log_file = f'logs/detailed_{datetime.datetime.now().strftime("%Y%m%d")}.log'
        print(f"{Fore.GREEN}[+] Logging to: {self.log_file}")
        print(f"{Fore.GREEN}[+] Detailed logs to: {self.detailed_log_file}")
    
    def get_ip_info(self, ip):
        """Get geographic information for an IP address"""
        try:
            # Import requests here to handle missing dependency gracefully
            import requests
            
            if ip in ['127.0.0.1', 'localhost', '::1']:
                return {'country': 'Local', 'city': 'Local', 'org': 'Local'}
            
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'org': data.get('org', 'Unknown')
                }
        except ImportError:
            print(f"{Fore.YELLOW}[!] requests library not available, geographic info disabled")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Failed to get geo info: {e}")
        
        return {'country': 'Unknown', 'city': 'Unknown', 'org': 'Unknown'}
    
    def update_stats(self, client_ip, username):
        """Update attack statistics"""
        self.stats['total_attempts'] += 1
        self.stats['unique_ips'].add(client_ip)
        self.stats['unique_users'].add(username)
        self.stats['last_attack'] = datetime.datetime.now()
    
    def print_stats(self):
        """Print current statistics"""
        runtime = datetime.datetime.now() - self.stats['start_time']
        print(f"\n{Fore.CYAN}=== HONEYPOT STATISTICS ===")
        print(f"{Fore.YELLOW}Runtime: {runtime}")
        print(f"{Fore.YELLOW}Total Attacks: {self.stats['total_attempts']}")
        print(f"{Fore.YELLOW}Unique IPs: {len(self.stats['unique_ips'])}")
        print(f"{Fore.YELLOW}Unique Users: {len(self.stats['unique_users'])}")
        if self.stats['last_attack']:
            print(f"{Fore.YELLOW}Last Attack: {self.stats['last_attack'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.CYAN}============================\n")
    
    def log_attack(self, client_ip, username, password):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get geographic information
        geo_info = self.get_ip_info(client_ip)
        
        # Update statistics
        self.update_stats(client_ip, username)
        
        # Console output with colors
        print(f"{Fore.RED}[{timestamp}] LOGIN ATTEMPT - IP: {client_ip} | User: {username} | Pass: {password}")
        print(f"{Fore.CYAN}    Location: {geo_info['city']}, {geo_info['country']} | Org: {geo_info['org']}")
        
        # Basic logging
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp},{client_ip},{username},{password},LOGIN_ATTEMPT\n")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to write to log file: {e}")
        
        # Detailed logging
        detailed_log = {
            'timestamp': timestamp,
            'ip': client_ip,
            'username': username,
            'password': password,
            'status': 'LOGIN_ATTEMPT',
            'geography': geo_info,
            'session_id': f"{client_ip}_{int(time.time())}"
        }
        
        try:
            with open(self.detailed_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(detailed_log) + '\n')
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to write to detailed log file: {e}")
    
    def handle_connection(self, client, addr):
        client_ip = addr[0]
        print(f"{Fore.BLUE}[+] New connection from {client_ip}")
        
        try:
            t = paramiko.Transport(client)
            t.add_server_key(paramiko.RSAKey(filename='server.key'))
            
            server = SSHServer(self, client_ip)
            t.start_server(server=server)
            
            channel = t.accept(20)
            if channel is None:
                print(f"{Fore.YELLOW}[-] No channel received from {client_ip}")
                return
            
            # Wait for authentication
            server.event.wait(10)
            if not server.event.is_set():
                print(f"{Fore.YELLOW}[-] Client {client_ip} never authenticated")
                return
            
            # Give them a realistic fake shell
            welcome_msgs = [
                b'Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-74-generic x86_64)\r\n',
                b'\r\n',
                b' * Documentation:  https://help.ubuntu.com/\r\n',
                b' * Management:     https://landscape.canonical.com\r\n',
                b' * Support:        https://ubuntu.com/advantage\r\n',
                b'\r\n',
                b'Last login: Mon Aug 21 20:15:32 2023 from 192.168.1.100\r\n',
                b'root@honeypot:~# '
            ]
            
            for msg in welcome_msgs:
                channel.send(msg)
                time.sleep(0.1)  # Small delay for realism
            
            # Keep connection alive and handle commands
            while True:
                try:
                    data = channel.recv(1024)
                    if not data:
                        break
                        
                    command = data.decode('utf-8', errors='ignore').strip()
                    if command:
                        print(f"{Fore.MAGENTA}[CMD] {client_ip}: {command}")
                        
                        # Simulate command responses
                        if command.lower() in ['ls', 'dir']:
                            channel.send(b'\r\nbin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var\r\n')
                        elif command.lower() == 'pwd':
                            channel.send(b'\r\n/root\r\n')
                        elif command.lower() == 'whoami':
                            channel.send(b'\r\nroot\r\n')
                        elif command.lower() in ['uname', 'uname -a']:
                            channel.send(b'\r\nLinux honeypot 5.4.0-74-generic #83-Ubuntu SMP Sat May 8 02:35:39 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux\r\n')
                        elif command.lower() == 'id':
                            channel.send(b'\r\nuid=0(root) gid=0(root) groups=0(root)\r\n')
                        elif command.lower() in ['exit', 'quit', 'logout']:
                            channel.send(b'\r\nlogout\r\n')
                            break
                        elif command.lower() == 'ps':
                            channel.send(b'\r\n  PID TTY          TIME CMD\r\n 1234 pts/0    00:00:01 bash\r\n 5678 pts/0    00:00:00 ps\r\n')
                        elif command.lower() == 'cat /etc/passwd':
                            channel.send(b'\r\nroot:x:0:0:root:/root:/bin/bash\r\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\r\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\r\n')
                        else:
                            channel.send(b'\r\nbash: ' + command.encode('utf-8', errors='ignore') + b': command not found\r\n')
                        
                        channel.send(b'root@honeypot:~# ')
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"{Fore.RED}[-] Error handling command: {e}")
                    break
            
        except Exception as e:
            print(f"{Fore.RED}[-] Connection error with {client_ip}: {e}")
        finally:
            try:
                client.close()
            except:
                pass
            print(f"{Fore.BLUE}[-] Connection closed from {client_ip}")
    
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(100)
            
            self.running = True
            print(f"{Fore.GREEN}[+] Advanced SSH Honeypot listening on {self.host}:{self.port}")
            print(f"{Fore.CYAN}[*] Waiting for connections...")
            print(f"{Fore.CYAN}[*] Press Ctrl+C to stop")
            
            while self.running:
                try:
                    client, addr = self.server_socket.accept()
                    client_handler = threading.Thread(target=self.handle_connection, args=(client, addr))
                    client_handler.daemon = True
                    client_handler.start()
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}[!] Shutting down...")
                    self.running = False
                    break
                except Exception as e:
                    if self.running:  # Only print error if we're still supposed to be running
                        print(f"{Fore.RED}[-] Accept error: {e}")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to start server: {e}")
        finally:
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            self.running = False
            print(f"{Fore.GREEN}[+] Honeypot stopped")

class SSHServer(paramiko.ServerInterface):
    def __init__(self, honeypot, client_ip):
        self.honeypot = honeypot
        self.client_ip = client_ip
        self.event = threading.Event()
    
    def check_auth_password(self, username, password):
        # Log all login attempts
        self.honeypot.log_attack(self.client_ip, username, password)
        self.event.set()
        # Always accept to keep attackers engaged
        return paramiko.AUTH_SUCCESSFUL
    
    def check_auth_publickey(self, username, key):
        # Reject public key auth to force password attempts
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        return 'password'
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_shell_request(self, channel):
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def main():
    print(f"{Fore.CYAN}[*] Starting Advanced SSH Honeypot...")
    print(f"{Fore.CYAN}[*] This is a LEARNING TOOL for cybersecurity education")
    print(f"{Fore.YELLOW}[!] Only use this on networks you own or have permission to test")
    
    # Check if server key exists
    if not os.path.exists('server.key'):
        print(f"{Fore.YELLOW}[*] Generating server key...")
        try:
            key = paramiko.RSAKey.generate(2048)
            key.write_private_key_file('server.key')
            print(f"{Fore.GREEN}[+] Server key generated")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to generate server key: {e}")
            return 1
    
    honeypot = SSHHoneypot()
    print(f"{Fore.GREEN}[+] Advanced honeypot initialized!")
    
    try:
        honeypot.start()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Stopped by user")
    except Exception as e:
        print(f"{Fore.RED}[-] Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
    
   