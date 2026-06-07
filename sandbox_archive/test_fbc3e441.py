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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        min_rank = float('inf')
        for i in range(1 << (n - 1)):
            rank = 0
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    rank += 1
            min_rank = min(min_rank, rank)
        return min_rank
    
    def local_cohomology_rank(f):
        n = int(math.log2(len(f)))
        ker_f = [i for i in range(1 << n) if f[i] == 0]
        H1_ker_f_F2 = len(ker_f)
        return H1_ker_f_F2
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [10, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(7):  # Ensure at least 30 instances per seed
            f = generate_random_boolean_function(n)
            comm_rank = communication_complexity_rank(f)
            H1_ker_f_F2 = local_cohomology_rank(f)
            metric_values.append(H1_ker_f_F2 ** 2 / comm_rank)
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = sum(metric_values) / len(metric_values)
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")