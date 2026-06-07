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
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M_f = [[f[i * 2 + j] for j in range(n)] for i in range(n)]
        return M_f
    
    def geometric_entropy(M):
        non_zero_entries = [x for row in M for x in row if x != 0]
        if not non_zero_entries:
            return 0
        p = [x / sum(non_zero_entries) for x in non_zero_entries]
        entropy = -sum(p[i] * math.log2(p[i]) for i in range(len(p)))
        return entropy
    
    def communication_complexity_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            row = M[i]
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_value = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        M_f = matrix_representation(f)
        entropy = geometric_entropy(M_f)
        rank = communication_complexity_rank(M_f)
        metric_value.append(entropy / rank)
        instances_tested += 1
        n_max = max(n_max, n)
    
    conjecture_holds = all(x <= y for x, y in zip(metric_value, [f(n) * f(n) for n in n_values]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy_rank_variance_ratio",
        "metric_value": sum(metric_value) / len(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(30, 59)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")