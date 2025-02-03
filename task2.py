from bcrypt import * 
from nltk.corpus import words
import nltk
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count

def parse_line(entry):
    return entry.split("$")


def check_password(args):
    word, full_hash = args
    if checkpw(word, full_hash.encode()):  
        return full_hash, word.decode()
    return None  

def crack_hash(hashed_pws):
    start_time = time.time()

    wordlist = [word.encode() for word in words.words() if 6 <= len(word) <= 10]

    cracked_passwords = {}

    for work_factor_group in hashed_pws:
        work_factor = work_factor_group[0]
        hashes = work_factor_group[1:]

        # Reconstruct the full bcrypt hash prefix (e.g., "$2b$08$...")
        full_hashes = [f"$2b${work_factor}${h}" for h in hashes]

        # Create task list: [(word1, hash1), (word2, hash1), ...]
        task_list = [(word, full_hash) for full_hash in full_hashes for word in wordlist]

        # Use multiprocessing Pool to parallelize password checking
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(check_password, task_list)

        # Collect found passwords
        for result in results:
            if result:  # If not None, a password was found
                cracked_passwords[result[0]] = result[1]

    end_time = time.time()

    print("\nCracked Passwords:")
    for hash_val, password in cracked_passwords.items():
        print(f"{hash_val} -> {password}")

    print(f"\nTotal Execution Time: {end_time - start_time:.2f} seconds")



def main(): 
    file = open("shadow.txt", "r")
    lines = file.readlines()
   
    hashed_pw_list = []
    
    for line in lines: 
        parsed_values = parse_line(line)[2:4]  
        parsed_values[1] = parsed_values[1].split(".")[-1].replace("\n", "")
        hashed_pw_list.append(parsed_values)
    
    grouped = defaultdict(list)

    for key, password in hashed_pw_list:
        grouped[key].append(password)

    collapsed_list = [[key] + passwords for key, passwords in grouped.items()]
    crack_hash(collapsed_list)
    print(nltk.data.find("corpora/words.zip"))

    print(collapsed_list)
    


if __name__ == "__main__":
    main()