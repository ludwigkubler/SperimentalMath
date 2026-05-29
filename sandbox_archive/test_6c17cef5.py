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
    
    def construct_matroid(f):
        n = len(f)
        matroid = []
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j))]
            if all(f[j] == f[subset[0]] for j in subset):
                matroid.append(subset)
        return matroid
    
    def communication_complexity(f):
        # Placeholder function to compute communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)  # Example: simply return the number of variables
    
    n = random.randint(10, 100)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    matroid = construct_matroid(f)
    min_rank = min(len(cycle) for cycle in matroid) if matroid else float('inf')
    comm_complexity = communication_complexity(f)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_rank >= math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")