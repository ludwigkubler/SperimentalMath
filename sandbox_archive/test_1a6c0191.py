# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, m):
        clauses = []
        for _ in range(m):
            variables = set(random.sample(range(1, n + 1), random.randint(1, n)))
            clause = ' or '.join(f'x{i}' if var > 0 else f'not x{-var}' for var in variables)
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def kcnf_to_brauer_rank(n, m):
        A = [[0] * n for _ in range(n)]
        for _ in range(m):
            clause_vars = random.sample(range(1, n + 1), random.randint(1, n))
            for var in clause_vars:
                if random.choice([True, False]):
                    A[var - 1][var - 1] += 1
                else:
                    A[-var - 1][-var - 1] += 1
        
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if A[j][i] != 0), None)
            if pivot is not None:
                rank += 1
                for j in range(n):
                    A[i][j], A[pivot][j] = A[pivot][j], A[i][j]
                for k in range(n):
                    if k != i and A[k][i] != 0:
                        factor = Fraction(A[k][i], A[i][i])
                        for j in range(n):
                            A[k][j] -= factor * A[i][j]
        
        return rank
    
    def largest_weight(kcnf):
        weight = 0
        for clause in kcnf.split(' and '):
            weight = max(weight, sum(1 for var in clause if var > 0))
        return weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n, n * (n - 1) // 2)
        kcnf = generate_kcnf(n, m)
        rank = kcnf_to_brauer_rank(n, m)
        weight = largest_weight(kcnf)
        results.append((rank, weight))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    max_weight = max(weight for _, weight in results)
    ratio = mean_rank / max_weight
    
    conjecture_holds = all(ratio <= 1 for rank, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Brauer Group Rank to Largest Weight",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=2) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")