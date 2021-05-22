import argparse
import encryption_math as em

def main(message, path, output_path=''):
    file_message = open(message, 'r')
    file_pubk = open(path, 'r')

    if file_message.mode == 'r' and file_pubk.mode == 'r':
        message = file_message.read()
        public_key = file_pubk.read().split('\n')

        try:
            message_int = em.EncDec.encode(message)
        except:
            print('encoder::main::em.EncDec.encode')
            return

        encrypted_message = em.modular_exponentiation(message_int, int(public_key[0]), int(public_key[1]))

        file_encrypted = open(output_path, 'w+')
        file_encrypted.write(str(encrypted_message))
        file_encrypted.close()
    else:
        print('main::unable to read one or both files', args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encodes a message using the RSA public key')
    parser.add_argument('-m', '--message', type=str, help='file location of the message you want to encrypt')
    parser.add_argument('-pubk', '--public_key', type=str, help='file location where the public key is stored')

    args = parser.parse_args()

    main(args.message, args.public_key, 'encrypted_message.txt')
    
