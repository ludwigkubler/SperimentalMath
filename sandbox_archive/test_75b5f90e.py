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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_vector_space(f):
        n = int(math.log2(len(f)))
        T_f = [[float('inf')] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if 2**i < len(f) and 2**j < len(f):
                    T_f[i][j] = min(f[2**i], f[2**j])
        return T_f
    
    def tusnady_2_box_discrepancy(T_f, n):
        m = len(T_f)
        D_2 = 0
        for i in range(m):
            row_max = max(T_f[i])
            col_max = max(row[T_i] for row in T_f for T_i in range(m) if (T_i & i) == i)
            D_2 += abs(row_max - col_max)
        return D_2 / m
    
    def spearman_rank_correlation(ranks):
        n = len(ranks)
        sorted_ranks = sorted(range(n), key=lambda x: ranks[x])
        rank_order = [sorted_ranks.index(i) for i in range(n)]
        n_ranks = list(range(1, n + 1))
        sum_diff_squares = sum((n_ranks[i] - rank_order[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks_r_f = []
    ranks_D_2 = []
    
    for n in n_values:
        f = generate_xor_function(n)
        T_f = compute_tropical_vector_space(f)
        D_2 = tusnady_2_box_discrepancy(T_f, n)
        
        r_f = sum(f) / len(f)
        ranks_r_f.append(r_f)
        ranks_D_2.append(D_2)
    
    correlation_coefficient = spearman_rank_correlation(ranks_r_f, ranks_D_2)
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": "" if correlation_coefficient >= 0.5 else "Spearman rank correlation coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")