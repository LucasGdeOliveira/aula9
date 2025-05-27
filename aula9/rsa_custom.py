import random

# Função para calcular o MDC usando algoritmo de Euclides
def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Função para encontrar o inverso modular
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Verificar se um número é primo (simplificado)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Gerar um número primo aleatório pequeno (para fins didáticos)
def generate_prime():
    while True:
        num = random.randint(100, 300)
        if is_prime(num):
            return num

# Gerar chaves públicas e privadas RSA
def generate_keys():
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while mdc(e, phi) != 1:
        e += 2

    d = modinv(e, phi)
    return (e, n), (d, n)

# Criptografar uma mensagem (string → int list)
def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# Descriptografar uma mensagem (int list → string)
def decrypt(cipher, private_key):
    d, n = private_key
    return ''.join([chr(pow(c, d, n)) for c in cipher])
