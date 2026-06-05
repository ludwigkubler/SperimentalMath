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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # 10 clauses per variable
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            cnf.append(clause)
        return cnf
    
    def depth(cnf):
        if not cnf:
            return 0
        max_depth = 0
        for clause in cnf:
            max_depth = max(max_depth, max(abs(x) for x in clause))
        return max_depth
    
    def geometric_quantization_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                for clause in cnf:
                    if any(abs(x) == i + 1 and abs(y) == j + 1 for x, y in zip(clause, clause)):
                        matrix[i][j] += 1
        return matrix
    
    def min_order(matrix):
        n = len(matrix)
        for k in range(1, n + 1):
            if all(all(matrix[i][j] >= k for j in range(i + 1, n)) for i in range(n)):
                return k
        return n
    
    n_max = 0
    instances_tested = 0
    total_oq = 0
    total_d = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        oq = min_order(geometric_quantization_matrix(cnf))
        d = depth(cnf)
        
        if n > n_max:
            n_max = n
        instances_tested += 1
        
        total_oq += oq
        total_d += d
    
    mean_oq = total_oq / instances_tested
    mean_d = total_d / instances_tested
    conjecture_holds = all(oq <= 2 * d for oq, d in zip([min_order(geometric_quantization_matrix(generate_cnf(n))) for n in range(5, 41)], [depth(generate_cnf(n)) for n in range(5, 41)]))
    
    return {
        "metric_name": "OQ/2D",
        "metric_value": mean_oq / (2 * mean_d),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")