# RSA-Encryption

WARNING: THIS IMPLEMENTATION IS NOT SECURE, IT WAS DEVELOPED JUST FOR EDUCATIONAL PURPOSES. PLEASE, DON'T USE IT FOR ANYTHING SERIOUS.

This code is an implementation of the RSA criptography system. It makes use of public and private keys to encrypt and decrypt messages.

It consists of 3 modules and 1 benchmark file used to measure the performance.

# key generation

You can generate a pair of public and private keys using the generate_keys.py file. You can pass as an argument the size in bits of the prime numbers that will be used to generate the keys (default size is 512). This script generates two txt files containing the public (public_key_'#bits'.txt) and private (private_key_'#bits'.txt) keys. Example:

  python generate_keys.py -b 824
  
This script will create a pair of keys using two prime numbers with 824 bits size each one. The keys will be stored in two generated txt files (public_key_824.txt and private_key_824.txt).

# Message Encryption
You can encrypt a message using the encoder.py file.
To encrypt a message first you have to generate a pair of keys. Make sure the size of the prime numbers in bits used to generate the keys is enough to encrypt a message of the required length. When you have your keys, write the message in a txt file so you can pass it to the script as an argument along with the location of your public key. This script will generate a txt file called 'encrypted_message.txt' that contains the encrypted message. Ex:

  python encoder.py -m message.txt -pubk public_key_824.txt


# Message Decryption
You can decrypt encrypted messages using the decoder.py file.
To decrypt the message you have to use your private key. Make sure you have the encrypted_message in a txt file so you can pass it as an argument along the private key to the script. The script will generate a txt file called 'decrypted_message.txt' that contains the original messsage. Ex:

  python decoder.py -m encrypted_message.txt -privk private_key_824.txt
  
# Benchmarks
The benchmark.py file runs a benchmark on the time the algorithm takes to generate pairs of keys of different sizes repeated times and taking the average.
It also generates dummy messages to test the time it takes to encrypt and decrypt these messages with the generated keys.
