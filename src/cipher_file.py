import os

# PyCryptoDome
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

# GLOBAL KEYS, SIZES IN BYTES
AES_KEY_SIZE = 16
RSA_KEY_SIZE = 256
NONCE_SIZE = 16
TAG_SIZE = 16


class CipherException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def gen_rsa_keypair(key_dir):
    if not is_dir(key_dir):
        raise CipherException('Incorrect directory for RSA keypair')

    key = RSA.generate(RSA_KEY_SIZE * 8)  # 2048 bits key
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    write_file(join_to_path(key_dir, 'id_rsa.pk'), private_key)
    write_file(join_to_path(key_dir, 'id_rsa.pubk'), public_key)


def get_rsa_key(key_file, public=True):
    try:
        ext_allowed = 'pubk' if public else 'pk'
        rsa_key = read_file(key_file, ext=[ext_allowed])
        rsa_imp_key = RSA.import_key(rsa_key)

        if public and rsa_imp_key.has_private():
            raise CipherException('Private key provided instead of Public')
        return rsa_imp_key
    except ValueError:
        raise CipherException('Incorrect rsa key format')


def encrypt_key_by_public_key(key, public_key):
    rsa_public_key = PKCS1_OAEP.new(public_key)
    return rsa_public_key.encrypt(key)


def decrypt_key_by_private_key(key, private_key):
    rsa_private_key = PKCS1_OAEP.new(private_key)
    return rsa_private_key.decrypt(key)


def gen_key():
    return Random.get_random_bytes(AES_KEY_SIZE)  # 128 bits key


def is_file(file):
    if not file:
        return False
    return os.path.isfile(file)


def get_dir(file):
    if not file:
        return None
    return os.path.dirname(file)


def is_dir(directory):
    if not directory:
        return False
    return os.path.isdir(directory)


def get_abs_path(path):
    if not path:
        return None
    return os.path.abspath(path)


def get_curr_dir():
    return os.getcwd()


def get_basename(path):
    if not path:
        return None
    return os.path.basename(path)


def get_extension(path):
    return os.path.splitext(path)[1][1:]


def get_file_size(file):
    if not file:
        return None
    return os.path.getsize(file)


def join_to_path(directory, file_name):
    if not directory or not file_name:
        return None
    return os.path.join(directory, file_name)


def read_file(file, num_bytes=None, ext=[], mode='rb'):
    if not is_file(file):
        raise CipherException("Provided file does not exists")
    if ext and not get_extension(file) in ext:
        raise CipherException("Provided file has wrong extension")

    with open(file, mode) as f:
        plaintext = f.read() if not num_bytes else f.read(num_bytes)
    return plaintext


def write_file(file, data, mode='wb'):
    with open(file, mode) as f:
        f.write(data)


def encrypt_file(public_key_path, in_file, out_file=None, chunk_size=64 * 1024):
    if not out_file:
        out_file = in_file + '.enc'
    # Open files
    file_in = open(in_file, 'rb')
    file_out = open(out_file, 'wb')
    # Generate AES key and encrypt it by RSA public key, write it to the file
    aes_key = gen_key()
    public_rsa_key = get_rsa_key(public_key_path)
    c1 = encrypt_key_by_public_key(aes_key, public_rsa_key)
    file_out.write(c1)
    # Write NONCE to the file
    cipher = AES.new(aes_key, AES.MODE_GCM)
    file_out.write(cipher.nonce)
    # Write data to the output file according to chunk size
    data = file_in.read(chunk_size)
    while len(data) != 0:
        encrypted_data = cipher.encrypt(data)
        file_out.write(encrypted_data)
        data = file_in.read(chunk_size)
    # Write TAG to the footer
    tag = cipher.digest()
    file_out.write(tag)
    # Close files
    file_in.close()
    file_out.close()


def decrypt_file(private_key_path, in_file, out_file=None, chunk_size=64 * 1024):
    if not out_file:
        out_file = in_file[:-4]
    # Open files
    file_in = open(in_file, 'rb')
    file_out = open(out_file, 'wb')
    # Decrypt AES key by RSA private key
    c1 = file_in.read(RSA_KEY_SIZE)
    private_rsa_key = get_rsa_key(private_key_path, False)
    aes_key = decrypt_key_by_private_key(c1, private_rsa_key)
    # Read NONCE from the file
    nonce = file_in.read(NONCE_SIZE)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    # Calculate size of the original file
    file_in_size = os.path.getsize(in_file)
    encrypted_data_size = file_in_size - RSA_KEY_SIZE - NONCE_SIZE - TAG_SIZE  # Size without encrypted key, nonce, tag
    # Decrypt data according to chunk size
    for _ in range(
            int(encrypted_data_size / chunk_size)):
        data = file_in.read(chunk_size)
        decrypted_data = cipher.decrypt(data)
        file_out.write(decrypted_data)
    # Read last encrypted data before the footer
    data = file_in.read(
        int(encrypted_data_size % chunk_size))
    decrypted_data = cipher.decrypt(data)
    file_out.write(decrypted_data)
    # Read TAG from the file and verify integrity
    tag = file_in.read(TAG_SIZE)
    try:
        cipher.verify(tag)
    except ValueError:
        file_in.close()
        file_out.close()
        os.remove(out_file)
        raise CipherException('Integrity validation failed')
    # Close files
    file_in.close()
    file_out.close()
