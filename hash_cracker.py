import hashlib
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

# Algoritmos soportados con sus longitudes
ALGORITHMS = {
    'md5': (hashlib.md5, 32),
    'sha1': (hashlib.sha1, 40),
    'sha224': (hashlib.sha224, 56),
    'sha256': (hashlib.sha256, 64),
    'sha384': (hashlib.sha384, 96),
    'sha512': (hashlib.sha512, 128),
    'blake2b': (hashlib.blake2b, 128),
    'blake2s': (hashlib.blake2s, 64)
}

def detect_hash_type(hash_str):
    """Detecta algoritmo por longitud"""
    hash_len = len(hash_str)
    for algo, (_, length) in ALGORITHMS.items():
        if hash_len == length:
            return algo
    return None

def crack_single_word(word, target_hash, algorithm):
    """Crackea una palabra individual"""
    try:
        hasher = ALGORITHMS[algorithm][0]()
        hasher.update(word.encode('utf-8'))
        if hasher.hexdigest() == target_hash:
            return word
    except:
        pass
    return None

def crack_thread(args):
    """Wrapper para ThreadPoolExecutor"""
    word, target_hash, algorithm = args
    return crack_single_word(word, target_hash, algorithm)

def load_wordlist(wordlist_path):
    """Carga wordlist con manejo de errores"""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Wordlist no encontrada: {wordlist_path}")
        sys.exit(1)

def crack_hash_multithread(target_hash, wordlist_path, algorithm, threads=8):
    """Versión con multithreading y barra de progreso"""
    words = load_wordlist(wordlist_path)
    print(f"[*] Probando {len(words)} palabras con {threads} hilos...")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        args_list = [(word, target_hash, algorithm) for word in words]
        futures = [executor.submit(crack_thread, args) for args in args_list]
        
        with tqdm(total=len(words), desc="Cracking", unit="word") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    executor.shutdown(wait=False, cancel_futures=True)
                    return result
                pbar.update(1)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash Cracker - Multithreading + Multi-algorithm")
    parser.add_argument("-H", "--hash", required=True, help="Hash a crackear")
    parser.add_argument("-w", "--wordlist", required=True, help="Ruta del diccionario")
    parser.add_argument("-a", "--algorithm", default="auto", help="Tipo de hash (auto, md5, sha1, sha256, etc.)")
    parser.add_argument("-t", "--threads", type=int, default=8, help="Número de hilos (default: 8)")
    
    args = parser.parse_args()
    
    # Detectar algoritmo
    if args.algorithm == "auto":
        algorithm = detect_hash_type(args.hash)
        if not algorithm:
            print("[-] No se pudo detectar el algoritmo. Especifica con -a")
            sys.exit(1)
        print(f"[+] Algoritmo detectado: {algorithm.upper()}")
    else:
        algorithm = args.algorithm.lower()
        if algorithm not in ALGORITHMS:
            print(f"[-] Algoritmo no soportado. Usa: {', '.join(ALGORITHMS.keys())}")
            sys.exit(1)
    
    # Ejecutar cracking
    print(f"[*] Hash objetivo: {args.hash}")
    result = crack_hash_multithread(args.hash, args.wordlist, algorithm, args.threads)
    
    if result:
        print(f"\n[+] ¡CRACKEADO! → {result}")
    else:
        print("\n[-] No encontrado en el diccionario.")
