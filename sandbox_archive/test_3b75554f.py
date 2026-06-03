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
    
    def generate_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_quasi_parseval_space(protocol):
        # Compute the quasi-Parseval space Q(P) associated with the protocol
        qps = []
        for p in protocol:
            if p == 0:
                qps.append([1, -1])
            else:
                qps.append([-1, 1])
        return qps
    
    def min_rank(matrix):
        # Compute the minimal rank of a matrix
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            rank += 1
            for j in range(m):
                matrix[i][j] /= matrix[i][j]
            for k in range(n):
                if k != i and any(matrix[k][j] != 0 for j in range(m)):
                    for j in range(m):
                        matrix[k][j] -= matrix[i][j] * matrix[k][j]
        return rank
    
    def communication_complexity_rank(protocol):
        # Compute the communication complexity rank r(P)
        n = len(protocol)
        rank = 0
        for i in range(n):
            if protocol[i] == 0:
                rank += 1
            else:
                rank -= 1
        return abs(rank) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    min_ranks = []
    r_Ps = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            protocol = generate_protocol(n)
            qps = compute_quasi_parseval_space(protocol)
            min_rank_value = min_rank(qps)
            r_P_value = communication_complexity_rank(protocol)
            
            total_instances += 1
            min_ranks.append(min_rank_value)
            r_Ps.append(r_P_value)
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_r_P = sum(r_Ps) / len(r_Ps)
    
    conjecture_holds = all(log(n) <= m <= r for n, m, r in zip(n_values, min_ranks, r_Ps))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_min_rank,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")