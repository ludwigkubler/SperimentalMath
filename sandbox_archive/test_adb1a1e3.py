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
    
    def communication_complexity_rank(f):
        n = len(f)
        count = [f.count(i) for i in set(f)]
        max_count = max(count)
        return sum(1 for c in count if c == max_count)
    
    def frobenius_norm(V):
        return math.sqrt(sum(x**2 for x in V))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_frobenius = 0.0
    total_rank = 0.0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            rank = communication_complexity_rank(f)
            V = [f.count(i) / len(f) for i in set(f)]
            frobenius = frobenius_norm(V)
            
            total_frobenius += frobenius
            total_rank += rank
            instances_tested += 1
    
    mean_frobenius = total_frobenius / instances_tested
    mean_rank = total_rank / instances_tested
    correlation = (instances_tested * sum(f * r for f, r in zip(total_frobenius, total_rank)) -
                   total_frobenius * total_rank) / math.sqrt(
                       instances_tested * sum(f**2 for f in total_frobenius) - total_frobenius**2 *
                       instances_tested * sum(r**2 for r in total_rank) - total_rank**2)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.6 else "correlation_below_threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")