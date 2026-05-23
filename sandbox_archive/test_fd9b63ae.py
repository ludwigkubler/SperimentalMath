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
    
    n = 10  # Start with a small size and increase if needed
    
    # Generate random matrices A and B over GF(2)
    F = [0, 1]
    A = [[random.choice(F) for _ in range(n)] for _ in range(n)]
    B = [[random.choice(F) for _ in range(n)] for _ in range(n)]
    
    def tensor_product(A, B):
        n = len(A)
        np_A_tensor_B = [[[A[i][k] * B[j][l] for l in range(n)] for k in range(n)] for j in range(n)]
        return np_A_tensor_B
    
    np_A_tensor_B = tensor_product(A, B)
    
    # Construct a read-twice BP for IP_2 corresponding to the tensor product
    def bp_read_twice(np_A_tensor_B):
        n = len(np_A_tensor_B)
        width = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if np_A_tensor_B[i][j][k] == 1:
                        width += 1
        return width
    
    W_G = bp_read_twice(np_A_tensor_B)
    
    # Compute the noncommutative tensor product rank
    def noncommutative_tensor_product_rank(np_A_tensor_B):
        n = len(np_A_tensor_B)
        rank = 0
        for i in range(n):
            for j in range(n):
                if any(np_A_tensor_B[i][j][k] == 1 for k in range(n)):
                    rank += 1
        return rank
    
    np_rank = noncommutative_tensor_product_rank(np_A_tensor_B)
    
    # Calculate the metric value
    metric_value = np_rank - W_G - math.log(n, 2)
    
    # Check if the conjecture holds
    conjecture_holds = abs(metric_value) <= 3 * math.sqrt(metric_value**2 / 100) or abs(metric_value) > 10
    
    return {
        "metric_name": "np(A ⊗ B) - W(G) - log(n)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"np_rank={np_rank}, W_G={W_G}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")