import argparse
import random
import encryption_math as em


class EncDec:
    @staticmethod
    def encode(text):
        bytes = text.encode("utf-8")
        return int.from_bytes(bytes, byteorder="big")

    @staticmethod
    def decode(value):
        bytes = value.to_bytes(((decrypted_message.bit_length() + 7) // 8), byteorder="big")
        return bytes.decode("utf-8")




if __name__ == '__main__':
    p = 0
    q = 0

    min_prime = em.binary_exponentiation(2, 512)
    max_prime = em.binary_exponentiation(2, 513)

    while (p == 0 or q == 0):
        candidate = random.randint(min_prime,
                                   max_prime)
        if em.miller_rabin(candidate, 20):
            if p == 0: 
                p = candidate
            elif p != candidate:
                q = candidate

    print('p = ', p)
    print('q = ', q)

    n = p * q
    print('n = ', n)

    # calculate e as a coprime of phi

    phi = (p-1)*(q-1)
    print('phi = ', phi)

    e = em.get_coprime(phi)
    print('e = ', e)

    d = em.modular_linear_equation_solver(e, 1, phi)
    print('d = ', d)

    print('e*d mod phi = ', (e*d) % phi)

    pub_key = (e, n)
    priv_key = (d, n)         

    print('RSA public key: ', pub_key)
    print('RSA private key: ', priv_key)

    message = 'test message to see how large it can be'

    message_int = EncDec.encode(message)

    encrypted_message = em.modular_exponentiation(message_int, e, n)
    print(encrypted_message)

    decrypted_message = em.modular_exponentiation(encrypted_message, d, n)

    recovered_message = EncDec.decode(decrypted_message)

    print(recovered_message)