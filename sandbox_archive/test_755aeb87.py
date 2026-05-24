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
    
    def bp_read_twice_circuit_size(matrix):
        n = len(matrix)
        if n == 1:
            return 0
        k = 1
        while True:
            for _ in range(2**k):
                new_matrix = [[matrix[i][j] ^ matrix[(i + j) % n][(i - j) % n] for j in range(n)] for i in range(n)]
                if new_matrix == matrix:
                    return k
            k += 1
    
    def geometric_entropy(matrix):
        n = len(matrix)
        count = sum(sum(row) for row in matrix)
        entropy = 0
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    p = (count + 1) / (2 * n * n)
                    entropy -= p * math.log2(p)
        return entropy
    
    def generate_random_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        for _ in range(30):
            matrix = generate_random_matrix(n)
            k = bp_read_twice_circuit_size(matrix)
            H_M = geometric_entropy(matrix)
            if H_M < 2**k:
                return {
                    "metric_name": "H(M) / 2^k",
                    "metric_value": float('inf'),
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Matrix of size {n} does not satisfy H(M) >= 2^k"
                }
            results.append(H_M / 2**k)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    
    return {
        "metric_name": "H(M) / 2^k",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")