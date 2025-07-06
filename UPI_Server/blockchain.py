import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transaction_data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transaction_data = transaction_data
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.transaction_data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", {"message": "Genesis Block"}, time.time())
        self.chain.append(genesis_block)
        
    def get_chain(self):
        return self.chain

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction_data):
        previous_block = self.get_last_block()
        new_index = previous_block.index + 1
        new_block = Block(new_index, previous_block.hash, transaction_data)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
