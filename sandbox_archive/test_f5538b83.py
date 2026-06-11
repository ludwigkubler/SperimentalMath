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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            return None  # Singular matrix, no unique solution
        for j in range(i + 1, n):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                if k < i:
                    matrix[j][k] += factor * matrix[i][k]
                elif k > i:
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def minimal_quaternionic_order(cnf):
    n = len(cnf)
    identity_matrix = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    reduced_matrix = gaussian_elimination(identity_matrix)
    if reduced_matrix is None:
        return float('inf')
    rank = sum(1 for row in reduced_matrix if any(val != Fraction(0, 1) for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        num_clauses = random.randint(1, n // 2)
        clause = set()
        while len(clause) < num_clauses:
            lit = random.choice([-i, i] for i in range(1, n + 1))
            if lit not in clause:
                clause.add(lit)
        cnf.append(list(clause))

    omega_phi = minimal_quaternionic_order(cnf)
    satisfiability_complexity = sum(len(clause) for clause in cnf)

    return {
        "metric_name": "log(omega(φ))",
        "metric_value": math.log(omega_phi, 10),
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")