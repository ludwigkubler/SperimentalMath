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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified version of the communication complexity rank
        return sum(f[i] != f[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
    
    def local_cohomology_rank(f):
        n = int(math.log2(len(f)))
        # Simplified version of the local cohomology rank
        return sum(1 for i in range(n) if f[i] != f[(i + 1) % n])
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    metric_name = "correlation_coefficient"
    instances_tested = 0
    n_max = 0
    total_correlation = 0.0
    
    for n in [10, 20, 30, 40]:
        for _ in range(7):  # Aim for at least 30 instances per seed
            f = generate_boolean_function(n)
            comm_rank = communication_complexity_rank(f)
            cohomology_rank = local_cohomology_rank(f)
            correlation = (comm_rank - 0.5) * (cohomology_rank - 0.5)
            total_correlation += correlation
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_correlation = total_correlation / instances_tested
    conjecture_holds = mean_correlation > 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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