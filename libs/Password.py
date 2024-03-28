import hashlib

class Password(object):
    def __init__(self, args1):
        self.args1 = args1
    
    def sha512(self):
        password = self.args1

        bytes_string = password.encode('utf-8')
        sha512_hash = hashlib.sha512()

        sha512_hash.update(bytes_string)
        hashed_string = sha512_hash.hexdigest()

        return hashed_string

if __name__=="__main__":
    hash_pass = Password("margonda100").sha512()
    print(hash_pass)


