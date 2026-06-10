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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def hodge_rank(A):
        rank = 0
        U, _, Vt = gaussian_elimination(A)
        for row in U:
            if any(row[j] != 0 for j in range(len(row))):
                rank += 1
        return rank
    
    def lidb(resolution_proof):
        # Simplified LIDB calculation (not actual implementation)
        return len(resolution_proof) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if time.time() + 20 > end_time:
            return {"seed": seed, "conjecture_holds": False, "counterexample": "budget_exceeded", "instances_tested": len(results), "n_max": max(n_values), "metric_name": "LIDB vs Hodge Rank", "metric_value": None}
        
        for _ in range(5):
            formula = [random.choice([0, 1]) for _ in range(n)]
            resolution_proof = []
            # Simulate resolution proof construction (not actual implementation)
            for i in range(n):
                if formula[i] == 1:
                    resolution_proof.append(i)
            
            lidb_value = lidb(resolution_proof)
            hodge_rank_value = hodge_rank([[random.choice([0, 1]) for _ in range(n)] for _ in range(n)])
            results.append((lidb_value, hodge_rank_value))
    
    if len(results) < 30:
        return {"seed": seed, "conjecture_holds": False, "counterexample": "insufficient_instances", "instances_tested": len(results), "n_max": max(n_values), "metric_name": "LIDB vs Hodge Rank", "metric_value": None}
    
    lidb_values = [r[0] for r in results]
    hodge_rank_values = [r[1] for r in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    std_lidb = math.sqrt(sum((x - mean_lidb) ** 2 for x in lidb_values) / len(lidb_values))
    mean_hodge_rank = sum(hodge_rank_values) / len(hodge_rank_values)
    std_hodge_rank = math.sqrt(sum((x - mean_hodge_rank) ** 2 for x in hodge_rank_values) / len(hodge_rank_values))
    
    correlation_coefficient = (sum((lidb_values[i] - mean_lidb) * (hodge_rank_values[i] - mean_hodge_rank) for i in range(len(lidb_values))) /
                               (len(lidb_values) * std_lidb * std_hodge_rank))
    
    return {
        "seed": seed,
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.8 else f"correlation={correlation_coefficient:.2f}",
        "instances_tested": len(results),
        "n_max": max(n_values),
        "metric_name": "LIDB vs Hodge Rank",
        "metric_value": correlation_coefficient
    }

if __name__ == "__main__":
    import sys
    import time
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    end_time = time.time() + 240
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")