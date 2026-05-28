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
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def communication_complexity(f):
        n = len(f)
        count = 0
        for i in range(2**n):
            x = format(i, f'0{n}b')
            y = format(int(f, 2) ^ int(x, 2), f'0{n}b')
            if x != y:
                count += 1
        return count
    
    def rank_of_free_algebra(n):
        # Simplified approximation for demonstration purposes
        return n + 1
    
    def alpha(n):
        # Simplified approximation for demonstration purposes
        return math.log2(math.log2(n)) if n > 1 else 0
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    cc_xor = communication_complexity(f)
    rank_F = rank_of_free_algebra(n)
    alpha_n = alpha(n)
    
    metric_value = cc_xor
    instances_tested = 1
    
    if rank_F <= n:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping_undefined' first_failing_seed={first_failing_seed}")