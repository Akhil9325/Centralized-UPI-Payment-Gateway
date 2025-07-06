import hashlib
import time
from blockchain import Blockchain  # Ensure blockchain.py is in the same directory

class Bank:
    banks = {
        "HDFC": ["HDFC001", "HDFC002", "HDFC003"],
        "ICICI": ["ICICI001", "ICICI002", "ICICI003"],
        "SBI": ["SBI001", "SBI002", "SBI003"]
    }
    
    def __init__(self, name):
        if name not in Bank.banks:
            raise ValueError("Invalid bank name")
        self.name = name
        self.branches = Bank.banks[name]
        self.merchants = {}
        self.users = {}
        self.blockchain = Blockchain()  # Initialize blockchain ledger

    def generate_mid(self, name, password):
        """Generate a 16-digit unique Merchant ID (MID)"""
        hash_input = f"{name}{password}{time.time()}".encode()
        hash_output = hashlib.sha256(hash_input).hexdigest()[:16]
        return hash_output

    def generate_uid(self, name, password):
        """Generate a 16-digit unique User ID (UID)"""
        hash_input = f"{name}{password}{time.time()}".encode()
        hash_output = hashlib.sha256(hash_input).hexdigest()[:16]
        return hash_output

    def generate_mmid(self, uid, mobile):
        """Generates an MMID by taking the last 6 digits of the UID and mobile number"""
        return uid[-6:] + mobile[-4:]

    def register_merchant(self, name, password, ifsc_code, balance):
        """Registers a merchant and generates a unique MID"""
        if ifsc_code not in self.branches:
            raise ValueError("Invalid IFSC code")
        
        mid = self.generate_mid(name, password)
        self.merchants[mid] = {
            "name": name,
            "ifsc": ifsc_code,
            "balance": balance,
            "password": password
        }
        return mid

    def register_user(self, name, password, ifsc_code, mobile, pin, balance):
        """Registers a user and generates a UID and MMID"""
        if ifsc_code not in self.branches:
            raise ValueError("Invalid IFSC code")
        
        uid = self.generate_uid(name, password)
        mmid = self.generate_mmid(uid, mobile)
        self.users[uid] = {
            "name": name,
            "ifsc": ifsc_code,
            "mobile": mobile,
            "pin": pin,
            "balance": balance,
            "mmid": mmid
        }
        return uid, mmid

    def verify_transaction(self, mmid, pin, amount, merchant_mid):
        """
        Verifies transaction details for same-bank transactions:
          - Checks if the provided MMID and PIN match a registered user
          - Ensures sufficient balance.
          - Deducts the amount from the user and credits the merchant.
          - Logs the transaction in the bank’s blockchain.
        """
        for uid, user in self.users.items():
            # Check using our MMID generation scheme
            if user["mobile"][-4:] in mmid and uid[-6:] in mmid:
                if user["pin"] == pin and user["balance"] >= amount:
                    user["balance"] -= amount
                    self.merchants[merchant_mid]["balance"] += amount
                    transaction_data = {
                        "user_id": uid,
                        "merchant_mid": merchant_mid,
                        "amount": amount,
                        "timestamp": time.time(),
                        "type": "intra-bank"
                    }
                    self.blockchain.add_transaction(transaction_data)
                    return True
        return False

    def get_all_merchants(self):
        """Returns all registered merchants"""
        return self.merchants

    def get_all_users(self):
        """Returns all registered users"""
        return self.users
