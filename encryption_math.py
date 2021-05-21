import random

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

    while (n - 1) % p == 0:
        t += 1
        p *= 2

    if t == 1:
        return True
    
    t -= 1
    p = p // 2
    u = (n - 1) // p

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
    if b == 0:
        return a
    return gcd(b, a % b)

# find a non trivial coprime of phi
def get_coprime(n):
    while True:
        candidate = random.randint(3, n - 1)
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