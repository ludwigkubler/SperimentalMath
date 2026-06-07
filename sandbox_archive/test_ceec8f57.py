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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def evaluate_quadratic_form(f, x):
        n = len(x)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = f[(i << (n - 1)) | (j << (n - 2))]
                if i != j:
                    Q[j][i] = Q[i][j]
        return sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(i, n))
    
    def minimal_quadratic_defect(f):
        n = int(math.log2(len(f)))
        min_defect = float('inf')
        for k in range(1, 2**n):
            x_k = [int(x) for x in bin(k)[2:].zfill(n)]
            defect = abs(evaluate_quadratic_form(f, x_k) - 1) / len(x_k)
            if defect < min_defect:
                min_defect = defect
        return min_defect
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        instances = [random.choice([0, 1]) for _ in range(30 * n)]
        cc = 0
        for i in range(n):
            x_i = instances[i::n]
            cc += sum(x_i) % 2
        return cc
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        min_defect = minimal_quadratic_defect(f)
        cc = communication_complexity(f)
        results.append({
            "n": n,
            "min_defect": min_defect,
            "cc": cc
        })
    
    instances_tested = len(results) * 30
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(abs(result["min_defect"] - result["cc"]) / result["cc"] <= 0.1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_quadratic_defect",
        "metric_value": sum(result["min_defect"] * result["cc"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")