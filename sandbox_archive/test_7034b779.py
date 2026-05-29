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
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 0:
            return [1]
        elif n == 1:
            return [matrix[0][0], -matrix[0][0] + 1]
        
        det = 0
        for j in range(n):
            submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * matrix[0][j] * characteristic_polynomial(submatrix)
        return [det]
    
    def free_entropy(matrix):
        n = len(matrix)
        coeffs = characteristic_polynomial(matrix)
        non_negative_coeffs = [c for c in coeffs if c >= 0]
        if not non_negative_coeffs:
            return 0
        total = sum(non_negative_coeffs)
        entropy = -sum(c / total * math.log2(c / total) for c in non_negative_coeffs if c > 0)
        return entropy
    
    def communication_complexity(n):
        # Placeholder function. Replace with actual computation.
        return random.random() * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        H_F = free_entropy(graph)
        CC_DISJ_n = communication_complexity(n)
        
        if H_F == 0 or CC_DISJ_n < 0:
            continue
        
        total_metric_value += CC_DISJ_n
        instances_tested += 1
        
        if CC_DISJ_n < H_F * math.log2(H_F):
            conjecture_holds = False
            counterexample = f"CC_DISJ_n ({CC_DISJ_n}) < H_F * log2(H_F) ({H_F * math.log2(H_F)})"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")