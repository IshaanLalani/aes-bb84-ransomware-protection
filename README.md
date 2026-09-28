# AES + QKD (BB84) Ransomware Data Protection System

An advanced cybersecurity framework that integrates **AES-256-GCM encryption** with the **BB84 Quantum Key Distribution (QKD)** protocol to automatically execute emergency key rotation and secure sensitive data upon ransomware detection.

---

## 📂 Core Modules & Workflow

1. **Dataset Ingestion Module:** Loads and analyzes the **MLRan dataset** (consisting of 4,880 total samples split into benign and ransomware records) using Python Pandas.
2. **Ransomware Detection Engine:** Scans the dataset via the `type_label` field to identify malicious activity (`type_label > 0`).
3. **BB84 QKD Protocol Simulation:** Automatically triggers emergency key rotation upon threat detection, simulating quantum bit generation, random basis selection, and sifting between Alice and Bob.
4. **Channel Security Verification (QBER):** Calculates the **Quantum Bit Error Rate (QBER)** to check for eavesdropping. Ensures the channel remains secure under the strict $11\%$ error threshold[cite: 6].
5. **Privacy Amplification & Encryption:** Passes the sifted key through **SHA-256** privacy amplification to generate a robust 256-bit key, which is then used to protect sensitive data via **AES-256-GCM** encryption[cite: 6].

---

## ⚙️ Security Thresholds & Logic

* **Ransomware Trigger:** Evaluated using MLRan label classifications ($0 = \text{Benign}$, $1\text{–}4 = \text{Ransomware}$)[cite: 6].
* **QBER Condition:** 
  $$\text{QBER} = \frac{\text{Errors}}{\text{Total Sifted Bits}}$$
  * $\text{QBER} < 11\% \rightarrow \text{Channel Secure \& Proceed}$[cite: 6]
  * $\text{QBER} \ge 11\% \rightarrow \text{Abort Communication}$[cite: 6]
* **Encryption Standard:** Symmetric 256-bit key applied in Galois/Counter Mode (AES-GCM) ensuring confidentiality, integrity, and authentication[cite: 6].

---

## 💻 Code Overview & Implementation

The application is built in Python utilizing core cryptographic and data science libraries[cite: 6].

### 1. Dependencies & Libraries
* `pandas`: For handling and analyzing the MLRan dataset records[cite: 6].
* `cryptography`: Utilizes `AESGCM` primitives for authenticated encryption[cite: 6].
* `hashlib` & `os`: Used for SHA-256 hashing (privacy amplification) and secure random nonce generation[cite: 6].

### 2. Core Script Functions (`main.py`)
* `bb84_simulation(n)`: Simulates quantum bit transmissions, basis matching, and error tracking to produce sifted keys[cite: 6].
* `generate_final_key(sifted_key)`: Applies SHA-256 hashing to transform raw bit lists into a cryptographic 256-bit binary key[cite: 6].
* `encrypt_data(key, plaintext)` / `decrypt_data(key, nonce, ciphertext)`: Manages secure AES-GCM wrapping and unwrapping of sensitive files[cite: 6].

---

## 🏗️ System Architecture & Workflow

```mermaid
flowchart TD
    subgraph Detection Phase
        DS[MLRan Dataset] --> Det[Ransomware Detection type_label > 0]
    end

    subgraph Quantum Key Distribution
        Det --> BB84[BB84 Protocol Simulation]
        BB84 --> Sift[Sifting & QBER Calculation]
        Sift --> Check{QBER < 11%?}
    end

    subgraph Secure Vault
        Check -- Yes --> PA[SHA-256 Privacy Amplification]
        PA --> AES[AES-256-GCM Encryption]
        AES --> Protect[Sensitive Data Protected]
        Check -- No --> Abort[Abort Communication]
    end
