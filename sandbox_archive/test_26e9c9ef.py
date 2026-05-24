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
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def bp_read_twice_circuit_size(matrix):
        n = len(matrix)
        if n == 1:
            return 1
        k = 0
        while True:
            k += 1
            if (2 ** k) >= n * n:
                return k
    
    def geometric_entropy(matrix):
        n = len(matrix)
        total = 0
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    total += 1
        p = Fraction(total, n * n)
        entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        return entropy
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 20, 40])
        matrix = generate_matrix(n)
        k = bp_read_twice_circuit_size(matrix)
        H_M = geometric_entropy(matrix)
        if H_M < 2 ** k:
            return {
                "metric_name": "H(M) / 2^k",
                "metric_value": H_M / (2 ** k),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Matrix of size {n} with H(M) < 2^k"
            }
        results.append(H_M / (2 ** k))
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "H(M) / 2^k",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": all(x >= 1 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")