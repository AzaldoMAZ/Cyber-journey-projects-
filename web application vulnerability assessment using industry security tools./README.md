# Web Application Vulnerability Assessment with Nikto

## Project Overview

This project demonstrates a comprehensive web application security assessment using industry-standard penetration testing tools and methodologies. The assessment was conducted on a deliberately vulnerable web application to identify and document security flaws.

## Objective

**Primary Goal**: Learn and execute web application vulnerability assessment using automated scanning tools and manual verification techniques.

**Learning Outcomes**:
- Understand vulnerability scanning workflows
- Practice manual verification of automated findings
- Develop security reporting and documentation skills
- Gain hands-on experience with Linux-based security tools

## Environment Setup

### System Configuration
- **Operating System**: Ubuntu 20.04 LTS via Windows Subsystem for Linux (WSL)
- **Target**: testphp.vulnweb.com (intentionally vulnerable test application)
- **Assessment Type**: External black-box security testing

### Tools Used
| Tool | Purpose | Version |
|------|---------|---------|
| **Nikto** | Web vulnerability scanner | v2.1.5 |
| **curl** | HTTP client for manual verification | Latest |
| **Linux Terminal** | Command execution environment | Bash |

## Methodology

### Phase 1: Automated Discovery
```bash
# Execute comprehensive vulnerability scan
nikto -h testphp.vulnweb.com -o nikto_scan_results.txt
```

### Phase 2: Manual Verification
```bash
# Verify directory indexing vulnerability
curl -I http://testphp.vulnweb.com/admin/

# Check cross-domain policy configuration
curl http://testphp.vulnweb.com/crossdomain.xml

# Validate missing security headers
curl -I http://testphp.vulnweb.com/ | grep -i "frame\|content\|security"

# Examine exposed files
curl http://testphp.vulnweb.com/admin/create.sql
```

### Phase 3: Impact Analysis
Each identified vulnerability was assessed for:
- **Severity Level** (Critical/High/Medium/Low)
- **Potential Impact** on confidentiality, integrity, and availability
- **Exploitation Difficulty** and attack vectors
- **Remediation Requirements**

## Key Findings

### Critical Vulnerabilities

#### 1. Database Schema Exposure
- **Location**: `/admin/create.sql`
- **Impact**: Complete database structure publicly accessible
- **Risk**: Enables targeted SQL injection attacks and architecture reconnaissance

#### 2. Wildcard Cross-Domain Policy
- **Location**: `/crossdomain.xml`
- **Configuration**: `<allow-access-from domain="*" to-ports="*" secure="false"/>`
- **Impact**: Allows any external domain to make authenticated requests
- **Risk**: Cross-site request forgery and data exfiltration

### High-Risk Issues

#### 3. Directory Indexing Enabled
- **Affected Paths**: `/admin/`, `/images/`
- **Impact**: File system structure enumeration
- **Risk**: Information disclosure and potential access to sensitive files

#### 4. Missing Security Headers
- **Missing Headers**: X-Frame-Options, Content-Security-Policy
- **Impact**: Vulnerable to clickjacking and content injection attacks
- **Risk**: UI redress attacks and malicious content injection

## Technical Evidence

### Nikto Scan Output Sample
```
+ Target IP: [IP_ADDRESS]
+ Target Hostname: testphp.vulnweb.com
+ Target Port: 80
+ GET /: The anti-clickjacking X-Frame-Options header is not present.
+ GET /admin/: Directory indexing found.
+ GET /crossdomain.xml: contains a full wildcard entry.
```

### Manual Verification Results
```bash
# Directory indexing confirmation
HTTP/1.1 200 OK
Content-Type: text/html
<title>Index of /admin/</title>

# Cross-domain policy verification
<?xml version="1.0"?>
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" secure="false"/>
</cross-domain-policy>
```

## Recommendations

### Immediate Actions Required
1. **Disable directory indexing** on web server
2. **Remove or secure** publicly accessible SQL files
3. **Implement restrictive cross-domain policy** with specific domain allowlists
4. **Add security headers** (X-Frame-Options, CSP, HSTS)

### Security Hardening
- Implement proper access controls on administrative directories
- Regular security scanning and penetration testing
- Web application firewall deployment
- Security awareness training for development teams

## Files Structure

```
vulnerability-assessment/
├── README.md
├── nikto_scan_results.txt          # Raw Nikto output
├── final_report.txt                # Executive summary
├── detailed_verification.txt       # Manual testing results
└── remediation_plan.md            # Security recommendations
```

## Learning Outcomes

### Technical Skills Developed
- **Command-line security tools** operation and configuration
- **HTTP protocol** analysis and manipulation
- **Vulnerability assessment** methodology and best practices
- **Security documentation** and professional reporting

### Key Insights
- Automated tools require manual verification to avoid false positives
- Cross-reference multiple information sources when learning new concepts
- Systematic documentation is essential for professional security assessments
- Understanding tool limitations is as important as knowing their capabilities

## Ethical Considerations

This assessment was conducted on:
- **Intentionally vulnerable** test applications designed for educational purposes
- **Publicly available** targets specifically created for security training
- **Controlled environment** with no impact on production systems

## Future Learning Path

### Next Steps
- Advanced manual testing techniques (SQL injection, XSS)
- Web application firewall bypass methods
- Automated reporting and integration workflows
- Mobile application security assessment

### Recommended Resources
- OWASP Web Security Testing Guide
- SANS Penetration Testing methodologies
- Burp Suite Academy training modules
- CTF platforms for practical skill development

## Disclaimer

This project is for **educational purposes only**. All testing was conducted on designated vulnerable applications designed for learning. Do not attempt these techniques on systems you do not own or have explicit permission to test.

---

**Author**: Security Student  
**Date**: August 2025  
**Environment**: Ubuntu on WSL  
**Status**: Learning Project - Building Cybersecurity Foundations
