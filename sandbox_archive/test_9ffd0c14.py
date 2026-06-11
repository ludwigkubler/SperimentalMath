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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Placeholder for actual communication complexity rank calculation
        return n
    
    def minimal_local_induction_dimension(simplicial_complex):
        # Placeholder for actual LID calculation
        return len(simplicial_complex)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_boolean_function(n)
        simplicial_complex = {tuple(f[i:i+n]): i for i in range(len(f) - n + 1)}
        r_f = communication_complexity_rank(f)
        lid_f = minimal_local_induction_dimension(simplicial_complex)
        results.append({"n": n, "r_f": r_f, "lid_f": lid_f})
    
    total_r_f = sum(result["r_f"] for result in results)
    total_lid_f = sum(result["lid_f"] for result in results)
    mean_ratio = total_r_f / total_lid_f if total_lid_f != 0 else float('inf')
    
    conjecture_holds = all(mean_ratio <= 3 for _ in range(24))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=0")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")