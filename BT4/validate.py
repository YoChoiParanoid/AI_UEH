from pyDatalog import pyDatalog
from sympy import prime, isprime

pyDatalog.clear()
pyDatalog.create_terms('X, prime_num')

# List of numbers
list_nums = [23, 4, 27, 17, 13, 10, 21, 29, 3, 32, 11, 19]

# Add facts to pyDatalog
for num in list_nums:
    if isprime(num):
        +prime_num(num)  # Add fact to the knowledge base

# Query and print primes
print("\nList of primes in the list:")
print(prime_num(X))

# First 7 prime numbers using sympy
print("\nList of first 7 prime numbers:")
first_seven_primes = [prime(i) for i in range(1, 8)]  # 1-based index
print(first_seven_primes)
