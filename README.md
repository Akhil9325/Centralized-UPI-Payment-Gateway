🏦 UPI Payment Gateway Simulation
This project simulates a Unified Payment Interface (UPI) payment ecosystem. It includes:
🏦 Multi-bank support with blockchain-backed transactions
🔐 Secure Merchant ID encryption (SPECK cipher)
⚛️ Quantum vulnerability simulation via Shor’s Algorithm
🌐 Client-server architecture using Python sockets

📁 Project Structure for UPI CLIENT
File	       Description
bank.py	       Bank logic: handles merchant/user registration, same-bank transactions
blockchain.py  Minimal blockchain implementation to log transactions
client.py	   Interactive client UI for registering, transacting, and blockchain viewing
lwc.py	       Lightweight SPECK64/128 encryption for Virtual Merchant IDs
quantum.py	   Quantum simulation of Shor’s algorithm for vulnerability demo
user.py	       Represents a user and initiates payments with optional quantum attack sim

🧠 Key Features
Register Users & Merchants with unique IDs, MMIDs, balances, and secure credentials
Same-bank Transactions using MMID and encrypted Merchant ID
Blockchain Ledger per bank using simple chained hash blocks
Virtual Merchant ID (VMID) generation using SPECK64/128 encryption
Quantum Simulation: Showcasing Shor's Algorithm to factor UID/PIN-derived numbers
Command-line UI for testing the complete UPI flow via client.py


🛠️ Setup Instructions
1. Install Dependencies:
pip install qiskit qiskit-aer numpy
2. Run the UPI Client
python client.py
This will launch a menu-driven interface for:
Registering users & merchants
Viewing registered data
Generating encrypted merchant IDs
Simulating transactions
Viewing blockchain ledgers
For each client (Merchant/ User) enter the ip of the Server pc and access the portal

📁 Project Structure for UPI SERVER
1. upi_machine.py:
Defines the UPIMachine class for managing Virtual Merchant IDs (VMIDs) and encrypting/decrypting merchant IDs.
Key Functions: Generate VMIDs, encrypt/decrypt merchant IDs.
2. server.py:
Implements server-side logic to handle client requests for:
Bank, Merchant, and User Registration.
Intra-Bank and Cross-Bank Transactions.
Blockchain Integration: Records transactions securely.
QR Code Generation: Generates QR codes for merchants.
3. merchant.py:
Defines the Merchant class for merchant-specific operations.
Key Features:
Generate QR codes with VMIDs.
Confirm transaction success or failure.
//the other files are same as for the client and have been already mentioned above in the client section


🛠️ Setup Instructions
1. Install Dependencies:
pip install qiskit qiskit-aer numpy
2. python server.py
For each client (Merchant/ User) enter the ip of the Server pc and access the portal
Use a client to interact with the server (e.g., register banks, merchants, users, or perform transactions).
Merchants can generate QR codes using the generate_qr_code() method.


TO RUN(after the dependencies are downloaded):
In UPI_Server run python server.py
In UPI_Client run python client.py
For each client (Merchant/ User) enter the ip of the Server pc and access the portal
