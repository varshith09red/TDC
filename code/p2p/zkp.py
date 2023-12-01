# from secp256k1Crypto import curve,scalar_mult, point_add
# import random
# import hashlib
# import sys

# secret="Hello"
# if (len(sys.argv)>1):
#   secret=sys.argv[1]

# s=int(hashlib.md5(secret.encode()).hexdigest(),16)

# # Alice generates
# x = random.randint(0, curve.n-1)

# # Alice generates
# xG = scalar_mult(x, curve.g)

# print ("Let's prove that Alice knows x_1 with Fiat Shamir\n")

# chal=str(curve.g)+str(x)+str(xG)
# h=hashlib.md5()
# h.update(chal.encode())


# v= random.randint(0, curve.n-1)
# vG = scalar_mult(v, curve.g)
# c=int(h.hexdigest(),16)

# r=(v-c*x) % (curve.n)

# Vcheck = point_add(scalar_mult(r,curve.g),scalar_mult(c,xG))

# print (f"Value to prove is {x}")
# print (f"\nxG= {xG}")
# print (f"\nv= {v}, vG={vG}")
# print (f"\nr= {r}, c={c}")

# if (vG==Vcheck): print("\nIt has been proven!!!")
# else: print("\nNot proven!!!")


import hashlib
import json
import os
import random
import binascii

zkp_file = 'zkpdatas.json'

class ZKProof:
    def __init__(self, salt = 0):
        self.N = 20
        self.salt = os.urandom(16) if (salt == 0) else salt
        print(f"salt : {self.salt.hex()}")
        self.write_file('N', self.N)
        self.write_file('salt', self.salt.hex())
        self.write_file('salt-decode', binascii.hexlify(self.salt.hex()))
        # return self.salt

    def getSalt(self):
        return self.salt.hex()

    def _hash(self, x, salt):
        return hashlib.sha256(x.encode('utf-8') + salt).hexdigest()

    def generate_proof(self, secret, salt):
        self.secret = secret
        self.v = self._hash(secret, salt)
        self.write_file('v',self.v)
        r = str(random.randint(1, self.N))
        self.x = self._hash(r, salt)
        return self.x

    def get_secret(self):
        return self.secret

    def verify(self, v, response, salt):
        # data = self.read_file()
        # self.v = data.get('v', '')
        print(f"v : {v == self._hash(response, salt)}")
        print(f"v1 : {v}")
        print(f"v2 : {self._hash(response, salt)}")
        return v == self._hash(response, salt)
    
    def read_file(self):
        data = {}
        try:
            with open(zkp_file, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return data
    
    def write_file(self, attr, val):
        try:
            with open(zkp_file, 'r') as f:
                json_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            json_data = {}

        json_data[attr] = val

        with open(zkp_file, 'w') as f:
            json.dump(json_data, f, indent=4)
    

# zkp = ZKProof()

# secret_card = 'spade_two' # Here we define the secret card
# x = zkp.generate_proof(secret_card)
# print('Proof:', x)

# response = input('Enter the card to verify: ')
# print('Verified:', zkp.verify(response))