import hashlib

def sha256_hash(data):
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()

def main():
    user_input = input("Enter text to hash: ")
    hashed_output = sha256_hash(user_input)
    print(f"SHA-256 Digest: {hashed_output}")

if __name__ == "__main__":
    main()