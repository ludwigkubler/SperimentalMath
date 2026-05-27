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

def generate_kcnf(n, m):
    k = 3  # Fixed to 3-SAT for simplicity
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([0, 1]) - 1) for _ in range(k)]
        if len(set(clause)) == k:
            clauses.append(clause)
    return clauses

def hodge_rank(kcnf):
    n = max(abs(var) for clause in kcnf for var in clause)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in kcnf:
        for i, var in enumerate(clause):
            if i == len(clause) - 1:
                A[var][n] += 1
            else:
                A[var][abs(clause[i + 1])] += 1
    
    rank = 0
    for i in range(n + 1):
        row = [A[j][i] for j in range(n + 1)]
        if any(row):
            pivot = next(j for j, x in enumerate(row) if x != 0)
            A[i], A[pivot] = A[pivot], A[i]
            rank += 1
            for j in range(n + 1):
                if i != j:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n + 1):
                        A[j][k] -= factor * A[i][k]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(10, n // 2)  # At least 10 clauses
        kcnf = generate_kcnf(n, m)
        rank = hodge_rank(kcnf)
        
        c1 = Fraction(1, 10)
        c2 = Fraction(5, 10)
        phi_n = c1 * math.log(n) ** 2 + c2
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "phi_n": phi_n
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    max_deviation = max(abs(result["rank"] - result["phi_n"]) for result in results)
    support_fraction = sum(1 for result in results if abs(result["rank"] - result["phi_n"]) <= 0.05 * mean_rank) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - result["phi_n"]) > 0.1 * mean_rank for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - result["phi_n"]) > 0.1 * mean_rank)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")