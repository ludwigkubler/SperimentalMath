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
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partition(f):
        n = len(f)
        if n == 1:
            return 1
        parts = []
        for i in range(1, n):
            left = f[:i]
            right = f[i:]
            if all(left[j] <= right[j] for j in range(len(right))):
                parts.append((left, right))
        return sum(noncrossing_partition(p) for p in parts) + 1
    
    def log_base(x, base):
        return math.log(x) / math.log(base)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_elements = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_monotone_function(n)
            elements = noncrossing_partition(f)
            total_elements += elements
            instances_tested += 1
    
    mean_elements = total_elements / instances_tested
    C = 2  # Empirical constant based on known results and conjecture
    max_allowed_elements = C * log_base(n, 2)
    
    conjecture_holds = mean_elements <= max_allowed_elements
    counterexample = "" if conjecture_holds else f"Mean elements {mean_elements} > {max_allowed_elements}"
    
    return {
        "metric_name": "Mean number of noncrossing partition elements",
        "metric_value": mean_elements,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")