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
    
    def generate_monotone_dnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def matroid_rank(clauses, n):
        incidence_matrix = [[0] * n for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                incidence_matrix[i][var - 1] = 1
        
        rank = 0
        for row in incidence_matrix:
            if any(row[j] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def gaussian_elimination(matrix, n):
        augmented_matrix = [row[:] + [i] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
        
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        return [row[-1] for row in augmented_matrix if any(row[:n])]

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            clauses = generate_monotone_dnf(n, k=3)
            rank = matroid_rank(clauses, n)
            if rank < n ** (1.5):
                return {
                    "metric_name": "matroid_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k=3, rank={rank}"
                }
            results.append(rank)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r >= n ** (1.5)]) / len(results)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, rank<{results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")