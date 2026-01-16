from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash(Argon2Hasher())

def hash_password(password):
    """ Hash the password """
    return password_hash.hash(password=password)

def verify_password(plain_password: str , hash_password) -> bool:
    """ Verify Password  """

    return password_hash.verify(plain_password, hash_password)


