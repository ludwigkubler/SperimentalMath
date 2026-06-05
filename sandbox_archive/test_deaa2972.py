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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_from_function(f, n):
        A = [[f[i * (1 << n) + j] for i in range(1 << (n-1))] for j in range(1 << (n-1))]
        return A
    
    def communication_complexity_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i][j] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def quasi_crystals_required(A):
        m, n = len(A), len(A[0])
        count = 0
        for i in range(m):
            for j in range(n):
                if A[i][j] == 1:
                    count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = matrix_from_function(f, n)
        rank = communication_complexity_rank(A)
        Q = quasi_crystals_required(A)
        
        if rank == 0 or Q == 0:
            continue
        
        results.append({
            "n": n,
            "Q": Q,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "Q/f vs rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    Q_values = [r["Q"] for r in results]
    rank_values = [r["rank"] for r in results]
    mean_Q_over_rank = sum(Q / rank for Q, rank in zip(Q_values, rank_values)) / len(results)
    std_dev = math.sqrt(sum((Q / rank - mean_Q_over_rank) ** 2 for Q, rank in zip(Q_values, rank_values)) / len(results))
    
    return {
        "metric_name": "Q/f vs rank",
        "metric_value": mean_Q_over_rank,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(mean_Q_over_rank - 1) <= 0.5 and std_dev <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
    else:
        mean_value = None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["instances_tested"] >= 30 for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std=Unknown support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Not enough instances supported\" first_failing_seed={first_failing_seed}")
    else:
        n_tested = sum(r["instances_tested"] for r in results)
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={n_tested}")