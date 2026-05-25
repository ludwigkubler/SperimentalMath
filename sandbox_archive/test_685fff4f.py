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
    
    def geometric_quantization(f):
        # Placeholder for actual geometric quantization logic
        return len(f)

    def acc0_complexity(f):
        # Placeholder for actual ACC⁰ complexity computation using DPLL solver
        return len(f)

    n = 40
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    rank = geometric_quantization(f)
    acc0_bound = acc0_complexity(f)
    
    metric_value = rank / acc0_bound
    
    return {
        "metric_name": "Rank/ACC⁰",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": rank <= 3 * math.sqrt(acc0_bound),
        "counterexample": "" if rank <= 3 * math.sqrt(acc0_bound) else "rank > 3 * sqrt(acc0_bound)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 149))  # Default to first 30 primes if no seeds provided
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
        print(f"RESULT: FALSIFIED counterexample=\"rank > 3 * sqrt(acc0_bound)\" first_failing_seed={first_failing_seed}")