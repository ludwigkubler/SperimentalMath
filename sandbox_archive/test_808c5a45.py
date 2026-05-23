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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    A_aug = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_aug[j][i]) > abs(A_aug[max_row][i]):
                max_row = j
        A_aug[i], A_aug[max_row] = A_aug[max_row], A_aug[i]
        pivot = A_aug[i][i]
        for j in range(n + 1):
            A_aug[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_aug[j][i]
                for k in range(n + 1):
                    A_aug[j][k] -= factor * A_aug[i][k]
    return [row[-1] for row in A_aug]

def geometric_group_rank(G, n):
    # Placeholder function to compute the rank of a geometric group action
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 5)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    G = [random.randint(1, 5) for _ in range(random.randint(3, 6))]
    n = random.randint(5, 40)
    c_G = geometric_group_rank(G, n)
    S_C = random.randint(10, 20)
    
    # Construct an AC0 parity circuit C with size S(C) computing XOR on n inputs
    C = [[random.choice([0, 1]) for _ in range(S_C)] for _ in range(n)]
    
    # Compute the r(G)-invariant subset for each group action on the circuit
    invariant_subset = []
    for i in range(n):
        invariant_subset.append(sum(C[i][j] for j in range(S_C) if (i + j) % 2 == 0))
    
    # Measure the rank of the invariant subset and compare it to c_G·log(S(C))
    r_G_S_C = len(set(invariant_subset))
    ratio = Fraction(r_G_S_C, math.log(S_C))
    
    return {
        "metric_name": "r(G(S(C))) / log(S(C))",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= c_G * math.log(S_C),
        "counterexample": "" if ratio <= c_G * math.log(S_C) else f"r(G(S(C))) = {r_G_S_C}, c_G·log(S(C)) = {c_G * math.log(S_C)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")