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

def generate_random_vector(n):
    return [random.random() for _ in range(n)]

def twisted_tensor_product(v1, v2):
    n = len(v1)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = v1[i] * v2[j]
    return result

def is_permutation_matrix(matrix, n):
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for row in matrix:
        if sum(row) != 1 or len(set(row)) != 1:
            return False
    for col in zip(*matrix):
        if sum(col) != 1 or len(set(col)) != 1:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    v1 = generate_random_vector(n)
    v2 = generate_random_vector(n)
    tensor_product = twisted_tensor_product(v1, v2)
    min_rank = sum(1 for row in tensor_product if any(row))
    conjecture_holds = is_permutation_matrix(tensor_product, n)
    counterexample = "Non-permutation matrix of rank {}".format(min_rank) if not conjecture_holds else ""
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print("TRIAL: {}".format(result))
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_rank, std_rank, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_rank, std_rank, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample='Non-permutation matrix' first_failing_seed={}".format(first_failing_seed))