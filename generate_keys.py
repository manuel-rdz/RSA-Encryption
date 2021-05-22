import random
import argparse
import encryption_math as em


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates public and private keys using RSA algorithm')
    parser.add_argument('-b', '--bits', type=int, nargs='?', const=1, default=512, help='size in bits of the prime number used to generate keys')

    args = parser.parse_args()
    print(args)

    p = 0
    q = 0

    min_prime = em.binary_exponentiation(2, int(args.bits))
    max_prime = em.binary_exponentiation(2, int(args.bits)+1) - 1

    while (p == 0 or q == 0):
        candidate = random.randint(min_prime,
                                   max_prime)
        if em.miller_rabin(candidate, 20):
            if p == 0: 
                p = candidate
            elif p != candidate:
                q = candidate

    #print('p = ', p)
    #print('q = ', q)

    n = p * q
    #print('n = ', n)

    # calculate e as a coprime of phi

    phi = (p-1)*(q-1)
    #print('phi = ', phi)

    e = em.get_coprime(phi)
    #print('e = ', e)

    d = em.modular_linear_equation_solver(e, 1, phi)
    #print('d = ', d)

    #print('e*d mod phi = ', (e*d) % phi)

    pub_key = open('public_key.txt', 'w+')
    priv_key = open('private_key.txt', 'w+')

    pub_key.write(str(e) + '\n')
    pub_key.write(str(n))

    priv_key.write(str(d) + '\n')
    priv_key.write(str(n))

    pub_key.close()
    priv_key.close()        

    #print('RSA public key: ', pub_key)
    #print('RSA private key: ', priv_key)
