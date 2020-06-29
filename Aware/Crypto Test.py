from cryptography.fernet import Fernet
key = b'pbIbmoD_5JaaZ2Wk7zhr2WazumWEeNB2RgYC7s_7qRI='


cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b"}{P';l?><")   #required to be bytes
print(ciphered_text) 
unciphered_text = (cipher_suite.decrypt(ciphered_text))
print(unciphered_text)


with open('C:/Users/Sam/AppData/Local/Programs/Python/Python38-32/secret_key.bin', 'wb') as file_object:
    file_object.write(key)
    file_object.close()


with open('C:/Users/Sam/AppData/Local/Programs/Python/Python38-32/cryptobin.bin', 'wb') as file_object:
    file_object.write(ciphered_text)
    file_object.close()
    
with open('C:/Users/Sam/AppData/Local/Programs/Python/Python38-32/secret_key.bin', 'rb') as file_object:
    for line in file_object:
        key = line
    file_object.close()
print(key)
   

with open('C:/Users/Sam/AppData/Local/Programs/Python/Python38-32/cryptobin.bin', 'rb') as file_object:
    for line in file_object:
        encryptedpwd = line
    file_object.close()
print('encrypted password:', encryptedpwd)
    


uncipher_text = (cipher_suite.decrypt(encryptedpwd))
normal = bytes(uncipher_text).decode("utf-8")
print(normal)
