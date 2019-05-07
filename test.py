from Crypto.Cipher import Salsa20

key = b'*Thirty-two byte (256 bits) key*'

cipher = Salsa20.new(key=key)

nonce = cipher.nonce

plaintext = 'Attack at dawn'.encode()
msg = cipher.encrypt(plaintext)

cipher = Salsa20.new(key=key, nonce=nonce)
msg = cipher.decrypt(msg)

print(msg.decode())
