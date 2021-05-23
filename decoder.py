import argparse
import encryption_math as em


def main(message, path, output_path=''):
    # open the files containing the encrypted message and the private key
    file_message = open(message, 'r')
    file_privk = open(path, 'r')

    # check if both files were correctly open
    if file_message.mode == 'r' and file_privk.mode == 'r':

        # read the encrypted message and the private key
        encrypted_message = int(file_message.read())
        private_key = file_privk.read().split('\n')

        # decrypt the message using the formula E^d (mod n)
        decrypted_message = em.modular_exponentiation(encrypted_message, int(private_key[0]), int(private_key[1]))
        try:
            # convert the bytes representation to string
            message_int = em.EncDec.decode(decrypted_message)
        except:
            print('decoder::main::em.EncDec.decode::Exception')
            return

        # generate the files that contain the decrypted message
        file_decrypted = open(output_path, 'w+')
        file_decrypted.write(str(message_int))
        file_decrypted.close()
    else:
        print('main::unable to read one or both files', args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decodes a message using the RSA private key')
    parser.add_argument('-m', '--message', type=str, help='file location of the encrypted message')
    parser.add_argument('-privk', '--private_key', type=str, help='file location where the private key is stored')

    args = parser.parse_args()

    main(args.message, args.private_key, 'decrypted_message.txt')