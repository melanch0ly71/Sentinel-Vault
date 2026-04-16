**Sentinel Vault 🛡️**  
Advanced Folder Encryption & Identity Management Suite

Sentinel Vault is a modular security utility designed for local data confidentiality and integrity. It leverages AES-256-GCM authenticated encryption to transform sensitive directories into secure .sentinel payloads while managing user access through a custom Identity and Access Management (IAM) layer.

📁 **Repository Structure**  
**src/:** The core source code. This contains the cryptographic engine, processing logic, and the CustomTkinter UI. (For Technical Review)

**bin/:** The compiled, standalone Windows executable. (For Deployment/Testing)

**identity/:** Database schemas and user authentication logic.

**core/:** AES-GCM implementation and ZIP-stream processing.

🚀 **Key Security Features**  
Authenticated Encryption (AEAD): Implements AES-256-GCM, providing both confidentiality and built-in tamper detection (Integrity).  

Secure Key Derivation: Uses PBKDF2-HMAC-SHA256 with unique salts to derive encryption keys from user passwords.

Forensic-Resistant Locking: Automatically compresses and encrypts target folders, followed by a secure deletion of the original cleartext source.

Local IAM: A standalone SQLite-backed identity manager that handles user registration and verification.

**🛠️ Technical Stack**
Language: Python 3.10+

Cryptography: PyCryptodome

GUI Framework: CustomTkinter

Database: SQLite3

Binary Packaging: PyInstaller

**⚙️ Installation & Usage**  

**For Users (Executable)**  
1. Navigate to the /bin folder.  
2. Download and run SentinelVault.exe.  
Note: Due to the tool's encryption and file-deletion capabilities, Windows Defender may trigger a heuristic alert. This is expected behavior for a security utility.


**For Developers (Source)**

1. Clone the repository:  
Bash
git clone https://github.com/yourusername/Sentinel-Vault.git
2. Install dependencies:
Bash
pip install pycryptodome customtkinter
3. Run the application:
Bash
python src/main.py

**🛡️ SOC Analyst Perspective**
This project was developed to demonstrate a practical understanding of the Confidentiality, Integrity, and Availability (CIA) Triad. It addresses common data-at-rest vulnerabilities and implements industry-standard cryptographic primitives to mitigate unauthorized access.

Developed by **Inshaal Bin Umar** Cybersecurity Student | Aspiring SOC Analyst Specializing in Incident Response & Threat Analysis
