from bank import Bank
from quantum import run_shors_algorithm

class User:
    def __init__(self, uid, name, ifsc, mobile, mmid, balance, pin):
        self.uid = uid
        self.name = name
        self.ifsc = ifsc
        self.mobile = mobile
        self.mmid = mmid
        self.balance = balance
        self.pin = pin

    def initiate_payment(self, bank, upi_machine, merchant_encrypted_mid, blockchain):
        print(f"User {self.name} is initiating a payment...")
        amount = float(input("Enter the transaction amount: "))
        pin = input("Enter your PIN: ")

        # Simulate quantum vulnerability
        simulate = input("Simulate Shor’s Algorithm attack on your UID and PIN? (yes/no): ").strip().lower()
        if simulate == "yes":
            try:
                composite = int(self.uid[-4:], 16) + int(self.pin)
                run_shors_algorithm(composite)
            except Exception as e:
                print(f"❌ Quantum simulation error: {e}")

        actual_mid, merchant_bank = upi_machine.decrypt_merchant_id(merchant_encrypted_mid)
        if not actual_mid:
            print("Invalid encrypted Merchant ID. Payment aborted.")
            return

        mmid = self.mmid
        if merchant_bank.verify_transaction(mmid, pin, amount, actual_mid):
            print("✅ Payment Authorized and Processed Successfully!")
            transaction_data = {
                "from": mmid,
                "to": actual_mid,
                "amount": amount
            }
            merchant_bank.blockchain.add_transaction(transaction_data)
        else:
            print("❌ Payment Failed. Please check your details or try again.")
