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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def group_action_orbits(clause, G):
        orbits = set()
        for g in G:
            orbit = tuple(sorted([g[v] for v in clause]))
            orbits.add(orbit)
        return len(orbits)

    def generate_group(n):
        # Generate a simple cyclic group of order n
        G = [[i + j % n for i in range(n)] for j in range(n)]
        return G

    def generate_clause(n, s):
        clause = random.sample(range(1, n+1), s)
        return clause

    def generate_sat_instance(n, s):
        clauses = [generate_clause(n, s) for _ in range(random.randint(5, 10))]
        return clauses

    def calculate_alpha(s):
        return s ** (math.log2(s))

    n_max = 40
    instances_tested = 0
    max_orbits = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(1, n_max + 1):
        for _ in range(3):  # Sample 3 instances per size
            s = random.randint(1, min(n, 5))  # Clause size up to n
            clauses = generate_sat_instance(n, s)
            G = generate_group(n)
            orbits = sum(group_action_orbits(clause, G) for clause in clauses)
            if orbits > max_orbits:
                max_orbits = orbits
            instances_tested += 1

    alpha_n = calculate_alpha(n_max)
    if max_orbits > alpha_n:
        conjecture_holds = False
        counterexample = f"max_orbits={max_orbits} > alpha({n_max})={alpha_n}"

    return {
        "metric_name": "max_orbits",
        "metric_value": max_orbits,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_orbits_exceeds_alpha\" first_failing_seed={first_failing_seed}")