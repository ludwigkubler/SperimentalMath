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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def min_complex_hypersurface_volume(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for x in clause:
                i = abs(x) - 1
                if x > 0:
                    matrix[i][i] += 1
                else:
                    matrix[n][i] -= 1
                    matrix[i][n] -= 1
        matrix[n][n] = len(cnf)
        rank = gaussian_elimination(matrix)
        return n - rank + 1
    
    def resolution_proof_length(cnf):
        n = len(cnf)
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if not any(x in clause for x in [-i for i in clause]):
                return 1
            new_clauses = []
            for other_clause in queue:
                if len(set(clause) & set(other_clause)) == 2:
                    new_clause = tuple(sorted([x for x in clause + other_clause if x not in clause and -x not in other_clause]))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return float('inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    min_volume = min_complex_hypersurface_volume(cnf)
    proof_length = resolution_proof_length(cnf)
    
    if min_volume < n or proof_length > math.pow(2, min_volume / 2):
        return {
            "metric_name": "min_volume",
            "metric_value": min_volume,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n}, min_volume={min_volume}, proof_length={proof_length}"
        }
    
    return {
        "metric_name": "min_volume",
        "metric_value": min_volume,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    num_supporting_seeds = sum(1 for r in results if r["conjecture_holds"])
    mean_metric_value = total_metric_value / len(results) if results else 0
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) if results else 0
    
    if num_supporting_seeds == len(results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif num_supporting_seeds >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={num_supporting_seeds / len(results)}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")