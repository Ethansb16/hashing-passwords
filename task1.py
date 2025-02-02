import time
import hashlib
import random
import string

def sha256_hash(data):
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()

def random_string(length=10):
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(chars) for _ in range(length))

def find_collision():
    seen_hashes = {}

    start_time = time.time()
    count = 0
    
    while True:

        count += 1
        rand_str = random_string()
        truncated_hash = sha256_hash(rand_str)[:8]

        if truncated_hash in seen_hashes:
            end_time = time.time()
            print(f"Collision found!")
            print(f"String 1: {seen_hashes[truncated_hash]} -> {truncated_hash}")
            print(f"String 2: {rand_str} -> {truncated_hash}")
            return

        seen_hashes[truncated_hash] = rand_str
    time_elapsed = start_time - end_time


def hamming_dist(first, second): 
    hamming_distance = sum(b1 != b2 for b1, b2 in zip(first, second))
    return hamming_distance
        

def main():
    user_input = input("Enter text to hash: ")
    hashed_output = sha256_hash(user_input)

    print(f" 1a) SHA-256 Digest: {hashed_output}")
    check_hamming_dist = sha256_hash("distance check")
    print(f"2a) {hamming_dist(hashed_output, check_hamming_dist)}")

    find_collision()

if __name__ == "__main__":
    main()