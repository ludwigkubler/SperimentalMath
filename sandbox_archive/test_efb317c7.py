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
    
    n = 40
    vectors = [random.choices(range(-10, 11), k=n) for _ in range(2)]
    tensor_product = [[sum(a * b for a, b in zip(v1, v2)) for v2 in vectors[1]] for v1 in vectors[0]]
    
    def is_permutation_matrix(matrix):
        n = len(matrix)
        if any(len(row) != n for row in matrix): return False
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            if sum(matrix[i]) != 1 or sum(matrix[j][i] for j in range(n)) != 1: return False
        return True
    
    min_rank = float('inf')
    for row in tensor_product:
        rank = len(set(row))
        if rank < min_rank:
            min_rank = rank
    
    conjecture_holds = is_permutation_matrix(tensor_product)
    counterexample = "Non-permutation matrix" if not conjecture_holds else ""
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")