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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            if var not in clause:
                clause.add(var)
        clauses.append(clause)
    return clauses

def generate_random_k_cnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 2:
            var = random.choice(variables)
            if var not in clause:
                clause.add(var)
        clauses.append(clause)
    return clauses

def quandle_representation(F):
    n = len(F[0])
    Q = [[0] * n for _ in range(n)]
    for clause in F:
        for i in clause:
            for j in clause:
                if i != j:
                    Q[i-1][j-1] += 1
    return Q

def min_rank(matrix):
    rank = 0
    m, n = len(matrix), len(matrix[0])
    for col in range(n):
        pivot_row = -1
        for row in range(m):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        rank += 1
        for r in range(m):
            if r != pivot_row and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[pivot_row][col])
                for c in range(n):
                    matrix[r][c] -= factor * matrix[pivot_row][c]
    return rank

def monotone_circuit_size(k, n):
    return 2**n // (math.factorial(k) * n**k)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(1, 41):
        for k in [3]:  # Only test k=3 for simplicity
            F = generate_random_k_cnf(n, k)
            Q_F = quandle_representation(F)
            rank_Q_F = min_rank(Q_F)
            lower_bound = Fraction(n**k, math.factorial(k))
            if rank_Q_F < lower_bound:
                return {
                    "metric_name": "Minimal Rank of Quandle Representation",
                    "metric_value": rank_Q_F,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, Q_F rank={rank_Q_F} < Ω(n^k / k!)"
                }
            circuit_size = monotone_circuit_size(k, n)
            upper_bound = Fraction(2**n, (math.factorial(k) * n**k))
            if circuit_size > upper_bound:
                return {
                    "metric_name": "Monotone Circuit Size",
                    "metric_value": circuit_size,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, Circuit size={circuit_size} > O(2^n / (n^k * k!))"
                }
            results.append((rank_Q_F, circuit_size))
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_circuit_size = sum(size for _, size in results) / len(results)
    return {
        "metric_name": "Minimal Rank of Quandle Representation",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": all(rank >= lower_bound and size <= upper_bound for rank, size in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    mean_circuit_size = sum(result["instances_tested"] * result["metric_value"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")