import socket
import pickle
import time

class UPIClient:
    def __init__(self, server_ip, port=5555):
        self.server_ip = server_ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.port))
            print("Connected to server successfully!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def send_request(self, action, **params):
        try:
            request = {"action": action, **params}
            self.socket.send(pickle.dumps(request))
            response = pickle.loads(self.socket.recv(4096))
            return response
        except EOFError:
            print("Connection lost. Trying to reconnect...")
            self.connect()
            return {"status": "error", "message": "Connection lost during transaction"}
        except Exception as e:
            print(f"Error during request: {e}")
            return {"status": "error", "message": str(e)}
    
    # Methods for bank actions
    def register_bank(self, bank_name):
        return self.send_request('register_bank', bank_name=bank_name)
    
    def register_merchant(self, bank_name, name, password, ifsc_code, balance):
        return self.send_request('register_merchant', 
                               bank_name=bank_name, 
                               name=name, 
                               password=password, 
                               ifsc_code=ifsc_code, 
                               balance=balance)
    
    def register_user(self, bank_name, name, password, ifsc_code, mobile, pin, balance):
        return self.send_request('register_user', 
                               bank_name=bank_name, 
                               name=name, 
                               password=password, 
                               ifsc_code=ifsc_code, 
                               mobile=mobile, 
                               pin=pin, 
                               balance=balance)
    
    def view_merchants(self):
        return self.send_request('view_merchants')
    
    def view_users(self):
        return self.send_request('view_users')
    
    def generate_vmid(self, mid):
        return self.send_request('generate_vmid', mid=mid)
    
    def generate_qr(self, mid):
        return self.send_request('generate_qr', mid=mid)
    
    def same_bank_transaction(self, bank_name, encrypted_mid, mmid, pin, amount):
        return self.send_request('same_bank_transaction', 
                               bank_name=bank_name, 
                               encrypted_mid=encrypted_mid, 
                               mmid=mmid, 
                               pin=pin, 
                               amount=amount)
    
    def cross_bank_transaction(self, sender_bank_name, merchant_bank_name, encrypted_mid, mmid, pin, amount):
        return self.send_request('cross_bank_transaction', 
                               sender_bank_name=sender_bank_name,
                               merchant_bank_name=merchant_bank_name,
                               encrypted_mid=encrypted_mid, 
                               mmid=mmid, 
                               pin=pin, 
                               amount=amount)
    
    def view_blockchain(self, bank_name):
        return self.send_request('view_blockchain', bank_name=bank_name)

def display_menu():
    print("\n=== UPI Payment Gateway Menu ===")
    print("1. Register as Merchant")
    print("2. Register as User")
    print("3. View All Merchants (per Bank)")
    print("4. View All Users (per Bank)")
    print("5. Generate Virtual Merchant ID (Using UPI Machine)")
    print("6. Generate Merchant QR Code")
    print("7. Simulate Same-Bank Transaction")
    print("8. Simulate Cross-Bank Transaction")
    print("9. View Blockchain (per Bank)")
    print("10. Exit")
    
    return input("Enter your choice: ").strip()

def handle_menu_choice(client, choice):
    if choice == "1":
        # Register as Merchant
        bank_name = input("Enter bank name (HDFC/ICICI/SBI): ").strip().upper()
        name = input("Enter Merchant Name: ")
        password = input("Enter Password: ")
        ifsc_code = input("Enter IFSC Code: ").strip()
        balance = float(input("Enter Initial Balance: "))
        
        response = client.register_merchant(bank_name, name, password, ifsc_code, balance)
        if response["status"] == "success":
            print(f"✅ {response['message']}")
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "2":
        # Register as User
        bank_name = input("Enter bank name (HDFC/ICICI/SBI): ").strip().upper()
        name = input("Enter User Name: ")
        password = input("Enter Password: ")
        ifsc_code = input("Enter IFSC Code: ").strip()
        mobile = input("Enter Mobile Number: ")
        pin = input("Set a 4-digit PIN: ")
        balance = float(input("Enter Initial Balance: "))
        
        response = client.register_user(bank_name, name, password, ifsc_code, mobile, pin, balance)
        if response["status"] == "success":
            print(f"✅ {response['message']}")
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "3":
        # View All Merchants
        response = client.view_merchants()
        if response["status"] == "success":
            merchants_data = response.get("merchants", {})
            if not merchants_data:
                print("No merchants registered yet.")
            else:
                for bank_name, merchants in merchants_data.items():
                    print(f"\n--- Merchants for {bank_name} ---")
                    for mid, details in merchants.items():
                        print(f"Merchant ID: {mid}")
                        print(f"Name: {details['name']}")
                        print(f"IFSC: {details['ifsc']}")
                        print(f"Balance: {details['balance']}")
                        print("-" * 30)
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "4":
        # View All Users
        response = client.view_users()
        if response["status"] == "success":
            users_data = response.get("users", {})
            if not users_data:
                print("No users registered yet.")
            else:
                for bank_name, users in users_data.items():
                    print(f"\n--- Users for {bank_name} ---")
                    for uid, details in users.items():
                        print(f"User ID: {uid}")
                        print(f"Name: {details['name']}")
                        print(f"MMID: {details['mmid']}")
                        print(f"Balance: {details['balance']}")
                        print("-" * 30)
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "5":
        # Generate Virtual Merchant ID
        bank_name = input("Enter bank name for Merchant (HDFC/ICICI/SBI): ").strip().upper()
        mid = input("Enter your Merchant ID: ").strip()
        response = client.generate_vmid(mid)
        if response["status"] == "success":
            print(f"Virtual Merchant ID (VMID): {response['vmid']}")
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "6":
        # Generate QR Code
        bank_name = input("Enter bank name for Merchant (HDFC/ICICI/SBI): ").strip().upper()
        mid = input("Enter your Merchant ID: ").strip()
        response = client.generate_qr(mid)
        if response["status"] == "success":
            print(f"QR Code generated with VMID: {response['vmid']}")
            print(f"QR Code saved as {mid}_qr.png")
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "7":
        # Simulate Same-Bank Transaction
        bank_name = input("Enter bank name for transaction (HDFC/ICICI/SBI): ").strip().upper()
        encrypted_mid = input("Enter encrypted Merchant ID from QR code: ").strip()
        mmid = input("Enter your MMID: ").strip()
        pin = input("Enter your PIN: ").strip()
        amount = float(input("Enter transaction amount: "))
        
        response = client.same_bank_transaction(bank_name, encrypted_mid, mmid, pin, amount)
        if response["status"] == "success":
            print(f"✅ {response['message']}")
        else:
            print(f"❌ {response['message']}")
        
    elif choice == "8":
        # Simulate Cross-Bank Transaction
        sender_bank_name = input("Enter sender bank name (HDFC/ICICI/SBI): ").strip().upper()
        merchant_bank_name = input("Enter merchant bank name (HDFC/ICICI/SBI): ").strip().upper()
        encrypted_mid = input("Enter encrypted Merchant ID from QR code: ").strip()
        mmid = input("Enter your MMID: ").strip()
        pin = input("Enter your PIN: ").strip()
        amount = float(input("Enter transaction amount: "))
        
        response = client.cross_bank_transaction(
            sender_bank_name, merchant_bank_name, encrypted_mid, mmid, pin, amount
        )
        if response["status"] == "success":
            print(f"✅ {response['message']}")
        else:
            print(f"❌ {response['message']}")
        
    elif choice == "9":
        # View Blockchain
        bank_name = input("Enter bank name for blockchain view (HDFC/ICICI/SBI): ").strip().upper()
        response = client.view_blockchain(bank_name)
        if response["status"] == "success":
            blockchain = response.get("blockchain", [])
            print(f"\n--- Blockchain Ledger for {bank_name} ---")
            for block in blockchain:
                print(f"Index: {block['index']}, Hash: {block['hash']}")
                print(f"Previous Hash: {block['previous_hash']}")
                print(f"Transaction: {block['transaction_data']}")
                print(f"Timestamp: {block['timestamp']}")
                print("=" * 40)
        else:
            print(f"❌ Error: {response['message']}")
        
    elif choice == "10":
        # Exit
        print("Exiting...")
        return False
    else:
        print("Invalid choice! Try again.")
    
    return True

def start_client():
    print("=== UPI Payment System Client ===")
    server_ip = input("Enter the server IP address: ")
    client = UPIClient(server_ip)
    
    if not client.connect():
        print("Failed to connect to server. Exiting...")
        return
    
    running = True
    while running:
        choice = display_menu()
        running = handle_menu_choice(client, choice)
    
    print("Thank you for using UPI Payment System!")

if __name__ == "__main__":
    start_client()
