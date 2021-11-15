from typing import List
from sympy import randprime, mod_inverse
from math import gcd
import random

class RSA:
    @staticmethod
    def generateKey() -> List[List[int]]:
        random_prime=[randprime(1,46341), randprime(1,46341)]
        n = random_prime[0] * random_prime[1]
        while(n>2147483647):
            random_prime=[randprime(1,46341), randprime(1,46341)]
            n = random_prime[0] * random_prime[1]
        totient_n = (random_prime[0]-1)*(random_prime[1]-1)
        e = random.choice(range(1,2147483647))
        while(gcd(e, totient_n)!=1):
            e = random.choice(range(1,2147483647))
        d = mod_inverse(e, totient_n)
        public = [e, n]
        private = [d, n]
        return [public, private]

    @staticmethod
    def blockPlainTextToAscii(text:str) -> List[str]:
        block_text = list(text.encode('ascii'))
        return block_text

    @staticmethod
    def blockCipherTextToAscii(text:str) -> List[str]:
        block_text = [text[i:i+10] for i in range(0, len(text), 10)]
        return block_text

    @staticmethod
    def encrypt(text:str, public_key:List[int]) -> str:
        plains_ascii = RSA.blockPlainTextToAscii(text)
        result_ascii = []
        for i in range(len(plains_ascii)):
            plain = plains_ascii[i]
            cipher = pow(plain, public_key[0], public_key[1])
            cipher = str(cipher).zfill(10)
            result_ascii.append(cipher)
        result_ascii = "".join(result_ascii)
        return result_ascii

    @staticmethod
    def decrypt(text:str, private_key:List[int]) -> str:
        ciphers_ascii = RSA.blockCipherTextToAscii(text)
        plain_ascii = []
        for i in range(len(ciphers_ascii)):
            cipher = int(ciphers_ascii[i])
            plain = pow(cipher, private_key[0], private_key[1])
            plain = chr(plain)
            plain_ascii.append(plain)
        plain_ascii = "".join(plain_ascii)
        return plain_ascii

if __name__ == '__main__':
    print("1 for generate, 2 for input key: ")
    mode = int(input())
    if(mode==1):
        key = RSA.generateKey()
        print("Public Key: ", key[0])
        print("Private Key: ", key[1])
        public = key[0]
        private = key[1]
    else:
        e = int(input("e: "))
        d = int(input("d: "))
        n = int(input("n: "))
        public = [e, n]
        private = [d, n]
    text = input("Masukkan plaintext: ")
    encryptText = RSA.encrypt(text, public)
    print("Encrypted text: ", encryptText)
    decryptText = RSA.decrypt(encryptText, private)
    print("Decrypted text: ", decryptText)

