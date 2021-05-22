from os import close, write
import generate_keys as gk
import encoder as e
import decoder as d

import time
import random
import string
import os

bits_szs = [10, 50, 100, 200, 300, 400, 512]
messages_szs = [1, 10, 20, 50, 70, 100, 120]
path = 'benchmarks/'

def generate_message_files(path):
    letters = string.ascii_letters
    for message_size in messages_szs:
        message = ''.join(random.choices(letters, k=message_size))
        f = open(path + 'message_' + str(message_size) + '.txt', 'w+')
        f.write(message)
        f.close()


if __name__ == '__main__':
    generate_message_files(path)

    for bits in bits_szs:
        started = time.time()
        gk.main(bits, path)
        elapsed = time.time()

        time_keys = elapsed - started

        for message_size in messages_szs:
            started = time.time()
            e.main( path + 'message_' + str(message_size) + '.txt', 
                    path + 'public_key_' + str(bits) + '.txt', 
                    path + 'encrypted_message_' + str(message_size) + '.txt')
            elapsed = time.time()

            time_encrypt = elapsed - started

            started = time.time()
            d.main( path + 'encrypted_message_' + str(message_size) + '.txt', 
                    path + 'private_key_' + str(bits) + '.txt',
                    path + 'decrypted_message_' + str(message_size) + '.txt')
            elapsed = time.time()

            time_decrypt = elapsed - started

            total_time = time_keys + time_encrypt + time_decrypt

            # check if it was valid
            decrypted_path = path + 'decrypted_message_' + str(message_size) + '.txt'
            
            if os.path.exists(decrypted_path):
                message_file = open(path + 'message_' + str(message_size) + '.txt', 'r')
                decrypted_file = open(decrypted_path, 'r')

                if decrypted_file.mode == 'r' and message_file.mode == 'r':
                    original_message = message_file.read()
                    decrypted_message = decrypted_file.read()

                    if original_message != decrypted_message:
                        time_encrypt = time_decrypt = total_time = 0
                else:
                    time_encrypt = time_decrypt = total_time = 0
            else:
                time_encrypt = time_decrypt = total_time = 0

            txt = 'bits = ' + str(bits) + ' message_size = ' + str(message_size)
            txt += ' time_keys = ' + str(time_keys) + ' time_encrypt = ' + str(time_encrypt) + ' time_decrypt = ' + str(time_decrypt)
            txt += ' total_time = ' + str(total_time)

            print(txt)