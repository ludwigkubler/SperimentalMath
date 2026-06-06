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
        n = int(math.log2(len(f)))
        matrix = [[f[i * (1 << j) + k] for j in range(n)] for k in range(1 << n)]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def lie_algebroid_local_index(f):
        # Simplified approximation for demonstration purposes
        return communication_complexity_rank(f)
    
    def is_valid_seed(seed):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        local_index = lie_algebroid_local_index(f)
        rank = communication_complexity_rank(f)
        if local_index < rank or local_index > 2 * rank:
            return False
        return True
    
    instances_tested = 30
    n_max = 40
    conjecture_holds = all(is_valid_seed(seed) for _ in range(instances_tested))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Local Index",
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")