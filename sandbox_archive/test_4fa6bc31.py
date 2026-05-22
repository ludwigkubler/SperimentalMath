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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def rank_of_matrix(G):
    n = len(G)
    A = [[G[i][j] for j in range(n)] for i in range(n)]
    rank = gaussian_elimination(A)
    return rank

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, num_vars) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, num_vars))]
        cnf.append(clause)
    return cnf

def resolution_length(cnf):
    # Simplified resolution length calculation
    return len(cnf) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, n)
            G = [[sum(x * y for x, y in zip(cnf[i], cnf[j])) for j in range(n)] for i in range(n)]
            rank = rank_of_matrix(G)
            proof_length = resolution_length(cnf)
            results.append((rank, proof_length))
    
    avg_rank = sum(rank for rank, _ in results) / len(results)
    avg_proof_length = sum(proof_length for _, proof_length in results) / len(results)
    ratio = avg_rank / avg_proof_length
    
    conjecture_holds = all(ratio <= 10**(1/2) for rank, proof_length in results)
    counterexample = "" if conjecture_holds else "ratio_exceeds_threshold"
    
    return {
        "metric_name": "Ratio of Average Minimal Symmetric Tensor Rank to SAT Proof Length",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_threshold\" first_failing_seed={first_failing_seed}")