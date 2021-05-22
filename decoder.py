import argparse
import encryption_math as em


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decodes a message using the RSA private key')
    parser.add_argument('-m', '--message', type=str, help='file location of the message you want to encrypt')
    parser.add_argument('-privk', '--private_key', type=str, help='file location where the private key is stored')

    args = parser.parse_args()
    
    file_message = open(args.message, 'r')
    file_privk = open(args.private_key, 'r')

    if file_message.mode == 'r' and file_privk.mode == 'r':
        encrypted_message = int(file_message.read())
        private_key = file_privk.read().split('\n')

        decrypted_message = em.modular_exponentiation(encrypted_message, int(private_key[0]), int(private_key[1]))
        message_int = em.EncDec.decode(decrypted_message)

        file_decrypted = open('decrypted_message.txt', 'w+')
        file_decrypted.write(str(message_int))
        file_decrypted.close()
    else:
        print('main::unable to read one or both files', args)