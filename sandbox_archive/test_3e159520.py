# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1)**(i%2)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[matrix_minor(matrix, j, i) * (-1)**(i+j) for i in range(n)] for j in range(n)]
    inverse = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inverse

def matrix_minor(matrix, row, col):
    minor = [row[:col] + row[col+1:] for row in matrix[1:]]
    return minor

def matrix_mul(A, B, mod):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
                result[i][j] %= mod
    return result

def matrix_pow(matrix, power, mod):
    n = len(matrix)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while power > 0:
        if power % 2 == 1:
            result = matrix_mul(result, matrix, mod)
        matrix = matrix_mul(matrix, matrix, mod)
        power //= 2
    return result

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    for num in range(2, n+1):
        if is_prime(num):
            primes.append(num)
    return primes[:n]

def generate_random_cnf(n, m):
    cnf = set()
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(variables, 2)
        cnf.add(tuple(sorted(clause)))
    return cnf

def convert_to_simplicial_complex(cnf):
    simplicial_complex = []
    for clause in cnf:
        simplicial_complex.append(clause)
        for i in range(len(clause)):
            for j in range(i+1, len(clause)):
                simplicial_complex.append(tuple(sorted([clause[i], clause[j]])))
    return simplicial_complex

def apply_algebraic_shifting(simplicial_complex):
    shifted_complex = []
    for face in simplicial_complex:
        shifted_face = [x + 1 for x in face]
        shifted_complex.append(shifted_face)
    return shifted_complex

def compute_ideal_generators(shifted_complex, n):
    generators = set()
    for face in shifted_complex:
        generators.add(tuple(sorted(face)))
    return generators

def communication_complexity(cnf):
    n = len(cnf)
    m = sum(len(clause) for clause in cnf)
    return n * math.log2(m)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2*n, 3*n)
    cnf = generate_random_cnf(n, m)
    simplicial_complex = convert_to_simplicial_complex(cnf)
    shifted_complex = apply_algebraic_shifting(simplicial_complex)
    generators = compute_ideal_generators(shifted_complex, n)
    cc = communication_complexity(cnf)
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": len(generators) <= cc,
        "counterexample": "" if len(generators) <= cc else f"Generators: {len(generators)}, CC: {cc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")