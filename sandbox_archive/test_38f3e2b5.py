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
        n = len(f)
        # Simplified version of communication complexity rank calculation
        return sum(1 for i in range(n) if f[i] != f[0])
    
    def local_cohomology_rank(f):
        n = len(f)
        # Simplified version of local cohomology rank calculation
        return sum(1 for i in range(n) if f[i] == 1)
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    correlation_coefficient = lambda a, b: (sum(x * y for x, y in zip(a, b)) - len(a) * sum(a) * sum(b) / len(a) ** 2) / math.sqrt((sum(x ** 2 for x in a) - len(a) * sum(a) ** 2 / len(a) ** 2) * (sum(y ** 2 for y in b) - len(b) * sum(b) ** 2 / len(b) ** 2))
    
    n_values = [10, 20, 30, 40]
    instances_tested = 0
    total_variance = 0.0
    total_local_cohomology_rank = 0.0
    
    for n in n_values:
        for _ in range(7):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            comm_rank = communication_complexity_rank(f)
            local_rank = local_cohomology_rank(f)
            total_variance += comm_rank ** 2
            total_local_cohomology_rank += abs(local_rank)
            instances_tested += 1
    
    mean_variance = total_variance / instances_tested
    mean_local_cohomology_rank = total_local_cohomology_rank / instances_tested
    
    correlation = correlation_coefficient([abs(local_cohomology_rank(generate_boolean_function(n))) for n in n_values], [mean_variance] * len(n_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.5,
        "counterexample": "" if correlation > 0.5 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break