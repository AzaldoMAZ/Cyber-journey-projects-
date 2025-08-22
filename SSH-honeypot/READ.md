# Advanced SSH Honeypot

A professional-grade SSH honeypot designed for cybersecurity education and threat intelligence gathering. This project demonstrates advanced honeypot capabilities including geographic tracking, command simulation, and comprehensive attack logging.

## 🚀 Features

- **SSH Server Simulation** - Realistic Ubuntu server environment
- **Attack Capture** - Logs all login attempts with timestamps
- **Geographic Intelligence** - Tracks attacker locations and organizations
- **Command Simulation** - Responds to basic Linux commands
- **Dual Logging System** - Basic CSV and detailed JSON logs
- **Real-time Statistics** - Live attack monitoring and counters
- **Professional Reporting** - Generate security intelligence reports

## 📊 Attack Intelligence

The honeypot captures:
- Username and password attempts
- IP addresses and geographic data
- Session commands and activities
- Attack timing and frequency patterns
- Connection metadata and session IDs

## ��️ Installation

### Prerequisites
- Python 3.7+
- Windows/Linux/macOS

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/cybersecurity-ssh-honeypot.git
cd cybersecurity-ssh-honeypot

# Install dependencies
pip install paramiko colorama requests

# Run the honeypot
python honeypot.py
```

## 📁 Project Structure

```
cybersecurity-ssh-honeypot/
├── honeypot.py          # Main honeypot application
├── security_report.md   # Professional security report
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── logs/              # Attack logs directory
│   ├── honeypot_YYYYMMDD.log    # Basic attack logs
│   └── detailed_YYYYMMDD.log    # Detailed JSON logs
└── server.key         # SSH server key (auto-generated)
```

## ⚙️ Configuration

### Port Configuration
- **Default Port:** 2222 (configurable in honeypot.py)
- **SSH Protocol:** Full SSH server implementation
- **Authentication:** Password-based (for attack capture)

### Logging Options
- **Basic Logs:** CSV format for quick analysis
- **Detailed Logs:** JSON format with geographic data
- **Real-time Display:** Colored console output
- **File Rotation:** Daily log files

## 📈 Usage Examples

### Start the Honeypot
```bash
python honeypot.py
```

### View Statistics
Press 's' + Enter in the honeypot terminal to see real-time statistics.

### Test Connection
```bash
ssh -p 2222 root@localhost
```

### Analyze Logs
```bash
# Basic logs
Get-Content logs/honeypot_YYYYMMDD.log

# Detailed logs
Get-Content logs/detailed_YYYYMMDD.log
```

## 📊 Sample Output

```
[+] Advanced SSH Honeypot listening on 0.0.0.0:2222
[+] New connection from 192.168.1.100
[2025-08-22 14:21:20] SUCCESS - IP: 192.168.1.100 | User: root | Pass: test123
    Location: New York, USA | Org: Comcast Cable
```

## 🎯 Use Cases

- **Cybersecurity Education** - Learn about attack patterns
- **Threat Intelligence** - Gather real attack data
- **Security Research** - Study attacker behavior
- **Network Monitoring** - Detect unauthorized access attempts
- **Professional Development** - Build cybersecurity skills

## ⚠️ Security Notice

**This is a LEARNING TOOL for cybersecurity education.**
- Only use on networks you own or have permission to test
- Do not deploy on production systems
- Intended for educational and research purposes only
- Use responsibly and ethically

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ��‍�� Author

Created as a cybersecurity learning project to demonstrate advanced honeypot capabilities and professional security tool development.

## �� Acknowledgments

- Built for educational purposes
- Demonstrates real-world cybersecurity skills
- Professional-grade implementation
- Comprehensive documentation and reporting

---

**⭐ Star this repository if you find it helpful for your cybersecurity journey!**
