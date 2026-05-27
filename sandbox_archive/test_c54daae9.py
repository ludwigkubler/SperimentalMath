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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def tropical_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i][j] != float('-inf') for j in range(n)):
                rank += 1
        return rank
    
    def generate_monotone_kclique_instance(n, k):
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(2, n))
            clauses.append(clause)
        return clauses
    
    def tropicalize_Birkhoff_polytope(clauses):
        m = len(clauses)
        n = max(max(clause) for clause in clauses) + 1
        A = [[float('-inf')] * (n*n) for _ in range(m)]
        
        for i, clause in enumerate(clauses):
            for j in range(n):
                if j in clause:
                    A[i][j*n+j] = 0
                else:
                    A[i][j*n+j] = float('inf')
        
        return gaussian_elimination(A)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n//2, 10))
    F = generate_monotone_kclique_instance(n, k)
    P_F = tropicalize_Birkhoff_polytope(F)
    rank_P_F = tropical_rank(P_F)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank_P_F,
        "instances_tested": 1,
        "conjecture_holds": rank_P_F >= n**0.5,
        "counterexample": "" if rank_P_F >= n**0.5 else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")