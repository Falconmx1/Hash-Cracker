import subprocess
import os
import tempfile
import sys

# Mapeo de algoritmos a códigos de hashcat
HASHCAT_MODES = {
    'md5': 0,
    'sha1': 100,
    'sha224': 1300,
    'sha256': 1400,
    'sha384': 10800,
    'sha512': 1700,
    'blake2b': 600,
    'blake2s': 610
}

def check_hashcat():
    """Verifica que hashcat esté instalado"""
    try:
        subprocess.run(['hashcat', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def crack_with_gpu(target_hash, wordlist_path, algorithm):
    """Usa hashcat para cracking con GPU"""
    if not check_hashcat():
        print("[-] Hashcat no está instalado o no está en PATH")
        print("[!] Instálalo: sudo apt install hashcat (Linux) o desde https://hashcat.net/hashcat/")
        return None
    
    mode = HASHCAT_MODES.get(algorithm)
    if not mode:
        print(f"[-] Algoritmo {algorithm} no soportado en hashcat")
        return None
    
    # Crear archivo temporal con el hash
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(target_hash)
        hash_file = f.name
    
    # Comando hashcat
    cmd = [
        'hashcat', '-m', str(mode), '-a', '0',
        hash_file, wordlist_path,
        '--quiet', '--force',  # --force para evitar warnings
        '-o', '/tmp/hashcat_result.txt'
    ]
    
    print(f"[*] Ejecutando hashcat (GPU) con modo {mode}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Leer resultado
    try:
        with open('/tmp/hashcat_result.txt', 'r') as f:
            output = f.read().strip()
            if output:
                cracked = output.split(':')[-1]
                return cracked
    except:
        pass
    
    # Limpiar
    os.unlink(hash_file)
    if os.path.exists('/tmp/hashcat_result.txt'):
        os.unlink('/tmp/hashcat_result.txt')
    
    return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python hash_cracker_gpu.py <hash> <wordlist> <algoritmo>")
        sys.exit(1)
    
    target_hash = sys.argv[1]
    wordlist = sys.argv[2]
    algorithm = sys.argv[3]
    
    result = crack_with_gpu(target_hash, wordlist, algorithm)
    if result:
        print(f"[+] CRACKEADO (GPU): {result}")
    else:
        print("[-] No encontrado o hashcat falló")
