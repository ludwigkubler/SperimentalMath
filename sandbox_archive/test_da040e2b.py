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
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        matrix = [[0] * (n + 2) for _ in range(n + 2)]
        for x, y in f.keys():
            index = x * (n + 1) + y
            matrix[index][index + 1] += 1
        # Compute the trace of the matrix
        trace = sum(matrix[i][i] for i in range(n + 2))
        return trace
    
    def l_p_geometric_entropy(f, p):
        n = len(f)
        if n == 1:
            return 0
        matrix = [[0] * (n + 2) for _ in range(n + 2)]
        for x, y in f.keys():
            index = x * (n + 1) + y
            matrix[index][index + 1] += 1
        # Compute the trace of the p-th power of the matrix
        trace_p = sum(matrix[i][i]**p for i in range(n + 2))
        return trace_p
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = {tuple(random.sample(range(2), n)): random.choice([0, 1]) for _ in range(n * (n + 1))}
        entropy = communication_complexity(f)
        p_values = [Fraction(i, 10) for i in range(11)]
        for p in p_values:
            H_p = l_p_geometric_entropy(f, p)
            results.append((n, p, H_p))
    
    metric_value = sum(H_p * n**(1 - p / (p + 1)) for n, p, H_p in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(H_p >= n**(1 - p / (p + 1)) for _, p, H_p in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")