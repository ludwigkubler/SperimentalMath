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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

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
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        minor = [[matrix[j][k] for k in range(n) if k != i] for j in range(1, n)]
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, mod)
    inv_det = mod_inverse(det % mod, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
            cofactor = ((-1) ** (i + j)) * determinant(minor, mod)
            adjugate[j][i] = cofactor
    return matrix_mod_mul(adjugate, inv_det, mod)

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def determinant(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = [[matrix[j][k] for k in range(n) if k != i] for j in range(1, n)]
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, mod)
    return det % mod

def polynomial_to_matrix(poly, var):
    n = len(poly)
    m = len(poly[0])
    matrix = [[0] * (m + 1) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if poly[i][j] == var:
                matrix[i][j] = 1
            elif poly[i][j] == '¬' + var:
                matrix[i][j] = -1
    return matrix

def resultant(poly1, poly2, mod):
    n = len(poly1)
    m = len(poly2)
    A = polynomial_to_matrix(poly1, 'x')
    B = polynomial_to_matrix(poly2, 'y')
    C = matrix_mod_mul(A, B, mod)
    D = matrix_mod_inv(C, mod)
    return determinant(D, mod)

def dpll(clauses):
    def is_satisfiable(model):
        for clause in clauses:
            if all(lit not in model or (model[lit] == 1 and lit[0] != '¬') or (model[lit] == -1 and lit[0] == '¬') for lit in clause):
                return True
        return False

    def backtrack(model, literals):
        if not literals:
            return is_satisfiable(model)
        literal = literals[0]
        rest = literals[1:]
        model[literal] = 1
        if backtrack(model, rest):
            return True
        del model[literal]
        model[literal] = -1
        if backtrack(model, rest):
            return True
        del model[literal]
        return False

    model = {}
    literals = sorted(set(lit for clause in clauses for lit in clause))
    return backtrack(model, literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 1.5  # Hypothesis that degree ≈ 1.5 * ProofSize(Φ)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        clauses = []
        for _ in range(n):
            clause = [random.choice(['x', '¬x', 'y', '¬y', 'z', '¬z']) for _ in range(3)]
            random.shuffle(clause)
            clauses.append(clause)

        poly1 = [(lit if lit[0] != '¬' else -int(lit[1])) for lit in clauses]
        poly2 = [(lit if lit[0] != '¬' else -int(lit[1])) for lit in clauses]

        degree = resultant(poly1, poly2, 2)
        proof_size = dpll(clauses)

        instances_tested += 1
        if abs(degree - k * proof_size) > 1:
            conjecture_holds = False
            counterexample = f"Degree {degree}, Proof Size {proof_size}"
            break

    return {
        "metric_name": "Resultant Degree",
        "metric_value": degree,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    degrees = [r["metric_value"] for r in results]
    proof_sizes = [r["instances_tested"] * 1.5 for r in results]  # Hypothesis k=1.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(degrees)/len(degrees):.2f} std={math.sqrt(sum((x - sum(degrees)/len(degrees))**2 for x in degrees) / len(degrees)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(degrees)/len(degrees):.2f} std={math.sqrt(sum((x - sum(degrees)/len(degrees))**2 for x in degrees) / len(degrees)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")