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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def matrix_representation(clauses, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            i, j = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                A[i][j] += 1
            elif clause[0] < 0 and clause[1] < 0:
                A[i][j] -= 1
        return A
    
    def tropical_symplectic_volume(A):
        n = len(A) - 1
        for i in range(n + 1):
            A[i][i] += 1
        
        # Gaussian elimination to find the volume
        for i in range(n):
            if A[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n + 1):
                factor = -A[j][i] / A[i][i]
                for k in range(i, n + 1):
                    A[j][k] += factor * A[i][k]
        
        volume = 1
        for i in range(n):
            volume *= max(0, A[i][i])
        return volume
    
    def entropy(clauses):
        total_clauses = len(clauses)
        counts = {}
        for clause in clauses:
            key = tuple(sorted(abs(x) for x in clause))
            if key not in counts:
                counts[key] = 1
            else:
                counts[key] += 1
        
        entropy_value = 0
        for count in counts.values():
            p = count / total_clauses
            entropy_value -= p * math.log2(p)
        
        return entropy_value
    
    n = random.randint(5, 40)
    m = random.randint(n**2 // 2, n**3 // 2)
    clauses = generate_cnf(n, m)
    
    A = matrix_representation(clauses, n)
    tsv = tropical_symplectic_volume(A)
    entropy_value = entropy(clauses)
    
    if tsv == float('inf'):
        return {
            "metric_name": "TSV",
            "metric_value": tsv,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "tropical_symplectic_volume_infinite"
        }
    
    correlation = (tsv - entropy_value) / (max(tsv, entropy_value) + 1e-9)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_less_than_0_5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")