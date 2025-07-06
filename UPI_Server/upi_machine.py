from lwc import generate_virtual_merchant_id, encrypt_merchant_id_speck

class UPIMachine:
    def __init__(self, all_banks):
        self.all_banks = all_banks  # Dictionary of bank name -> Bank instance

    def generate_vmid(self, mid):
        return generate_virtual_merchant_id(mid)

    def encrypt_merchant_id(self, mid):
        return encrypt_merchant_id_speck(mid)

    def decrypt_merchant_id(self, encrypted_mid):
        """
        Decrypt across all banks' merchant registries.
        """
        for bank in self.all_banks.values():
            for mid in bank.merchants.keys():
                if self.encrypt_merchant_id(mid) == encrypted_mid:
                    return mid, bank  # Return actual MID and the correct bank
        return None, None
