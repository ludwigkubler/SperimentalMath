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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity(f):
        n = len(f)
        m = n.bit_length() - 1
        max_rank = 0
        for i in range(n):
            rank = sum(1 for j in range(m) if f[i] & (1 << j))
            max_rank = max(max_rank, rank)
        return max_rank
    
    def hodge_dimension(f):
        n = len(f)
        m = n.bit_length() - 1
        H = [[0] * (m + 1) for _ in range(m + 1)]
        H[0][0] = 1
        for i in range(1, m + 1):
            H[i][i-1] = H[i-1][i-1]
            H[i][i] = H[i-1][i-1]
        det = determinant(H)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def correlation_coefficient(dim_H, rank_com):
        n = len(dim_H)
        if n < 2:
            return None
        mean_dim_H = sum(dim_H) / n
        mean_rank_com = sum(rank_com) / n
        numerator = sum((dim_H[i] - mean_dim_H) * (rank_com[i] - mean_rank_com) for i in range(n))
        denominator = math.sqrt(sum((dim_H[i] - mean_dim_H) ** 2 for i in range(n))) * math.sqrt(sum((rank_com[i] - mean_rank_com) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else None
    
    instances_tested = 1000
    n_max = 40
    dim_H = []
    rank_com = []
    
    for _ in range(instances_tested):
        m = random.randint(5, n_max)
        f = generate_boolean_function(m)
        dim_H.append(hodge_dimension(f))
        rank_com.append(communication_complexity(f))
    
    metric_name = "Hodge Dimension vs Communication Complexity"
    metric_value = correlation_coefficient(dim_H, rank_com)
    conjecture_holds = metric_value is not None and abs(metric_value) > 0.9
    counterexample = "" if conjecture_holds else f"Correlation: {metric_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")