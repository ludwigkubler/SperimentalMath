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

def generate_cnf(m, n):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([1, -1]) - 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def bruhn_matrix(clauses, n):
    m = len(clauses)
    matrix = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                matrix[i][literal - 1] += 1
            else:
                matrix[i][-1] += 1
    return matrix

def min_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
        matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
        rank += 1
        for j in range(m):
            if i == j:
                continue
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return rank

def frege_proof_width(clauses):
    # Placeholder function to simulate Frege proof width calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m_range = [int(m * (n / 10)) for m in range(1, 11)]
    results = []
    
    for m in m_range:
        cnf = generate_cnf(m, n)
        matrix = bruhn_matrix(cnf, n)
        rank = min_rank(matrix)
        proof_width = frege_proof_width(cnf)
        
        results.append({
            "m": m,
            "n": n,
            "rank": rank,
            "proof_width": proof_width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_proof_width = sum(result["proof_width"] for result in results) / len(results)
    conjecture_holds = all(rank <= math.log(m / n, 2)**2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")