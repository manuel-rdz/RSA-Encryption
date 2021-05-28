import random
import argparse
import encryption_math as em


def main(bits, output_path=''):
    p = 0
    q = 0

    # calculate max and min range of prime values to be generated
    min_prime = em.binary_exponentiation(2, int(bits))
    max_prime = min_prime * 2 -1

    # find 2 prime numbers using miller-rabin algorithm
    while (p == 0 or q == 0):
        candidate = random.randint(min_prime,
                                   max_prime)
        if em.miller_rabin(candidate, 20):
            if p == 0: 
                p = candidate
            elif p != candidate:
                q = candidate
    
    # calculate value of n
    n = p * q

    # calculate phi(n)
    phi = (p-1)*(q-1)

    # find value of e as a non-trivial coprime of phi(n)
    e = em.get_coprime(phi, min(p-1, q-1, 100000))

    # find the multiplicative inverse of e (mod phi(n))
    # solving the equation x*e = 1 (mod phi(n))
    d = em.modular_linear_equation_solver(e, 1, phi)

    # create files to store both keys
    pub_key = open(output_path + 'public_key_' + str(bits) + '.txt', 'w+')
    priv_key = open(output_path + 'private_key_' + str(bits) + '.txt', 'w+')

    # write the public key as the pair (e, n)
    pub_key.write(str(e) + '\n')
    pub_key.write(str(n))

    # write the private key as the pair (d, n)
    priv_key.write(str(d) + '\n')
    priv_key.write(str(n))

    # close the files to save changes
    pub_key.close()
    priv_key.close() 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates public and private keys using RSA algorithm')
    parser.add_argument('-b', '--bits', type=int, nargs='?', const=1, default=512, help='size in bits of the prime number used to generate keys')

    args = parser.parse_args()

    main(args.bits)
