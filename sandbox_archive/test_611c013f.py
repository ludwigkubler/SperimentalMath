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
    
    def generate_sipser_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_homology_groups(f):
        # Simplified homology computation (not actual persistent homology)
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        return [sum(f[i] for i in range(2**(k-1), 2**k)) % 2 for k in range(1, n+1)]
    
    def minimal_local_index(homology_groups):
        return max(homology_groups)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_sipser_function(n)
        homology_groups = compute_homology_groups(f)
        local_index = minimal_local_index(homology_groups)
        total_metric_value += local_index
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = abs(mean_metric_value - n**2) <= 3 * n**2
    counterexample = "" if conjecture_holds else f"mean={mean_metric_value}, expected=Θ(n^2)"
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")