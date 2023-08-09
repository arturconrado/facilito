def is_prime(n):
    if n == 1 or n == 0:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_fibonacci(n):
    x = 5 * n ** 2 + 4
    y = 5 * n ** 2 - 4
    return x ** 0.5 % 1 == 0 or y ** 0.5 % 1 == 0