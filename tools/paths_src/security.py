from _lib import *

SEC_FOUND = PH("Security foundations", "Weeks 1–10", "Know how computers and networks work well enough to defend them.", [
  N("Networking fundamentals", "Security is mostly networking. Know how packets get from A to B and what each layer does.", ["OSI & TCP/IP models", "IP addressing & subnets", "TCP vs UDP", "DNS, DHCP, ARP", "common ports"], ["cloudflare-learn", "beej-net"], core="s3m6"),
  N("Linux", "Most servers and security tools run on Linux. Get comfortable at the command line.", ["file system & permissions", "users & groups", "processes", "logs", "bash scripting"], ["linuxjourney", "bandit", "rm-linux"], core="s0m1"),
  N("Windows & Active Directory", "Most corporate networks run Windows with Active Directory, and most breaches touch it.", ["users, groups & GPO", "Active Directory basics", "PowerShell", "event logs"], [("Microsoft Learn: Windows Server", "https://learn.microsoft.com/en-us/windows-server/")]),
  N("Programming for security", "Python and Bash to automate tasks, parse logs and write small tools.", ["Python scripting", "regular expressions", "working with APIs", "Bash"], ["py-tut", "regex"], core="s1m5"),
  N("Core security concepts", "The vocabulary: CIA triad, threats vs vulnerabilities vs risks, defence in depth, least privilege.", ["CIA triad", "risk", "authentication vs authorisation", "defence in depth"], ["cs50sec", "nist-csf"]),
  N("Cryptography basics", "What hashing, encryption and signatures do, and how they go wrong.", ["symmetric vs asymmetric", "hashing", "TLS", "PKI & certificates"], ["cs50sec", "cryptopals"]),
 ], ("Home lab", "Build a virtual lab: a Linux server, a Windows machine and a firewall in VirtualBox or Proxmox. Document the network diagram and harden each machine with a checklist."))

PATH(id="cybersecurity", title="Cybersecurity Analyst", icon="shield", hue="#34d399", cat="Cybersecurity", duration="10–14 months",
 tagline="Defend organisations: detect attacks, respond to incidents, harden systems.",
 about=["Security analysts (the 'blue team') protect organisations. In a Security Operations Centre you'll triage alerts, investigate suspicious activity, respond to incidents and improve detections so the next attack is caught sooner.","Demand is persistent across every industry and government. Curiosity, calm under pressure and clear writing matter as much as tools."],
 day=["Triage alerts in a SIEM", "Investigate suspicious logins, processes and network traffic", "Respond to incidents and write reports", "Tune detections and reduce false positives", "Harden systems and track vulnerabilities"],
 tools=["SIEM (Splunk, Elastic, Sentinel)", "EDR", "Wireshark", "Sysmon", "Sigma rules", "Python", "Linux", "MITRE ATT&CK"],
 roles=["SOC Analyst", "Security Analyst", "Incident Responder", "Threat Hunter", "Detection Engineer"],
 core=["s3m4", "s3m6", "s7m4"],
 phases=[SEC_FOUND,
  PH("Blue-team skills", "Weeks 11–22", "See attacks in logs and traffic.", [
   N("Logs & SIEM", "Collect, search and correlate logs across an organisation.", ["log sources", "SIEM queries (SPL/KQL)", "correlation rules", "dashboards"], ["letsdefend", "thm"]),
   N("Network traffic analysis", "Read packet captures and spot anomalies.", ["Wireshark", "tcpdump", "Zeek", "beaconing"], ["wireshark"]),
   N("Endpoint detection", "What attackers do on a machine and how EDR and Sysmon record it.", ["process trees", "persistence", "Sysmon", "EDR"], ["thm"]),
   N("MITRE ATT&CK", "A shared map of attacker tactics and techniques; the language of detection.", ["tactics vs techniques", "mapping detections", "threat groups"], ["attack"]),
   N("Detection engineering", "Write detections as code and test them against real attack data.", ["Sigma", "YARA", "testing detections", "false positives"], ["sigma"]),
   N("Phishing analysis", "The most common way in. Analyse emails, headers, links and attachments safely.", ["email headers", "URL analysis", "sandboxing"], ["letsdefend"]),
  ], ("Detection lab", "Send logs from your home lab to an open-source SIEM (Elastic or Wazuh), simulate five ATT&CK techniques, and write detections that catch each one with low false positives.")),
  PH("Incident response & governance", "Weeks 23–34", "Handle incidents end to end and speak the language of risk.", [
   N("Incident response lifecycle", "Preparation, detection, containment, eradication, recovery and lessons learned.", ["IR playbooks", "containment", "evidence handling", "post-incident reviews"], [("NIST SP 800-61: Incident handling guide", "https://csrc.nist.gov/pubs/sp/800/61/r2/final")]),
   N("Digital forensics basics", "Collect and analyse evidence from disks, memory and logs.", ["disk images", "memory forensics", "timelines", "chain of custody"], ["thm"]),
   N("Threat intelligence", "Use indicators and reports to anticipate attacks.", ["IOCs vs TTPs", "threat feeds", "CISA KEV"], ["cisa", "attack"]),
   N("Vulnerability management", "Find, prioritise and track fixes for vulnerabilities.", ["scanning", "CVSS", "prioritising by exploitability", "patch cycles"], ["cisa"]),
   N("Governance, risk & compliance", "Frameworks and regulations that shape security programmes.", ["NIST CSF", "ISO 27001", "GDPR basics", "risk registers"], ["nist-csf"]),
   N("Cloud security basics", "Identity, logging and misconfigurations in AWS/Azure.", ["IAM", "cloud logging", "misconfigurations", "shared responsibility"], ["aws-skill", "azure-learn"]),
  ], ("Incident write-up", "Investigate a public practice incident (for example a Blue Team Labs or LetsDefend case) and write a professional report: timeline, impact, root cause and recommendations.")),
  PH("Specialise", "Months 9–14", "Choose a deeper direction.", [
   N("Threat hunting", "Proactively search for attackers that evaded detection.", ["hypotheses", "baselining", "hunting queries"], ["attack"]),
   N("Malware analysis basics", "Static and dynamic analysis in a safe lab.", ["sandboxes", "strings & imports", "behaviour analysis"], ["thm"], opt=True),
   N("Security automation (SOAR)", "Automate repetitive triage with Python and playbooks.", ["SOAR", "APIs", "enrichment scripts"], ["py-tut"]),
   N("Capture the Flag practice", "Keep skills sharp with defensive and forensic CTFs.", ["forensics challenges", "log analysis CTFs"], ["picoctf", "thm"]),
  ]),
 ],
 interview=["Walk through investigating a suspicious login or a phishing email.", "Networking: TCP handshake, DNS, common ports and protocols.", "Explain ATT&CK techniques and how you'd detect one.", "Scenario: ransomware on one laptop. What do you do in the first hour?"],
 certs=["CompTIA Security+ (common entry requirement)", "CompTIA CySA+ or Blue Team Level 1", "GIAC GCIH / GCIA (later)", "Microsoft SC-200 (Sentinel/Defender)"],
 related=["appsec", "cloud", "devops"])

