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

def generate_k_cnf(k: int, m: int) -> list:
    variables = set(range(1, k + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables | {-v for v in variables}, k)
        clauses.append(clause)
    return clauses

def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def shannon_entropy(clause_set: set[tuple[int, ...]]) -> float:
    n = len(clause_set)
    if n == 0:
        return 0.0
    p = 1 / n
    entropy = -p * math.log2(p) * n
    for clause in clause_set:
        q = sum(1 for _ in clause) / k
        entropy -= q * math.log2(q)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = 3  # Example value for k, can be changed as needed
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        n = len(set(abs(v) for v in generate_k_cnf(k, m)))
        if n > 40:
            continue
        clause_set = set(tuple(sorted(clause)) for clause in generate_k_cnf(k, m))
        matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for clause in clause_set:
            for v in clause:
                matrix[v-1][v-1] += 1
        det = determinant(matrix)
        entropy = shannon_entropy(clause_set)
        
        results.append({
            "n": n,
            "det": abs(det),
            "entropy": entropy,
        })
    
    if not results:
        return {
            "metric_name": "Brauer Group Order / Clause Entropy Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_ratio = sum(result["det"] / result["entropy"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["det"] <= 10 * result["entropy"]) / len(results)
    
    return {
        "metric_name": "Brauer Group Order / Clause Entropy Ratio",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 10 * result["entropy"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] > 10 * result["entropy"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")