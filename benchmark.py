from os import close, write
import generate_keys as gk
import encoder as e
import decoder as d

import time
import random
import string
import os
import shutil

import matplotlib.pyplot as plt
import numpy as np

bits_szs = [10, 50, 100, 200, 256, 300, 400, 512, 800]
messages_szs = [1, 10, 20, 50, 70, 100, 120, 150]
path = 'benchmarks/'
repeat = 10

def clean_benchmarks_folder(path):
    shutil.rmtree(path)
    os.makedirs(path)

def generate_message_files(path):
    letters = string.ascii_letters
    for message_size in messages_szs:
        message = ''.join(random.choices(letters, k=message_size))
        f = open(path + 'message_' + str(message_size) + '.txt', 'w+')
        f.write(message)
        f.close()

def plot_keys_chart(keys_times):
    X = list(map(str, bits_szs))
    X_axis = np.arange(len(X))
  
    plt.bar(X_axis, keys_times, 0.8)
    
    plt.xticks(X_axis, X)
    plt.xlabel("Prime used size in bits")
    plt.ylabel("Avg time taken (s)")
    plt.title("Average time to generate a pair of keys of n bits")
    plt.legend()
    plt.show()

def get_message_times(mp):
    messages_times = np.zeros((len(messages_szs), len(bits_szs))) * 0.0

    i = 0
    for _, v in mp.items():
        messages_times[:, i] = np.transpose(v)
        i += 1
    
    return messages_times

def plot_charts(keys, encrypt, decrypt):
    plot_keys_chart(keys)

    message_encrypt_times = get_message_times(encrypt)
    message_decrypt_times = get_message_times(decrypt)

    X = list(map(str, bits_szs))
    X_axis = np.arange(len(X))

    for i, v in enumerate(messages_szs):
        plt.bar(X_axis - 0.2, message_encrypt_times[i], 0.4, label = 'Encryption')
        plt.bar(X_axis + 0.2, message_decrypt_times[i], 0.4, label = 'Decryption')
    
        plt.xticks(X_axis, X)
        plt.xlabel("bits used for the prime number")
        plt.ylabel("Time taken (s)")
        plt.title("Average time to encrypt and decrypt message of size " + str(v))
        plt.legend()
        plt.show()


if __name__ == '__main__':
    
    avg_generate_keys_times = np.zeros(len(bits_szs))
    avg_encrypt_times = {}
    avg_decrypt_times = {}
    avg_total_times = []

    for i in range(repeat):
        generate_keys_times = []

        clean_benchmarks_folder(path)
        generate_message_files(path)

        for bits in bits_szs:
            encrypt_times = []
            decrypt_times = []
            total_times = []

            started = time.time()
            gk.main(bits, path)
            elapsed = time.time()

            generate_keys_times.append(elapsed - started)

            for message_size in messages_szs:
                started = time.time()
                e.main( path + 'message_' + str(message_size) + '.txt', 
                        path + 'public_key_' + str(bits) + '.txt', 
                        path + 'encrypted_message_' + str(message_size) + '.txt')
                elapsed = time.time()

                encrypt_times.append(elapsed - started)

                started = time.time()
                d.main( path + 'encrypted_message_' + str(message_size) + '.txt', 
                        path + 'private_key_' + str(bits) + '.txt',
                        path + 'decrypted_message_' + str(message_size) + '.txt')
                elapsed = time.time()

                decrypt_times.append(elapsed - started)

                total_times.append(generate_keys_times[-1] + encrypt_times[-1] + decrypt_times[-1])

                # check if it was valid
                decrypted_path = path + 'decrypted_message_' + str(message_size) + '.txt'

                if os.path.exists(decrypted_path):
                    message_file = open(path + 'message_' + str(message_size) + '.txt', 'r')
                    decrypted_file = open(decrypted_path, 'r')

                    if decrypted_file.mode == 'r' and message_file.mode == 'r':
                        original_message = message_file.read()
                        decrypted_message = decrypted_file.read()

                        if original_message != decrypted_message:
                            total_times[-1] = encrypt_times[-1] = decrypt_times[-1] = 0
                    else:
                        total_times[-1] = encrypt_times[-1] = decrypt_times[-1] = 0
                else:
                    total_times[-1] = encrypt_times[-1] = decrypt_times[-1] = 0

            avg_encrypt_times[bits] = np.add(avg_encrypt_times.setdefault(bits, np.zeros(len(encrypt_times))), encrypt_times)
            avg_decrypt_times[bits] = np.add(avg_decrypt_times.setdefault(bits, np.zeros(len(decrypt_times))), decrypt_times)
                
        
        avg_generate_keys_times = np.add(avg_generate_keys_times, generate_keys_times)
    
    avg_generate_keys_times = np.divide(avg_generate_keys_times, repeat)
    
    for k, v in avg_encrypt_times.items():
        v = np.divide(v, repeat)

    for k, v in avg_decrypt_times.items():
        v = np.divide(v, repeat)

    
    plot_charts(avg_generate_keys_times, avg_encrypt_times, avg_decrypt_times)
