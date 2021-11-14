# Import external dependency.
import binascii
import math
from typing import List
from copy import deepcopy

# Import own dependency.

class Keccak:
    """
    Class for interpreting keccak (SHA3) hash algorithm. Can use the SHA3-224, SHA3-256,
    SHA3-384, and SHA3-512 variety.

    Attributes
    ----------
     round : int
        Round in keccak -> 24 round
    round_constant : List[int]
        Constant for each round in keccak.
    rotation_offset : List[int]
        Offset for each rotation in some round.
    r : int
        Rate of Sha3
    c : int
        Capacity of Sha3
    d : int
        Padding of the message
    output_length : int
        Length of the message digest
    original_message: str
        Message before hashed
    byte_message: bytesarray
        Message before hashed in byte representation
    message_digest: str
        Digest message
    byte_message_digest: bytearray
        Digest message in bytes
    """

    def __init__(self, type:str, message:str) -> None:
        """
        Constructor for Keccak class

        Params
        type : str
            Variety of the SHA3 algorithm.
        message : str
            Message to be hashed
        ------
        """
        # Init constant attributes.
        self.round_constants:List[int] = [
            0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
            0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
            0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
            0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
            0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
            0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
        ]
        self.rotation_offsets = [
            [  0,  1, 62, 28, 27, ],
            [ 36, 44,  6, 55, 20, ],
            [  3, 10, 43, 25, 39, ],
            [ 41, 45, 15, 21,  8, ],
            [ 18,  2, 61, 56, 14, ]
        ]
        self.d =  0x06
        self.original_message = message
        self.byte_message = bytearray(message, "utf-8")
        self.message_digest=""
        self.byte_message_digest=bytearray()
        self.round = 24

        # Init dynamic attributes based on type.
        if (type=="SHA3-224"):
            self.r = 1152
            self.c = 448
            self.output_length = 224
        elif (type=="SHA3-256"):
            self.r = 1088
            self.c = 512
            self.output_length = 256
        elif (type=="SHA3-384"):
            self.r = 832
            self.c = 786
            self.output_length = 384
        elif (type=="SHA3-512"):
            self.r = 576
            self.c = 1024
            self.output_length = 512
        else:
            raise Exception("Invalid SHA3 type")
        self.state = bytearray((self.r + self.c) // 8)
    
    def rotation64(self, val, shift_num):
        """
        Rotation for 64 bit.
        """
        return ((val >> (64-(shift_num % 64))) + (val << (shift_num % 64))) % (1 << 64)

    def load64(self, bytearray):
        """
        Load a 64-bit value using the little-endian format.
        """
        res = 0
        for i in range(7,-1,-1):
            res <<= 8
            res |= bytearray[i]
        return res
 

    def store64(self, val):
        """
        Store a 64-bit value using the little-endian (LE) convention.
        """
        res = []
        for _ in range(8):
            res.append(val % 256)
            val >>= 8
        return res
    
    def keccakPermutation(self):
        """
        Permute keccak state.
        """
        # Map current state to 2 dimension 5*5 state 
        mapped_state=[]
        for i in range(5):
            row = []
            for j in range(5):
                row.append(self.load64(self.state[8*(i+5*j):8*(i+5*j)+8]))
            mapped_state.append(row)
        # print("Mapped state")
        # print(mapped_state)
        
        for round_num in range(self.round):
            # θ step
            # Initiate variable
            C = []
            D = []

            # Fill C, D, and modify mapped state value.
            for i in range(5):
                C.append(mapped_state[i][0] ^ mapped_state[i][1] ^ mapped_state[i][2] ^ mapped_state[i][3] ^ mapped_state[i][4])
            for i in range(5):
                D.append(C[(i-1)%5] ^ self.rotation64(C[(i+1)%5], 1))
            for i in range(5):
                row = []
                for j in range(5):
                    row.append(mapped_state[i][j] ^ D[i])
                mapped_state[i] = row

            # ρ and π steps
            # B = deepcopy(mapped_state)
            B = [[0 for i in range (5)] for j in range (5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2*x+3*y)%5] = self.rotation64(mapped_state[x][y], self.rotation_offsets[y][x])
            
            # χ steps.
            for x in range(5):
                for y in range(5):
                    mapped_state[x][y] = B[x][y] ^ ((~B[(x+1)%5][y] & (B[(x+2)%5][y])))

            # ι steps.
            mapped_state[0][0] = mapped_state[0][0] ^ self.round_constants[round_num]
        
        # Map 2 dimension 5*5 state to current state. 
        for i in range(5):
            for j in range(5):
                self.state[8*(i+5*j):8*(i+5*j)+8] = self.store64(mapped_state[i][j])

    def hash(self)->str:
        """
        Hash the current message. Return the message digest, also modify the attributes.
        """
        # Absorbing
        # Calculate num of block used.
        rate_bytes = self.r // 8
        num_of_block = math.ceil(len(self.original_message)/ rate_bytes)

        # Begin absorbing
        for i in range(num_of_block):
            # Last absorption
            if (i == num_of_block-1):
                # Count the message block real size and number of padding required
                message_block_size = len(self.original_message) - (i * rate_bytes)
                diff = rate_bytes - message_block_size
                
                # Xor the state and message.
                message_block = self.byte_message[i*rate_bytes: i*rate_bytes+message_block_size]
                for j in range(message_block_size):
                    self.state[j] ^= message_block[j]
                
                # Xor the state with padding if required.
                for y in range(diff):
                    self.state[j+y] ^= self.d
                
            else:
                # Xor the state and message.
                message_block = self.byte_message[i*rate_bytes: i*rate_bytes+rate_bytes]
                for j in range(rate_bytes):
                    self.state[j] ^= message_block[j]
            
            self.keccakPermutation()
            

        # Begin squeezing
        byte_output_length = self.output_length // 8
        num_of_block = math.ceil(byte_output_length / rate_bytes)

        for i in range(num_of_block):
            # Last squezing
            if (i == num_of_block-1):
                remaining_block = byte_output_length - (i * rate_bytes)
                self.byte_message_digest += self.state[0:remaining_block]
            else:
                self.byte_message_digest += self.state[0:rate_bytes]
                self.keccakPermutation()

        self.message_digest = binascii.hexlify(self.byte_message_digest).upper()
        self.message_digest = self.message_digest.decode("utf-8")
        return self.message_digest   

def main():
    message = "aaaaaaaaaaaaaaaaaaaa"
    keccak = Keccak("SHA3-256", message)
    print(keccak.hash())
    
if __name__ == "__main__":
    main()

# aaaaaaaaaaaaaaaaaaaa
# 255AA50C417EA6C85C15F2D0F7BFECA367E900B8BF7C7C6FEED0C9003C2A9E03
