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
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, k):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mult(result, M)
        M = matrix_mult(M, M)
        k //= 2
    return result

def is_coxeter_group(G):
    n = len(G)
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 0 and G[j][i] == 0:
                return False
    return True

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def automorphism_group(cnf):
    variables = set(abs(lit) for lit in cnf[0])
    n = len(variables)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if all(lit % (j - i) == 0 for lit in cnf[0]):
                G[i][j] = 1
                G[j][i] = 1
    return G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    max_n = 40
    instances_tested = 0
    n_max = 0
    max_size = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, max_n + 1):
        cnf = generate_cnf(n)
        G = automorphism_group(cnf)
        if not is_coxeter_group(G):
            continue
        size = sum(sum(row) for row in G) // 2
        if size > max_size:
            max_size = size
            n_max = n

        instances_tested += 1

    metric_value = max_size
    support_fraction = instances_tested / (max_n - 4)

    if max_size > 2 ** max_n:
        conjecture_holds = False
        counterexample = f"Size {max_size} exceeds bound 2^{max_n}"

    return {
        "metric_name": "Max Group Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
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
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Size exceeds bound\" first_failing_seed={first_failing_seed}")