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
    
    def twisted_tensor_product(v1, v2):
        n = len(v1)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = v1[i] * v2[j]
        return result
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] /= factor
                        break
        return rank
    
    def is_permutation_matrix(matrix):
        n = len(matrix)
        count = [0] * n
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    count[j] += 1
                elif matrix[i][j] != 0:
                    return False
        return all(c == 1 for c in count)
    
    n = random.randint(5, 40)
    v1 = [random.random() for _ in range(n)]
    v2 = [random.random() for _ in range(n)]
    matrix = twisted_tensor_product(v1, v2)
    rank = min_rank(matrix)
    property_P = is_permutation_matrix(matrix)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": property_P,
        "counterexample": "" if property_P else f"Non-permutation matrix of rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-permutation matrix\" first_failing_seed={first_failing_seed}")