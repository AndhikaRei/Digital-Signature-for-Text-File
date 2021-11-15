from rsa import RSA
from keccak import Keccak
from typing import List

class Signature:
  """
  Class for signing a message. Message signing is done with RSA and SHA3 algorithm
  """

  @staticmethod
  def sign(message: str, private_key: List[int]) -> str:
    """
    Get the signature of a given message.
    """
    keccak = Keccak("SHA3-256", message)
    hash = keccak.hash()

    return RSA.encrypt(hash, private_key)

  @staticmethod
  def verify(message: str, signature: str, public_key: List[int]) -> bool:
    """
    Verify signature of a given message and signature.
    """
    keccak = Keccak("SHA3-256", message)
    hash = keccak.hash()

    decrypted = RSA.decrypt(signature, public_key)

    return hash == decrypted

def main():
  message = "Test message 1 2 3"
  print("Message:", message)

  keys = RSA.generateKey()
  print("Keys:", keys)

  signature = Signature.sign(message, keys[1])
  print("Signature:", signature)

  verify = Signature.verify(message, signature, keys[0])
  print("Verify:", verify)
    
if __name__ == "__main__":
  main()