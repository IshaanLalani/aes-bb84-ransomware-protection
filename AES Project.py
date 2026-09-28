import hashlib
import os
import random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import pandas as pd

# -------------------------------------------------------------
# 1. LOAD DATASET
# -------------------------------------------------------------
labels_file = "MLRan_labels.csv"

try:
  df = pd.read_csv(labels_file)
  print("=" * 60)
  print("MLRan Dataset Loaded Successfully")
  print("=" * 60)

  total_samples = len(df)
  benign_samples = len(df[df["type_label"] == 0])
  ransomware_samples = len(df[df["type_label"] > 0])

  print(f"Total Samples      : {total_samples}")
  print(f"Benign Samples     : {benign_samples}")
  print(f"Ransomware Samples : {ransomware_samples}")

except Exception as e:
  print("Dataset Loading Error (Make sure CSV files are in the same folder):")
  print(e)
  # For fallback/testing without local CSV file:
  df = pd.DataFrame({"type_label": [0, 2]})

# -------------------------------------------------------------
# 2. BB84 PROTOCOL SIMULATION
# -------------------------------------------------------------


def bb84_simulation(n=256):
  alice_bits = [random.randint(0, 1) for _ in range(n)]
  alice_bases = [random.choice(["+", "x"]) for _ in range(n)]

  bob_bases = [random.choice(["+", "x"]) for _ in range(n)]
  bob_results = []

  for i in range(n):
    if alice_bases[i] == bob_bases[i]:
      bob_results.append(alice_bits[i])
    else:
      bob_results.append(random.randint(0, 1))

  sifted_alice = []
  sifted_bob = []
  errors = 0
  total = 0

  for i in range(n):
    if alice_bases[i] == bob_bases[i]:
      sifted_alice.append(alice_bits[i])
      sifted_bob.append(bob_results[i])
      total += 1
      if alice_bits[i] != bob_results[i]:
        errors += 1

  qber = errors / total if total > 0 else 0
  return sifted_alice, sifted_bob, qber


# -------------------------------------------------------------
# 3. SHA-256 PRIVACY AMPLIFICATION & AES ENCRYPTION
# -------------------------------------------------------------


def generate_final_key(sifted_key):
  key_string = "".join(map(str, sifted_key))
  final_key = hashlib.sha256(key_string.encode()).digest()
  return final_key


def encrypt_data(key, plaintext):
  aes = AESGCM(key)
  nonce = os.urandom(12)
  ciphertext = aes.encrypt(nonce, plaintext.encode(), None)
  return nonce, ciphertext


def decrypt_data(key, nonce, ciphertext):
  aes = AESGCM(key)
  plaintext = aes.decrypt(nonce, ciphertext, None)
  return plaintext.decode()


# -------------------------------------------------------------
# 4. RANSOMWARE DETECTION & EMERGENCY RESPONSE
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("Scanning Dataset For Ransomware Samples...")
print("=" * 60)

ransomware_detected = False

for index, row in df.iterrows():
  label = row["type_label"]
  if label > 0:
    ransomware_detected = True
    print("\n" + "=" * 60)
    print("RANSOMWARE DETECTED!")
    print("=" * 60)
    print(f"Dataset Record ID : {index}")
    print(f"Ransomware Type   : {label}")
    print("\nStarting Emergency Key Rotation...")
    print("Running BB84 Quantum Key Distribution Protocol...\n")

    alice_key, bob_key, qber = bb84_simulation()

    print("BB84 RESULTS")
    print("-" * 40)
    print(f"Sifted Alice Key (First 20 Bits): {alice_key[:20]}")
    print(f"Sifted Bob Key (First 20 Bits)  : {bob_key[:20]}")
    print(f"\nQBER Calculation : {round(qber * 100, 2)}%")

    if qber < 0.11:
      print("\nCHANNEL SECURE (QBER < 11% Threshold)")
      final_key = generate_final_key(alice_key)

      print("\nSHA-256 GENERATED KEY")
      print("-" * 40)
      print(final_key.hex())

      message = "Sensitive Company Data - Secured Post-Incident"
      nonce, encrypted = encrypt_data(final_key, message)

      print("\nAES-256-GCM ENCRYPTION")
      print("-" * 40)
      print(f"Original Data  : {message}")
      print(f"Encrypted Data : {encrypted}")

      decrypted = decrypt_data(final_key, nonce, encrypted)
      print(f"\nDecrypted Data : {decrypted}")
      print("\n[✔] Data Protection & Recovery Successful!")
    else:
      print(
          "\nWARNING: High QBER detected! Aborting communication channel"
          " security."
      )
    break

if not ransomware_detected:
  print("No ransomware signatures found in the scanned batch.")