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
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def bp_read_twice_circuit_size(matrix):
        n = len(matrix)
        k = 0
        while True:
            found = False
            for i in range(n):
                for j in range(i + 1, n):
                    if matrix[i][j] != matrix[j][i]:
                        found = True
                        break
                if found:
                    break
            if not found:
                return k
            k += 1
    
    def geometric_entropy(matrix):
        n = len(matrix)
        count = sum(sum(row) for row in matrix)
        p = count / (n * n)
        q = 1 - p
        if p == 0 or q == 0:
            return 0
        return -p * math.log2(p) - q * math.log2(q)
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        for _ in range(30):
            matrix = generate_matrix(n)
            k = bp_read_twice_circuit_size(matrix)
            H_M = geometric_entropy(matrix)
            if H_M < 2**k:
                return {
                    "metric_name": "H(M) / 2^k",
                    "metric_value": None,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, H(M)={H_M}, 2^k={2**k}"
                }
            results.append(H_M / 2**k)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= 0.5]) / len(results)
    
    return {
        "metric_name": "H(M) / 2^k",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    
    if all(r is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min([r for r in results if r < 0.5]))]
        print(f"RESULT: FALSIFIED counterexample='H(M) / 2^k < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")