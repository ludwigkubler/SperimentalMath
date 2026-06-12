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
    
    p = 2  # Fixed prime for p-adic expansion
    
    def generate_protocol(n):
        protocol = [random.randint(0, 1) for _ in range(n)]
        return protocol
    
    def p_adic_expansion(protocol, p):
        n = len(protocol)
        rank = [[0] * (n + 1) for _ in range(n + 1)]
        rank[0][0] = 1
        
        for i in range(1, n + 1):
            rank[i][i] = 1
            for j in range(i - 1, -1, -1):
                rank[j][j] += protocol[i - 1]
                if rank[j][j] >= p:
                    rank[j][j] -= p
        
        return rank
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        
        for i in range(m):
            if matrix[i][i] == 0:
                found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    return i
        
        rank = 0
        for i in range(m):
            if matrix[i][i] != 0:
                rank += 1
        
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_variance = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            protocol = generate_protocol(n)
            p_adic_expansion_value = p_adic_expansion(protocol, p)
            rank_value = matrix_rank(p_adic_expansion_value)
            variance_value = variance(protocol)
            
            total_rank += rank_value
            total_variance += variance_value
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    rank_mean = total_rank / instances_tested
    variance_mean = total_variance / instances_tested
    
    if variance_mean == 0:
        return {
            "metric_name": "Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    correlation = (instances_tested * sum((rank_value - rank_mean) * (variance_value - variance_mean) for rank_value, variance_value in zip(p_adic_expansion_value, protocol)) - total_rank * total_variance) / (math.sqrt(instances_tested * sum((rank_value - rank_mean) ** 2 for rank_value in p_adic_expansion_value) - total_rank ** 2) * math.sqrt(instances_tested * sum((variance_value - variance_mean) ** 2 for variance_value in protocol) - total_variance ** 2))
    
    return {
        "metric_name": "Rank",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")