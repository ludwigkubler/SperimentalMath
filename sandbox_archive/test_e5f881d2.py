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
    
    def xor(a, b):
        return a != b
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_k_sat_instance(m, n):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(n), random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def compute_tropical_vector_space(f):
        n = int(math.log2(len(f)))
        T_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    T_f[i][j] = f[2**i]
                else:
                    T_f[i][j] = float('inf')
        return T_f
    
    def compute_minimal_rank(T_f):
        n = len(T_f) - 1
        rank = 0
        for i in range(n + 1):
            if all(T_f[j][i] == float('inf') for j in range(i + 1, n + 1)):
                rank += 1
        return rank
    
    def tusnady_2_box_discrepancy(F):
        m = len(F)
        n = max(max(clause) for clause in F)
        D = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                count = sum(1 for clause in F if i in clause and j not in clause)
                D[i][j] = abs(count - (m / 2))
        return max(max(row) for row in D)
    
    def spearman_rank_correlation(ranks_f, ranks_d):
        n = len(ranks_f)
        ranks_f_sorted = sorted(range(n), key=lambda i: ranks_f[i])
        ranks_d_sorted = sorted(range(n), key=lambda i: ranks_d[i])
        s = sum((ranks_f_sorted[i] - ranks_d_sorted[i]) ** 2 for i in range(n))
        return 1 - (6 * s) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks_f = []
    ranks_d = []
    
    for n in n_values:
        f = generate_xor_function(n)
        T_f = compute_tropical_vector_space(f)
        r_f = compute_minimal_rank(T_f)
        F = generate_k_sat_instance(2**n // 4, n)
        d = tusnady_2_box_discrepancy(F)
        
        ranks_f.append(r_f)
        ranks_d.append(d)
    
    correlation = spearman_rank_correlation(ranks_f, ranks_d)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.5,
        "counterexample": "" if correlation >= 0.5 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")