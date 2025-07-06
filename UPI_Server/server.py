import socket
import pickle
import threading
import time
from bank import Bank
from blockchain import Blockchain
from upi_machine import UPIMachine
from merchant import Merchant
from user import User

# Initialize state
banks = {}
merchant_objects = {}
user_objects = {}

# Create UPI machine with access to all banks
upi_machine = UPIMachine(banks)

def handle_client(client_socket, addr):
    """Handle client connection and requests"""
    print(f"Connected to {addr}")
    
    while True:
        try:
            # Receive data from client
            data = pickle.loads(client_socket.recv(4096))
            action = data.get('action')
            response = {"status": "error", "message": "Invalid action"}
            
            # Handle different actions based on menu selection
            if action == 'register_bank':
                bank_name = data.get('bank_name')
                if bank_name not in banks:
                    banks[bank_name] = Bank(bank_name)
                response = {"status": "success", "message": f"Bank {bank_name} registered"}
            
            elif action == 'register_merchant':
                bank_name = data.get('bank_name')
                name = data.get('name')
                password = data.get('password')
                ifsc_code = data.get('ifsc_code')
                balance = data.get('balance')
                
                if bank_name not in banks:
                    banks[bank_name] = Bank(bank_name)
                
                bank = banks[bank_name]
                try:
                    mid = bank.register_merchant(name, password, ifsc_code, balance)
                    merchant_objects[mid] = Merchant(mid, name, ifsc_code, balance, upi_machine)
                    response = {"status": "success", "message": f"Merchant registered with MID: {mid}", "mid": mid}
                except ValueError as e:
                    response = {"status": "error", "message": str(e)}
            
            elif action == 'register_user':
                bank_name = data.get('bank_name')
                name = data.get('name')
                password = data.get('password')
                ifsc_code = data.get('ifsc_code')
                mobile = data.get('mobile')
                pin = data.get('pin')
                balance = data.get('balance')
                
                if bank_name not in banks:
                    banks[bank_name] = Bank(bank_name)
                
                bank = banks[bank_name]
                try:
                    uid, mmid = bank.register_user(name, password, ifsc_code, mobile, pin, balance)
                    user_objects[uid] = User(uid, name, ifsc_code, mobile, mmid, balance, pin)
                    response = {"status": "success", "message": f"User registered with UID: {uid}, MMID: {mmid}", 
                               "uid": uid, "mmid": mmid}
                except ValueError as e:
                    response = {"status": "error", "message": str(e)}
            
            elif action == 'view_merchants':
                merchants_data = {}
                for bank_name, bank in banks.items():
                    merchants = bank.get_all_merchants()
                    if merchants:
                        merchants_data[bank_name] = merchants
                response = {"status": "success", "merchants": merchants_data}
            
            elif action == 'view_users':
                users_data = {}
                for bank_name, bank in banks.items():
                    users = bank.get_all_users()
                    if users:
                        users_data[bank_name] = users
                response = {"status": "success", "users": users_data}
            
            elif action == 'generate_vmid':
                mid = data.get('mid')
                vmid = upi_machine.generate_vmid(mid)
                response = {"status": "success", "vmid": vmid}
            
            elif action == 'generate_qr':
                mid = data.get('mid')
                if mid in merchant_objects:
                    merchant = merchant_objects[mid]
                    vmid = merchant.generate_qr_code()
                    response = {"status": "success", "vmid": vmid}
                else:
                    response = {"status": "error", "message": "Merchant not found"}
            
            elif action == 'same_bank_transaction':
                bank_name = data.get('bank_name')
                encrypted_mid = data.get('encrypted_mid')
                mmid = data.get('mmid')
                pin = data.get('pin')
                amount = data.get('amount')
                
                if bank_name not in banks:
                    response = {"status": "error", "message": "Bank not found"}
                else:
                    bank = banks[bank_name]
                    actual_mid, merchant_bank = upi_machine.decrypt_merchant_id(encrypted_mid)
                    
                    if not actual_mid:
                        response = {"status": "error", "message": "Invalid encrypted Merchant ID"}
                    else:
                        success = bank.verify_transaction(mmid, pin, amount, actual_mid)
                        if success:
                            transaction_data = {
                                "from": mmid,
                                "to": actual_mid,
                                "amount": amount,
                                "timestamp": time.time(),
                                "type": "intra-bank"
                            }
                            bank.blockchain.add_transaction(transaction_data)
                            response = {"status": "success", "message": "Transaction Successful!"}
                        else:
                            response = {"status": "error", "message": "Transaction Failed!"}
            
            elif action == 'cross_bank_transaction':
                sender_bank_name = data.get('sender_bank_name')
                merchant_bank_name = data.get('merchant_bank_name')
                encrypted_mid = data.get('encrypted_mid')
                mmid = data.get('mmid')
                pin = data.get('pin')
                amount = data.get('amount')
                
                if sender_bank_name not in banks or merchant_bank_name not in banks:
                    response = {"status": "error", "message": "One or both banks not found"}
                else:
                    sender_bank = banks[sender_bank_name]
                    merchant_bank = banks[merchant_bank_name]
                    actual_mid, _ = upi_machine.decrypt_merchant_id(encrypted_mid)
                    
                    if not actual_mid:
                        response = {"status": "error", "message": "Invalid encrypted Merchant ID"}
                    else:
                        user_found = False
                        for uid, user in sender_bank.users.items():
                            if user["mmid"] == mmid and user["pin"] == pin and user["balance"] >= amount:
                                user_found = True
                                sender_bank.users[uid]["balance"] -= amount
                                merchant_bank.merchants[actual_mid]["balance"] += amount
                                
                                transaction_data = {
                                    "from": mmid,
                                    "to": actual_mid,
                                    "amount": amount,
                                    "timestamp": time.time(),
                                    "type": "cross-bank"
                                }
                                
                                sender_bank.blockchain.add_transaction(transaction_data)
                                merchant_bank.blockchain.add_transaction(transaction_data)
                                response = {"status": "success", "message": "Cross-Bank Transaction Successful!"}
                                break
                        
                        if not user_found:
                            response = {"status": "error", "message": "Transaction Failed! User not found or insufficient funds"}
            
            elif action == 'view_blockchain':
                bank_name = data.get('bank_name')
                if bank_name not in banks:
                    response = {"status": "error", "message": "Bank not found"}
                else:
                    bank = banks[bank_name]
                    blockchain_data = []
                    for block in bank.blockchain.get_chain():
                        block_data = {
                            "index": block.index,
                            "hash": block.hash,
                            "previous_hash": block.previous_hash,
                            "transaction_data": block.transaction_data,
                            "timestamp": block.timestamp
                        }
                        blockchain_data.append(block_data)
                    
                    response = {"status": "success", "blockchain": blockchain_data}
            
            # Send response back to client
            client_socket.send(pickle.dumps(response))
            
        except EOFError:
            print(f"Client {addr} disconnected")
            break
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break
    
    client_socket.close()
    print(f"Connection to {addr} closed")

def start_server():
    # Import here to avoid circular imports
    from merchant import Merchant
    from user import User
    
    global merchant_objects, user_objects
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)  # Allow multiple connections
    print("Server started, waiting for connections...")
    
    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.daemon = True
        client_handler.start()

if __name__ == "__main__":
    start_server()
