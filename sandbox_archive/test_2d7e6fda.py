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
    
    def calculate_geometric_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != f[0]:
                count += 1
        return count / (2**n)
    
    def calculate_communication_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            if any(f[j] != f[j + 2**i] for j in range(2**(n - i))):
                rank += 1
        return rank
    
    def calculate_variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        gc = calculate_geometric_complexity(f)
        cr = calculate_communication_rank(f)
        results.append((gc, cr))
    
    if not results:
        return {
            "metric_name": "Var(CR(f))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gc_values, cr_values = zip(*results)
    var_cr = calculate_variance(cr_values)
    corr_coeff = sum((gc - sum(gc_values) / len(gc_values)) * (cr - sum(cr_values) / len(cr_values)) for gc, cr in results) / (len(results) * math.sqrt(sum((gc - sum(gc_values) / len(gc_values)) ** 2 for gc in gc_values)) * math.sqrt(sum((cr - sum(cr_values) / len(cr_values)) ** 2 for cr in cr_values)))
    
    return {
        "metric_name": "Var(CR(f))",
        "metric_value": var_cr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.5,
        "counterexample": "" if corr_coeff > 0.5 else "correlation_coefficient_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = next((result["counterexample"] for result in results if result["conjecture_holds"] == False), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        mean_var_cr = sum(result["metric_value"] for result in results) / len(results)
        std_var_cr = math.sqrt(sum((result["metric_value"] - mean_var_cr) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_var_cr} std={std_var_cr} support_fraction={support_fraction}")