import hashlib
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor

def crack_hash(hash_to_crack, wordlist_path, hash_type):
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()
                if hash_type == 'md5':
                    hashed = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == 'sha1':
                    hashed = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == 'sha256':
                    hashed = hashlib.sha256(word.encode()).hexdigest()
                else:
                    return None
                
                if hashed == hash_to_crack:
                    return word
    except FileNotFoundError:
        print(f"[-] Wordlist not found: {wordlist_path}")
        sys.exit(1)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash Cracker Tool")
    parser.add_argument("-H", "--hash", required=True, help="Hash to crack")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-t", "--type", default="auto", choices=["md5", "sha1", "sha256", "auto"], help="Hash type")
    
    args = parser.parse_args()
    
    # Auto-detect hash type by length
    if args.type == "auto":
        if len(args.hash) == 32:
            hash_type = "md5"
        elif len(args.hash) == 40:
            hash_type = "sha1"
        elif len(args.hash) == 64:
            hash_type = "sha256"
        else:
            print("[-] Could not auto-detect hash type")
            sys.exit(1)
    else:
        hash_type = args.type
    
    print(f"[*] Cracking hash ({hash_type}) with wordlist...")
    result = crack_hash(args.hash, args.wordlist, hash_type)
    
    if result:
        print(f"[+] Cracked! → {result}")
    else:
        print("[-] Not found in wordlist")
