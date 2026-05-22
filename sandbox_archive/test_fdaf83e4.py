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

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented_Ab = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented_Ab[j][i]) > abs(Augmented_Ab[max_row][i]):
                max_row = j
        Augmented_Ab[i], Augmented_Ab[max_row] = Augmented_Ab[max_row], Augmented_Ab[i]
        for j in range(i+1, m):
            factor = Augmented_Ab[j][i] / Augmented_Ab[i][i]
            for k in range(n+1):
                Augmented_Ab[j][k] -= factor * Augmented_Ab[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Augmented_Ab[i][-1] / Augmented_Ab[i][i]
        for j in range(i):
            Augmented_Ab[j][-1] -= Augmented_Ab[j][i] * x[i]
    return x

def min_symmetric_tensor_rank(G):
    n = len(G)
    I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    A = matrix_multiply(I, G)
    B = matrix_multiply(A, G)
    C = gaussian_elimination(B, [0] * n)
    rank = sum(1 for row in C if any(row))
    return rank

def resolution_proof_length(CNF):
    clauses = CNF.split(' 0\n')
    clauses = [c.split()[:-1] for c in clauses]
    stack = []
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = int(unit_clause[0])
        for clause in clauses:
            if literal in clause:
                clause.remove(literal)
            elif -literal in clause:
                clause.remove(-literal)
                stack.append(-literal)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    CNF = ' '.join(str(random.randint(1, n)) for _ in range(n)) + ' 0\n'
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    rank = min_symmetric_tensor_rank(G)
    proof_length = resolution_proof_length(CNF)
    metric_value = rank / proof_length
    return {
        "metric_name": "min_symmetric_tensor_rank_to_proof_length_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= 10**(1/2),
        "counterexample": "" if metric_value <= 10**(1/2) else f"n={n}, rank={rank}, proof_length={proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")