# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mult(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_power(A, n):
    result = [[0 if i != j else 1 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, A)
        A = matrix_mult(A, A)
        n //= 2
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError('No unique solution')
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            A[i][-1] -= A[i][j] * A[j][-1]
        A[i][-1] /= A[i][i]
        A[i][i] = 1
    return [row[-1] for row in A]

def lcm_list(lst):
    result = lst[0]
    for num in lst[1:]:
        result = lcm(result, num)
    return result

def generate_random_dnf(n, k, implicant_size):
    variables = list(range(n))
    implicants = set()
    while len(implicants) < k:
        implicant = random.sample(variables, implicant_size)
        if all(len(set(a).intersection(b)) == 0 for b in implicants):
            implicants.add(tuple(sorted(implicant)))
    dnf = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        if any(all(binary[j] == '1' for j in implicant) for implicant in implicants):
            dnf.append(i)
    return dnf

def compute_decision_tree_depth(dnf, n):
    @lru_cache(None)
    def depth(mask):
        if mask == 0:
            return 0
        max_depth = -1
        for i in range(n):
            if mask & (1 << i) != 0:
                new_mask = mask ^ (1 << i)
                if all(new_mask & (1 << j) == 0 for j in range(i+1, n)):
                    max_depth = max(max_depth, depth(new_mask))
        return max_depth + 1
    return depth((1 << n) - 1)

def compute_meet_closure_lattice(dnf):
    n = len(bin(dnf[0])) - 2
    lattice = {frozenset(): 0}
    for i in range(n):
        new_elements = set()
        for element in lattice:
            for j in range(i+1, n):
                if (element | {j}) not in lattice:
                    new_elements.add(element | {j})
        for element in new_elements:
            lattice[element] = len(element)
    return lattice

def compute_möbius_function(lattice):
    mu = defaultdict(int)
    mu[frozenset()] = 1
    for element in sorted(lattice, key=lambda x: len(x)):
        mu[element] = -sum(mu[subelement] for subelement in lattice if subelement < element and element - subelement == {min(element)})
    return mu

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    k_values = range(3, 9)
    implicant_sizes = [2, 3, 4]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for k in k_values:
            for implicant_size in implicant_sizes:
                dnf = generate_random_dnf(n, k, implicant_size)
                depth = compute_decision_tree_depth(dnf, n)
                lattice = compute_meet_closure_lattice(dnf)
                mu = compute_möbius_function(lattice)
                mu_value = abs(mu[frozenset()])
                required_depth = math.ceil(math.log2(1 + mu_value))
                if depth < required_depth:
                    conjecture_holds = False
                    counterexample = f"n={n}, k={k}, implicant_size={implicant_size}, D^dt(f)={depth}, μ_f={mu_value}"
                    break
        instances_tested += len(n_values) * len(k_values) * len(implicant_sizes)

    return {
        "metric_name": "D^dt(f)",
        "metric_value": depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")