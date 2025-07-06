import qrcode
from upi_machine import UPIMachine

class Merchant:
    def __init__(self, mid, name, ifsc, balance,upi_machine):
        self.mid = mid
        self.name = name
        self.ifsc = ifsc
        self.balance = balance
        self.upi_machine = upi_machine    # For VMID and QR code generation

    def generate_qr_code(self):
        """
        Generates a QR code containing the Virtual Merchant ID (VMID).
        """
        vmid = self.upi_machine.generate_vmid(self.mid)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(vmid)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f"{self.mid}_qr.png")
        print(f"QR Code generated for Merchant {self.name}. (Saved as {self.mid}_qr.png)")
        return vmid

    def confirm_transaction(self, status):
        """Displays a confirmation message based on transaction status."""
        if status:
            print("Transaction Successful! Merchant account updated.")
        else:
            print("Transaction Failed! Please check details and try again.")