PATH(id="appsec", title="Application Security Engineer", icon="bug", hue="#fbbf24", cat="Cybersecurity", duration="12–16 months",
 tagline="Help developers build software that is secure by design.",
 about=["Application security engineers work alongside development teams so that security is built in from the start: reviewing designs, setting up automated checks in CI, writing secure-coding guidance and helping teams fix issues quickly.","It suits developers who enjoy security, since the job is as much about enabling other engineers as it is about finding problems."],
 day=["Run threat-modelling sessions on new features", "Review code and designs for security issues", "Maintain automated security checks in CI", "Triage reported issues and guide fixes", "Write secure-coding guidelines and training"],
 tools=["SAST tools (Semgrep, CodeQL)", "Dependency scanners", "Secret scanners", "OWASP ASVS", "Threat modelling", "Python", "CI/CD"],
 roles=["Application Security Engineer", "Product Security Engineer", "DevSecOps Engineer", "Security Champion"],
 core=["s4m3", "s4m5", "s5m3", "s7m4"],
 phases=[
  foundations("Python"),
  PH("Web development first", "Weeks 9–18", "You can only secure software you understand how to build.", [
   N("Build a web application", "Build a small app with a backend, database and login so you understand what you'll be reviewing.", ["HTTP & REST", "a web framework", "SQL", "sessions"], ["mdn-http", "fastapi"], core="s4m3"),
   N("Authentication & sessions", "How login, sessions, tokens and permissions are meant to work.", ["password hashing", "session management", "OAuth 2.0", "access control"], ["owasp-cs", "oauth"]),
   N("Core security concepts", "CIA triad, least privilege, defence in depth and trust boundaries.", ["trust boundaries", "least privilege", "defence in depth"], ["cs50sec"]),
  ]),
  PH("Secure development", "Weeks 19–30", "Prevent the most common classes of weakness.", [
   N("OWASP Top 10", "The most common categories of web application risk and how to prevent each.", ["access control", "injection prevention", "security misconfiguration", "logging & monitoring"], ["owasp10", "owasp-cs"]),
   N("Secure coding standards", "Turn guidance into checklists and requirements teams can follow.", ["input validation", "output encoding", "parameterised queries", "ASVS levels"], ["asvs", "owasp-cs"]),
   N("Threat modelling", "Ask 'what could go wrong?' at design time, when fixes are cheapest.", ["data-flow diagrams", "STRIDE", "trust boundaries", "mitigations"], ["tm-manifesto"]),
   N("Code review for security", "Read code with a defender's eye and give actionable fixes.", ["review checklists", "common weakness patterns", "writing clear findings"], ["cwe25", "owasp-cs"], core="s5m3"),
  ], ("Threat model and review", "Threat-model your own web app, review its code against the ASVS, fix what you find and document the decisions.")),
  PH("Security at scale", "Months 8–16", "Make secure the default across many teams.", [
   N("Security in CI/CD", "Automated static analysis, dependency and secret scanning on every pull request.", ["SAST", "dependency scanning", "secret scanning", "triage workflows"], ["semgrep", "gha"]),
   N("Supply-chain security", "Know what you ship and where it came from.", ["SBOMs", "pinning & lockfiles", "signed builds", "SLSA"], ["slsa"]),
   N("Cloud & container hardening", "Secure defaults for infrastructure your apps run on.", ["IAM least privilege", "secrets management", "container image hygiene"], ["docker", "aws-wa"]),
   N("Security programmes", "Champions programmes, training and metrics that improve outcomes.", ["security champions", "developer training", "metrics"], ["nist-csf"]),
  ], ("Secure pipeline", "Add SAST, dependency and secret scanning to a project's CI with clear triage rules, and write a one-page secure-coding guide for its contributors.")),
 ],
 interview=["Review a code snippet and explain the weakness and the fix.", "Threat-model a feature on a whiteboard.", "Explain how you'd roll out security tooling without slowing teams down.", "Web fundamentals: auth, sessions, HTTP and common weakness classes."],
 certs=["CompTIA Security+ (optional)", "ISC2 CSSLP (later, optional)"],
 related=["cybersecurity", "backend", "devops"])
