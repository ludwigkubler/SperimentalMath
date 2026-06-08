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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def min_non_degenerate_representation(f):
        n = int(math.log2(len(f)))
        V = [f[i] for i in range(2**n) if f[i] != 0]
        return len(V)
    
    def communication_complexity_matrix(f):
        n = int(math.log2(len(f)))
        C = [[0] * (2**n) for _ in range(2**n)]
        for x in range(2**n):
            for y in range(2**n):
                if f[x] == f[y]:
                    C[x][y] = 1
        return C
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(i+1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        sigma_min = min_non_degenerate_representation(f)
        C = communication_complexity_matrix(f)
        rank_C = matrix_rank(C)
        results.append((n, sigma_min, rank_C))
    
    if not results:
        return {
            "metric_name": "sigma_min / Var(Rank(C))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    sigma_mins = [r[1] for r in results]
    rank_Cs = [r[2] for r in results]
    var_rank_C = variance(rank_Cs)
    
    if var_rank_C == 0:
        return {
            "metric_name": "sigma_min / Var(Rank(C))",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r[0] for r in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    ratio = sum(sigma_mins) / var_rank_C
    return {
        "metric_name": "sigma_min / Var(Rank(C))",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(r[0] for r in results),
        "conjecture_holds": True if ratio <= 1 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        mean_ratio = sum(r["metric_value"] for r in results[:first_failing_seed]) / first_failing_seed
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results[:first_failing_seed])) if first_failing_seed > 0 else None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_ratio:.2f} std={std_ratio:.2f} support_fraction={support_fraction:.2f}")