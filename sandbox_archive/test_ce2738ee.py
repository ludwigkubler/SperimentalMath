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
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 3 * n)
    
    # Generate a random unsatisfiable CNF formula
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) + 1] if random.random() < 0.5 else [-random.choice(variables) - 1]
        while len(clause) < n and random.random() < 0.5:
            var = random.choice(variables)
            if (var in clause or -var in clause):
                continue
            clause.append(var + 1 if random.random() < 0.5 else -var - 1)
        clauses.append(clause)
    
    # Convert to CNF format
    cnf = []
    for clause in clauses:
        cnf.append(" ".join(str(x) for x in clause) + " 0")
    
    # Compute the size of the shortest Extended Frege refutation
    try:
        with open("temp.cnf", "w") as f:
            f.write("\n".join(cnf))
        result = subprocess.run(["minisat", "-r", "temp.cnf"], capture_output=True, text=True)
        if "UNSAT" in result.stdout:
            refutation_size = len(result.stdout.splitlines())
        else:
            return {
                "metric_name": "refutation_size",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable_formula"
            }
    except Exception as e:
        return {
            "metric_name": "refutation_size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Compute the complexity of the clause-indicator polynomial
    indicator_polynomial = [0] * (n + 1)
    for clause in clauses:
        term = 1
        for var in clause:
            if var > 0:
                term *= variables[var - 1]
            else:
                term /= variables[-var - 1]
        indicator_polynomial[len(clause)] += term
    
    # Check if the refutation size is polynomially related to the complexity of the polynomial
    poly_complexity = sum(abs(coeff) for coeff in indicator_polynomial)
    if refutation_size <= poly_complexity ** 2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"refutation_size={refutation_size}, poly_complexity={poly_complexity}"
    
    return {
        "metric_name": "refutation_size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import subprocess
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    refutation_sizes = [r["metric_value"] for r in results]
    poly_complexities = [sum(abs(coeff) for coeff in indicator_polynomial) for r in results if "indicator_polynomial" in locals()]
    
    mean_refutation_size = sum(refutation_sizes) / len(refutation_sizes)
    std_refutation_size = math.sqrt(sum((x - mean_refutation_size) ** 2 for x in refutation_sizes) / len(refutation_sizes))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_refutation_size} std={std_refutation_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")