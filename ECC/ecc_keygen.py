# ECC public & private key üretimi

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# ECC private-public key üret
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Key'leri PEM formatında dışa aktar
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Dosyaya kaydet
with open("ecc_private_key.pem", "wb") as f:
    f.write(pem_private)

with open("ecc_public_key.pem", "wb") as f:
    f.write(pem_public)

print("ECC anahtar çifti oluşturuldu ve kaydedildi.")
