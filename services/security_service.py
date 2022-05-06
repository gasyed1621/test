# In-built libraries
from base64 import b64decode
import hashlib
import os
# Third-party libraries
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



class SecurityService:
    @staticmethod
    def verify_digital_signature(data, signature, path_to_pubkey):
        '''
            Verifies a Digital Signature.

            Parameters:
            data (string): Data used to generate signature.
            signature (string): Base64 encoded digital signature.
            path_to_pubkey (string): Path to Public Key PEM file.
        
            Returns:
            bool: Validity of digital signature.
        '''
        with open(path_to_pubkey, "rb") as public_key_file:
            public_key = serialization.load_pem_public_key(public_key_file.read())
        signature = b64decode(signature.encode('utf-8'))
        public_key.verify(
            signature,
            data.encode('utf-8'),
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = 20
            ),hashes.SHA256())
        return True

    @staticmethod
    def get_checksum(target_file):
        sha256_hash = hashlib.sha256()
        with open(target_file, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            checksum_apj = sha256_hash.hexdigest()
            return checksum_apj

