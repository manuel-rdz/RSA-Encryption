import random

# class to encode string to integer number by using its byte representation
class EncDec:
    @staticmethod
    def encode(text):
        bytes = text.encode("utf-8")
        return int.from_bytes(bytes, byteorder="big")

    @staticmethod
    def decode(value):
        bytes = value.to_bytes(((value.bit_length() + 7) // 8), byteorder="big")
        return bytes.decode("utf-8")


def binary_exponentiation(n, p):
    ans = 1
    b = 1
    while b <= p:
        if (p & b):
            ans *= n    
        n *= n
        b *= 2

    return ans


def modular_exponentiation(n, p, m):
    ans = 1
    b = 1
    while b <= p:
        if (p & b):
            ans = (ans * n) % m
        n = (n * n) % m
        b *= 2

    return ans

def witness(a, n):
    t = 1
    p = 2

    # find the greatest power of 2 that divides (n - 1)
    while (n - 1) % p == 0:
        t += 1
        p *= 2

    # if 2 does not divide (n - 1), then it is a witness??
    if t == 1:
        return True
    
    # calculate the representation of (n - 1) as u*2^t
    t -= 1
    p = p // 2
    u = (n - 1) // p

    # from the book
    x_0 = modular_exponentiation(a, u, n)
    for i in range(1, t + 1):
        x_1 = (x_0 ** 2) % n
        if x_1 == 1 and x_0 != 1 and x_0 != n - 1:
            return True
    
    if x_1 != 1:
        return True
    
    return False

def miller_rabin(n, s):
    for i in range(0, s):
        a = random.randint(1, n - 1)
        if witness(a, n):
            return False
    
    return True

def gcd(a, b):
    while b != 0:
        aux = b
        b = a % b
        a = aux
    return a

# find a non trivial coprime of phi by proposing random 
# numbers and calculating their gcd with n
def get_coprime(n, max_value):
    while True:
        candidate = random.randint(3, max_value)
        if (candidate & 1) and gcd(candidate, n) == 1:
            return candidate


def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
         d, x, y = extended_euclid(b, a % b)
    
    return d, y, (x - a//b*y)


def modular_linear_equation_solver(a, b, n):
    d, x, y = extended_euclid(a, n)
    if b % d == 0:
        return x % n
    print('modular_linear_equation_solver::no solutions')        
    return 0