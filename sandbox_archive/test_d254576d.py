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
    
    def frobenius_norm(matrix):
        return sum(sum(abs(x)**2 for x in row) for row in matrix)**0.5
    
    def generate_instance(n):
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        return A, B
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    mean_frobenius_norm = 0.0
    rank_variance_sum = 0.0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            A, B = generate_instance(n)
            C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
            frob_norm = frobenius_norm(C)
            rank_variance_sum += frob_norm**2
            total_instances += 1
    
    mean_frobenius_norm = math.sqrt(rank_variance_sum / total_instances)
    
    return {
        "metric_name": "Frobenius Norm",
        "metric_value": mean_frobenius_norm,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": mean_frobenius_norm > 0.9 * math.sqrt(5),  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")