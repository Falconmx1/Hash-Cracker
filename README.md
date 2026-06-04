# 🔓 Hash Cracker

Herramienta para crackear hashes **MD5**, **SHA1** y **SHA256** usando un diccionario.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Características
- Soportes: MD5, SHA1, SHA256
- Ataque con diccionario (wordlist)
- Multithreading opcional
- Fácil de usar

## 📦 Instalación
```bash
git clone https://github.com/Falconmx1/Hash-Cracker.git
cd Hash-Cracker
pip install -r requirements.txt  # si usas Python

🎯 Uso
python hash_cracker.py -H 5d41402abc4b2a76b9719d911017c592 -w rockyou.txt

🧪 Ejemplo
$ python hash_cracker.py -H 5d41402abc4b2a76b9719d911017c592 -w wordlists/rockyou.txt
[+] Hash: MD5
[+] Crackeado: hello
