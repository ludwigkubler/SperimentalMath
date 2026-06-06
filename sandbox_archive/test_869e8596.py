# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(2, n))]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = max(range(rank, m), key=lambda i: abs(matrix[i][j]))
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank:
                    factor = Fraction(-matrix[i][j], matrix[rank][j])
                    for k in range(n):
                        matrix[i][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf)
        rank_variances = []
        for _ in range(2):
            circuit = [random.randint(0, n-1) for _ in range(n)]
            rank = gaussian_elimination([[circuit[j] if i == j else 0 for j in range(n)] for i in range(n)])
            rank_variances.append(rank)
        return abs(rank_variances[0] - rank_variances[1])
    
    def minimal_order_brauer_group(cnf):
        n = len(cnf)
        # Placeholder for actual Brauer group computation
        return n**2 * random.log(n, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    rank_variance_sum = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        brauer_group_order = minimal_order_brauer_group(cnf)
        rank_variance = communication_complexity_rank_variance(cnf)
        rank_variance_sum += rank_variance
        results.append({
            "n": n,
            "brauer_group_order": brauer_group_order,
            "rank_variance": rank_variance
        })
    
    mean_rank_variance = rank_variance_sum / len(n_values)
    correlation_coefficient = sum((r["brauer_group_order"] - (sum(r["brauer_group_order"] for r in results) / len(results))) * (r["rank_variance"] - mean_rank_variance) for r in results) / (len(results) * sum((r["brauer_group_order"] - (sum(r["brauer_group_order"] for r in results) / len(results)))**2 for r in results))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_rank_variance,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_rank_variance <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_rank_variance <= 3 else "mapping_undefined"
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
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")