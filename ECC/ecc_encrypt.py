# Ortak anahtar üzerinden simetrik anahtar oluşturur (AES ile şifreleme yapar)

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import os

### ECC Public Key'i oku (karşı tarafın key'i gibi düşün)
with open("ecc_public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

### Yeni geçici bir ECC private key üret (senin tarafın)
private_key = ec.generate_private_key(ec.SECP256R1())

### Paylaşılan anahtarı üret (ECDH)
shared_key = private_key.exchange(ec.ECDH(), public_key)

### AES anahtarı türet
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'ecc_demo'
).derive(shared_key)

### ornek.txt dosyasını oku
with open("ornek_ECC.txt", "rb") as f:
    plaintext = f.read()

### AES ile şifrele (CBC + padding)
iv = get_random_bytes(16)
cipher = AES.new(derived_key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

### Çıktıyı dosyaya yaz (iv + ciphertext)
with open("sifreli-ornek_ECC.enc", "wb") as f:
    f.write(iv + ciphertext)

print("ornek_ECC.txt dosyası başarıyla şifrelendi → sifreli-ornek_ECC.enc")
